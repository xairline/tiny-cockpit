from layers.base import LayerBase


class STAT2(LayerBase):
    def __init__(self, xp, display):
        super().__init__("STAT2", xp, display)
        self.add_dataref(
            "sim/cockpit2/gauges/indicators/heading_electric_deg_mag_pilot", freq=20
        )
        self.add_dataref("sim/cockpit2/gauges/indicators/airspeed_kts_pilot", freq=20)

    def show(self, values):
        try:
            hdg = (
                values["sim/cockpit2/gauges/indicators/heading_electric_deg_mag_pilot"]
                / 1000
            )
            ias = values["sim/cockpit2/gauges/indicators/airspeed_kts_pilot"] / 1000
            title = "STAT2"
            self.display.show(
                title,
                "HDG:   " + f"{hdg:.1f}",
                "IAS:    " + f"{ias:.1f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
