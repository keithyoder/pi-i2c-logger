from sensors.sensor import Sensor
from dash_daq import LEDDisplay

class UVRaw(Sensor):
    def __init__(self, device):
        # precision=-1 (via Sensor's default handling of a falsy precision)
        # isn't appropriate here -- raw counts are integers, so precision=0
        # avoids Sensor#value's round() adding a pointless ".0"
        super().__init__(device, "ltr390_uv_raw", "counts", precision=0)

    def value(self):
        try:
            return super().value(self.device.uvs)
        except:
            return None

    def dashboard_gauge(self):
        return LEDDisplay(
            id=self.key,
            label="UV Raw Count",
            value=0
        )