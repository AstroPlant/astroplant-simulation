import trio
from astroplant_kit.peripheral import Display, Actuator
from .environment import environment


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
        print(f"config for {self.name}: {configuration}")

    async def do(self, command):
        FULL_WATTAGE = 10.0
        if "heat" in command:
            environment.set_kit_heating(
                self.name, FULL_WATTAGE * command["heat"] / 100.0
            )

    async def run(self):
        """
        Asynchronously run the peripheral device.
        """
        pass
