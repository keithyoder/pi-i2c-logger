import time
from datetime import datetime, UTC
import logging

from devices.device import Device
from sensors.bmp581.temperature import Temperature
from sensors.bmp581.pressure import Pressure

class BMP581(Device):
    FORCED_MODE_DELAY_SECONDS = 0.15

    def __init__(self, sea_level_pressure_hpa=1013.25):
        super().__init__("BMP581")
        try:
            import adafruit_bmp5xx
            import board
            self.device = adafruit_bmp5xx.BMP5XX_I2C(board.I2C())
            self.device.sea_level_pressure = sea_level_pressure_hpa
            self._mode_module = adafruit_bmp5xx
        except:
            self.device = None
            self._mode_module = None
        self.sensors = [
            Temperature(self.device),
            Pressure(self.device)
        ]
        self.values = {}

    def is_connected(self):
        if self.device is None:
            return False

        # NORMAL mode's autonomous conversion cycle doesn't reliably
        # produce data on this sensor (confirmed via console: data_ready
        # stayed False indefinitely regardless of ODR/OSR). FORCED mode
        # works reliably instead -- trigger one conversion per read cycle
        # and give it a moment to actually complete before checking.
        self.device.mode = self._mode_module.BMP5XX_POWERMODE_FORCED
        time.sleep(self.FORCED_MODE_DELAY_SECONDS)
        ready = self.device.data_ready
        if not ready:
            logging.warning(f"[BMP581] data_ready=False after forced trigger at {datetime.now(UTC)}")
        return ready