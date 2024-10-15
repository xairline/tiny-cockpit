from layers.base import LayerBase


class ALT(LayerBase):
    NAME = "ALT"
    DATAREF_ALT = "toliss_airbus/pfdoutputs/general/ap_alt_target_value"

    def __init__(self, xp, display):
        super().__init__(self.NAME, xp, display)
        self.add_dataref(self.DATAREF_ALT, freq=5)

    def show(self, values):
        try:
            alt = values[self.DATAREF_ALT] / 1000
            self.display.show(
                self.NAME,
                f"{alt:.0f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
