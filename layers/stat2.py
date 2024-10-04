from layers.base import LayerBase


class STAT2(LayerBase):
    def __init__(self, xp, display):
        super().__init__("STAT2", xp, display)
        self.add_dataref(
            "sim/cockpit2/gauges/indicators/heading_electric_deg_mag_pilot", freq=3
        )
        self.add_dataref("sim/flightmodel/position/indicated_airspeed", freq=3)

    def show(self, values):
        try:
            hdg = (
                values["sim/cockpit2/gauges/indicators/heading_electric_deg_mag_pilot"]
                / 1000
            )
            ias = values["sim/flightmodel/position/indicated_airspeed"] / 1000
            title = "STAT2"
            self.display.show(
                title,
                "HDG:   " + f"{hdg:.0f}",
                "IAS:    " + f"{ias:.0f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
