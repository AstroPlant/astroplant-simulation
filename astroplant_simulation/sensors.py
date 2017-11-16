import asyncio
import random
from astroplant_kit.peripheral import *
from . import environment

class Temperature(Sensor):
    """
    A temperature sensor implementation using the virtual simulated environment.
    """

    def __init__(self, *args, sleep):
        super().__init__(*args)
        self.sleep = int(sleep)

    async def measure(self):
        temperature = environment.Environment.kit_air_temperature + random.uniform(-0.02, 0.02)
        temperature_measurement = Measurement(self, "Temperature", "Degrees Celsius", temperature)

        await asyncio.sleep(self.sleep / 1000)
        return temperature_measurement

class Pressure(Sensor):
    """
    A pressure sensor implementation using the virtual simulated environment.
    """

    def __init__(self, *args, sleep):
        super().__init__(*args)
        self.sleep = int(sleep)

    async def measure(self):
        pressure = environment.Environment.kit_air_pressure + random.uniform(-0.75, 0.75)
        pressure_measurement = Measurement(self, "Pressure", "Hectopascal", pressure)

        await asyncio.sleep(self.sleep / 1000)
        return pressure_measurement

class Barometer(Sensor):
    """
    A barometer sensor implementation using the virtual simulated environment.
    """

    def __init__(self, *args, sleep):
        super().__init__(*args)
        self.sleep = int(sleep)

    async def measure(self):
        temperature = environment.Environment.kit_air_temperature + random.uniform(-0.035, 0.035)
        temperature_measurement = Measurement(self, "Temperature", "Degrees Celsius", temperature)

        humidity = environment.Environment.kit_air_humidity + random.uniform(-0.95, 0.95)
        humidity_measurement = Measurement(self, "Humidity", "Percent", humidity)

        pressure = environment.Environment.kit_air_pressure + random.uniform(-0.95, 0.95)
        pressure_measurement = Measurement(self, "Pressure", "Hectopascal", pressure)

        await asyncio.sleep(self.sleep / 1000)
        return [temperature_measurement, humidity_measurement, pressure_measurement]

