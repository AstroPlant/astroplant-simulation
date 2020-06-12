"""
Temperature is in degrees celsius.
Pressure is in hPa.
Specific humidity is kg moisture per kg air.
Relative humidity is a fraction of total possible humidity.
"""

import threading
import time
import datetime
import math

SECONDS_PER_HOUR = 60 * 60

KIT_VOLUME = 0.5 * 1.0 * 2.0  # m^3
KIT_AIR_MASS = 1.293 * KIT_VOLUME  # kg

AIR_SPECIFIC_HEAT = 1000.0  # J/kg


def dew_point(air_temperature):
    """Rough calculation for dew point in specific humidity (kg moisture per kg air).
    Based on doubling of dew point per 10 degrees celsius, and a dew point of 0.051kg at 40 degrees celsius."""
    return 0.051 * 2 ** ((air_temperature - 40.0) / 10.0)


def relative_humidity(specific_humidity, air_temperature):
    return specific_humidity / dew_point(air_temperature)


class Environment:
    """
    Class to simulate a controlled environment.
    """

    def __init__(self):
        self._running = False

        #: Simulation sleep between steps in seconds
        self._simulation_sleep = 0.1
        #: Simulation time step in seconds
        self._dtime = 0.1

        self.current_date_time = datetime.datetime(year=2017, month=11, day=16, hour=8)

        self.ambient_air_temperature = 20.0
        #: Change in ambient air temperature per second given the date and time
        self.dambient_air_temperature_dsecond = (
            lambda date_time: math.sin((date_time.hour - 6) / 24 * math.pi * 2)
            / 4
            / SECONDS_PER_HOUR
        )

        self.ambient_air_pressure = 1000.0
        self.ambient_air_specific_humidity = 0.006

        self.kit_air_temperature = 24.0
        self.kit_air_pressure = 1000.0
        self.kit_air_specific_humidity = 0.008

        self.kit_heating = {}

    def simulate(self):
        """
        Simulate the environment.
        """
        while self._running:
            self.current_date_time += datetime.timedelta(seconds=self._dtime)

            self.simulate_step(self._dtime)
            time.sleep(self._simulation_sleep)

    def simulate_step(self, dtime):
        """
        Perform a simulation step.
        :param dtime: The simulated time (in seconds) passed since the last simulation step.
        """
        self.simulate_ambient_factors(dtime)
        self.simulate_kit(dtime)

    def simulate_ambient_factors(self, dtime):
        """
        Simulate ambient environmental factors.
        :param dtime: The simulated time (in seconds) passed since the last simulation step.
        """
        self.ambient_air_temperature += (
            self.dambient_air_temperature_dsecond(self.current_date_time) * dtime
        )

    def set_kit_heating(self, name, wattage):
        self.kit_heating[name] = wattage

    def simulate_kit(self, dtime):
        """
        Simulate factors within the kit.
        :param dtime: The simulated time (in seconds) passed since the last simulation step.
        """
        dkit_air_temperature_dtime = 0

        # Leakage of ambient temperature to kit air temperature
        # (Assume without other forces, equilibrium is restored in two hours)
        dkit_air_temperature_dtime += (
            (self.ambient_air_temperature - self.kit_air_temperature)
            / 2
            / SECONDS_PER_HOUR
        )

        for wattage in self.kit_heating.values():
            dkit_air_temperature_dtime += wattage / (KIT_AIR_MASS * AIR_SPECIFIC_HEAT)

        self.kit_air_temperature += dkit_air_temperature_dtime * dtime

        if self.ambient_air_specific_humidity > dew_point(self.ambient_air_temperature):
            self.ambient_air_specific_humidity = dew_point(self.ambient_air_temperature)

        self.kit_air_pressure = self.ambient_air_pressure
        self.kit_air_specific_humidity = self.ambient_air_specific_humidity

    @property
    def kit_air_humidity(self):
        return relative_humidity(
            self.kit_air_specific_humidity, self.kit_air_temperature
        )

    def get_dval_dtime_from_list(self, dval_dtimes):
        """
        Get a dval/dtime value from a list of times-of-day and dval/dtime values.

        :param dval_dtimes: The list with tuples of times-of-day and dval/dtimes.
        :return: The first value in the list such that the time-of-day is greater than the current simulated time.
        """
        current_time = self.current_date_time.time()

        for time, val in dval_dtimes:
            if time >= current_time:
                return val

        # Return last value otherwise
        return val


environment = Environment()

# for backwards compatibility:
Environment = environment

if not environment._running:
    environment._running = True
    thread = threading.Thread(target=environment.simulate)
    thread.daemon = True
    thread.start()
