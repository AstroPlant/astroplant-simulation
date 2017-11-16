import threading
import time
import datetime
import math

SECONDS_PER_HOUR = 60 * 60

class Environment:
    """
    Class to simulate an AstroPlant kit environment.

    Temperature is in degrees celsius.
    Pressure is in hPa.
    Humidity is in percentages.
    """
    _running = False

    #: Simulation sleep between steps in seconds
    _simulation_sleep = 0.1

    #: Simulation time step in seconds
    _dtime = 50 
    
    #: The current date and time
    current_date_time = datetime.datetime(year = 2017, month = 11, day = 16, hour = 8)

    #: Ambient environmental air temperature
    ambient_air_temperature = 20.0

    #: Change in ambient air temperature per second given the date and time
    dambient_air_temperature_dsecond = lambda date_time: math.sin((date_time.hour - 6)  / 24 * math.pi * 2) / 4 / SECONDS_PER_HOUR

    #: Ambient air pressure
    ambient_air_pressure = 1000

    #: Ambient air humidity
    ambient_air_humidity = 35

    #: Kit air temperature
    kit_air_temperature = 20.0

    #: Kit air pressure
    kit_air_pressure = 1000

    #: Kit air humidity
    kit_air_humidity = 35

    @classmethod
    def simulate(clss):
        """
        Simulate the environment.
        """
        while True:
            clss.current_date_time += datetime.timedelta(seconds = clss._dtime)

            clss.simulate_step(clss._dtime)
            time.sleep(clss._simulation_sleep)

    @classmethod
    def simulate_step(clss, dtime):
        """
        Perform a simulation step.
        :param dtime: The simulated time (in seconds) passed since the last simulation step.
        """
        clss.simulate_ambient_factors(dtime)
        clss.simulate_kit(dtime)

    @classmethod
    def simulate_ambient_factors(clss, dtime):
        """
        Simulate ambient environmental factors.
        :param dtime: The simulated time (in seconds) passed since the last simulation step.
        """
        clss.ambient_air_temperature += clss.dambient_air_temperature_dsecond(clss.current_date_time) * dtime

    @classmethod
    def simulate_kit(clss, dtime):
        """
        Simulate factors within the kit.
        :param dtime: The simulated time (in seconds) passed since the last simulation step.
        """
        dkit_air_temperature_dtime = 0

        # Leakage of ambient temperature to kit air temperature
        # (Assume without other forces, equilibrium is restored in two hours)
        dkit_air_temperature_dtime += (clss.ambient_air_temperature - clss.kit_air_temperature) / 2 / SECONDS_PER_HOUR

        clss.kit_air_temperature += dkit_air_temperature_dtime * dtime

        clss.kit_air_pressure = clss.ambient_air_pressure
        clss.kit_air_humidity = clss.ambient_air_humidity

    @classmethod
    def get_dval_dtime_from_list(clss, dval_dtimes):
        """
        Get a dval/dtime value from a list of times-of-day and dval/dtime values.

        :param dval_dtimes: The list with tuples of times-of-day and dval/dtimes.
        :return: The first value in the list such that the time-of-day is greater than the current simulated time.
        """
        current_time = clss.current_date_time.time()

        for time, val in dval_dtimes:
            if time >= current_time:
                return val

        # Return last value otherwise
        return val
            

if not Environment._running:
    Environment._running = True
    thread = threading.Thread(target = Environment.simulate)
    thread.start()
