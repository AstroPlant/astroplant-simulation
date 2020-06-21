import logging
import trio
import io
import numpy as np
import random
import schedule
from datetime import datetime, time
from PIL import Image
from astroplant_kit.peripheral import Data, Peripheral, PeripheralCommandResult

logger = logging.getLogger("astroplant_simulation.camera")


def _rgb_to_png(rgb) -> bytes:
    im = Image.fromarray(rgb)
    bytes_stream = io.BytesIO()
    im.save(bytes_stream, format="png")
    bytes_stream.seek(0)
    return bytes_stream.read()


def _generate_art():
    """Generates recursively operated-on images."""
    DEPTH_MAX = 11
    DEPTH_MIN = 3
    WIDTH = 600
    HEIGHT = 400

    def random_color():
        return np.tile(np.random.standard_normal((1, 1, 3)), (HEIGHT, WIDTH, 1))

    def horizontal_linspace():
        c1 = np.linspace(
            np.random.standard_normal(), np.random.standard_normal(), num=WIDTH
        ).reshape((1, WIDTH))
        c2 = np.linspace(
            np.random.standard_normal(), np.random.standard_normal(), num=WIDTH
        ).reshape((1, WIDTH))
        c3 = np.linspace(
            np.random.standard_normal(), np.random.standard_normal(), num=WIDTH
        ).reshape((1, WIDTH))
        c = np.stack((c1, c2, c3), axis=-1)
        return np.tile(c, (HEIGHT, 1, 1))

    def vertical_linspace():
        c1 = np.linspace(
            np.random.standard_normal(), np.random.standard_normal(), num=HEIGHT
        ).reshape((HEIGHT, 1))
        c2 = np.linspace(
            np.random.standard_normal(), np.random.standard_normal(), num=HEIGHT
        ).reshape((HEIGHT, 1))
        c3 = np.linspace(
            np.random.standard_normal(), np.random.standard_normal(), num=HEIGHT
        ).reshape((HEIGHT, 1))
        c = np.stack((c1, c2, c3), axis=-1)
        return np.tile(c, (1, WIDTH, 1))

    def divide(x1, x2):
        return np.divide(x1, np.maximum((x2 + 1.0) / 2.0, 0.1))

    def arcsin(x):
        return np.arcsin(x.clip(-1.0, 1.0))

    def rescale(x):
        low = np.percentile(x, 5)
        high = np.percentile(x, 95)
        scale = np.maximum(high - low, 0.1)
        return (x - low) / scale * 2.0 - 1.0

    def generate(depth=0):
        functions = []
        if depth >= DEPTH_MIN:
            functions += [
                (random_color, 0),
                (horizontal_linspace, 0),
                (vertical_linspace, 0),
            ]
        if depth < DEPTH_MAX:
            functions += [
                (np.sin, 1),
                (np.cos, 1),
                (arcsin, 1),
                (rescale, 1),
                (np.add, 2),
                (np.subtract, 2),
                (np.multiply, 2),
                (divide, 2),
            ]
        fun, num_inputs = random.choice(functions)
        inputs = [generate(depth + 1) for n in range(num_inputs)]
        return fun(*inputs)

    img = generate()
    return ((img.clip(-1.0, 1.0) + 1.0) / 2.0 * 255.0).astype(np.uint8)


class Random(Peripheral):
    COMMANDS = True
    RUNNABLE = True

    def __init__(self, *args, configuration=None):
        super().__init__(*args)

        self._nursery = None
        self._scheduler = schedule.Scheduler()
        for task in configuration["schedule"]:
            self._scheduler.every().day.at(task["time"]).do(
                self._spawn_command, task["command"]
            )

    def _spawn_command(self, command):
        self._nursery.start_soon(self._handle_command_with_control, command)

    async def _handle_command_with_control(self, command):
        # Block until nothing can call `do` anymore.
        async with self.manager.control(self):
            return await self._handle_command(command)

    async def _handle_command(self, command):
        if command == "uniform":
            rgb = np.random.uniform(0, 255, (400, 600, 3,)).astype(dtype=np.uint8)
            result = _rgb_to_png(rgb)
            name = "uniform.png"
        elif command == "art":
            rgb = _generate_art()
            result = _rgb_to_png(rgb)
            name = "art.png"

        media = self.create_media(name, "image/png", result, None)
        await self._publish_data(Data(media))
        return media

    async def run(self):
        async with trio.open_nursery() as nursery:
            while True:
                self._nursery = nursery
                await trio.sleep(self._scheduler.idle_seconds)
                self._scheduler.run_pending()

    async def do(self, command):
        logger.debug(f"received command {command}")
        media = await self._handle_command(command)
        # await self._publish_data(Data(media))
        return PeripheralCommandResult(media=media)
