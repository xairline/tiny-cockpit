from layers.base import LayerBase


class SPD(LayerBase):
    NAME = "SPD"
    DATAREF_SPEED = "toliss_airbus/pfdoutputs/general/ap_speed_value"

    def __init__(self, xp, display):
        super().__init__(self.NAME, xp, display)
        self.add_dataref(self.DATAREF_SPEED, freq=5)

    def show(self, values):
        try:
            spd = values[self.DATAREF_SPEED] / 1000
            self.display.show(
                self.NAME,
                f"{spd:.0f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
