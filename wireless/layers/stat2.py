from layers.base import LayerBase


class STAT2(LayerBase):
    NAME = "STAT2"
    DATAREF_HEADING = "sim/cockpit2/gauges/indicators/heading_electric_deg_mag_pilot"
    DATAREF_AIRSPEED = "sim/flightmodel/position/indicated_airspeed"

    def __init__(self, xp, display):
        super().__init__(self.NAME, xp, display)
        self.add_dataref(self.DATAREF_HEADING, freq=5)
        self.add_dataref(self.DATAREF_AIRSPEED, freq=5)

    def show(self, values):
        try:
            hdg = values[self.DATAREF_HEADING] / 1000
            ias = values[self.DATAREF_AIRSPEED] / 1000
            self.display.show(
                self.NAME,
                "HDG:   " + f"{hdg:.0f}",
                "IAS:    " + f"{ias:.0f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
