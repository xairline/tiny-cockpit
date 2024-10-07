from layers.base import LayerBase


class STAT1(LayerBase):
    NAME = "STAT1"
    DATAREF_ELEVATION = "sim/flightmodel/position/elevation"
    DATAREF_VSPEED = "sim/flightmodel/position/vh_ind_fpm"

    def __init__(self, xp, display):
        super().__init__(self.NAME, xp, display)
        self.add_dataref(self.DATAREF_ELEVATION, freq=5)
        self.add_dataref(self.DATAREF_VSPEED, freq=5)

    def show(self, values):
        try:
            alt = values[self.DATAREF_ELEVATION] / 1000 * 3.28084
            vs = values[self.DATAREF_VSPEED] / 1000
            self.display.show(
                self.NAME,
                "ALT:   " + f"{alt:.0f}",
                "VS:      " + f"{vs:.0f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass