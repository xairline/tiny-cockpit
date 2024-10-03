from layers.base import LayerBase


class STAT1(LayerBase):
    def __init__(self, xp, display):
        super().__init__("STAT1", xp, display)
        self.add_dataref("sim/cockpit2/gauges/indicators/altitude_ft_pilot", freq=20)
        self.add_dataref("sim/flightmodel/position/vh_ind_fpm", freq=20)

    def show(self, values):
        try:
            alt = values["sim/cockpit2/gauges/indicators/altitude_ft_pilot"] / 1000
            vs = values["sim/flightmodel/position/vh_ind_fpm"] / 1000
            title = "STAT1"
            self.display.show(
                title,
                "ALT:   " + f"{alt:.1f}",
                "VS:    " + f"{vs:.1f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
