import trio
from astroplant_kit.peripheral import *
from . import environment

class VirtualDisplay(Display):
    def display(self, str):
        print("---VirtualDisplay---")
        print(str)
        print("--------------------")


class Heater(Actuator):
    """
    A heater actuator implementation using the virtual simulated environment.
    """

    RUNNABLE = True

    def __init__(self, *args, configuration):
        super().__init__(*args)
        print(f'config for {self.name}: {configuration}')

    async def do(self, command):
        print(f'got command: {command}')

    async def run(self):
        """
        Asynchronously run the peripheral device.
        """
        pass
