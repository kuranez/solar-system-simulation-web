""" ephemeris.py

    # Method overview:


"""

from skyfield.api import load
from skyfield.timelib import Time

class EphemerisManager:

    eph = None
    status = "idle"
    error = None

    @classmethod
    def load(cls):

        if cls.eph is not None:
            return cls.eph

        cls.status = "loading"

        try:
            cls.eph = load("de440s.bsp")
            cls.status = "ready"

        except Exception as exc:
            cls.status = "error"
            cls.error = exc
            raise

        return cls.eph

    @classmethod
    def get(cls):

        if cls.eph is None:
            return cls.load()

        return cls.eph