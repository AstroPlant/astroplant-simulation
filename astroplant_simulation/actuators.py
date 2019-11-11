import trio
from astroplant_kit.peripheral import *
from . import environment

class VirtualDisplay(Display):
    def display(self, str):
        print("---VirtualDisplay---")
        print(str)
        print("--------------------")

