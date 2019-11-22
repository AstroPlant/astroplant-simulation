import trio
import random
from astroplant_kit.peripheral import *
from . import environment


class Temperature(Sensor):
    """
    A temperature sensor implementation using the virtual simulated environment.
    """

    def __init__(self, *args, configuration):
        super().__init__(*args)
        self.measurement_interval = configuration["intervals"]["measurementInterval"]
        self.aggregate_interval = configuration["intervals"]["aggregateInterval"]

    async def measure(self):
        temperature = environment.Environment.kit_air_temperature + random.uniform(
            -0.02, 0.02
        )
        temperature_measurement = self.create_raw_measurement(
            "Temperature", "Degrees Celsius", temperature
        )

        return temperature_measurement


class Pressure(Sensor):
    """
    A pressure sensor implementation using the virtual simulated environment.
    """

    def __init__(self, *args, configuration):
        super().__init__(*args)
        self.measurement_interval = configuration["intervals"]["measurementInterval"]
        self.aggregate_interval = configuration["intervals"]["aggregateInterval"]

    async def measure(self):
        pressure = environment.Environment.kit_air_pressure + random.uniform(
            -0.75, 0.75
        )
        pressure_measurement = self.create_raw_measurement(
            "Pressure", "Hectopascal", pressure
        )

        return pressure_measurement


class Barometer(Sensor):
    """
    A barometer sensor implementation using the virtual simulated environment.
    """

    def __init__(self, *args, configuration):
        super().__init__(*args)
        self.measurement_interval = configuration["intervals"]["measurementInterval"]
        self.aggregate_interval = configuration["intervals"]["aggregateInterval"]

    async def measure(self):
        temperature = environment.Environment.kit_air_temperature + random.uniform(
            -0.035, 0.035
        )
        temperature_measurement = self.create_raw_measurement(
            "Temperature", "Degrees Celsius", temperature
        )

        humidity = environment.Environment.kit_air_humidity + random.uniform(
            -0.95, 0.95
        )
        humidity_measurement = self.create_raw_measurement(
            "Humidity", "Percent", humidity
        )

        pressure = environment.Environment.kit_air_pressure + random.uniform(
            -0.95, 0.95
        )
        pressure_measurement = self.create_raw_measurement(
            "Pressure", "Hectopascal", pressure
        )

        return [temperature_measurement, humidity_measurement, pressure_measurement]
