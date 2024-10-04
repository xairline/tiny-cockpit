from layers.base import LayerBase


class STAT1(LayerBase):
    def __init__(self, xp, display):
        super().__init__("STAT1", xp, display)
        self.dataref1 = "sim/flightmodel/position/elevation"
        self.dataref2 = "sim/flightmodel/position/vh_ind_fpm"
        self.add_dataref(self.dataref1, freq=3)
        self.add_dataref(self.dataref2, freq=3)

    def show(self, values):
        try:
            alt = values[self.dataref1] / 1000 * 3.28084
            vs = values[self.dataref2] / 1000
            title = "STAT1"
            self.display.show(
                title,
                "ALT:   " + f"{alt:.0f}",
                "VS:      " + f"{vs:.0f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
