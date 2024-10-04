from layers.base import LayerBase


class COM1(LayerBase):
    NAME = "COM1"
    TITLE = "COM 1"
    COM1_FREQ_REF = "sim/cockpit2/radios/actuators/com1_frequency_hz_833"
    COM1_STBY_FREQ_REF = "sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833"
    COM2_FREQ_REF = "sim/cockpit2/radios/actuators/com2_frequency_hz_833"
    COM2_STBY_FREQ_REF = "sim/cockpit2/radios/actuators/com2_standby_frequency_hz_833"

    def __init__(self, xp, display):
        super().__init__(self.NAME, xp, display)
        self.add_dataref(self.COM1_FREQ_REF, freq=5)
        self.add_dataref(self.COM1_STBY_FREQ_REF, freq=5)
        self.add_dataref(self.COM2_FREQ_REF, freq=5)
        self.add_dataref(self.COM2_STBY_FREQ_REF, freq=5)

    def show(self, values):
        try:
            com1_active = values[self.COM1_FREQ_REF] / 1_000_000
            com1_standby = values[self.COM1_STBY_FREQ_REF] / 1_000_000
            self.display.show(
                self.TITLE,
                "ACT:   " + f"{com1_active:.3f}",
                "STBY: " + f"{com1_standby:.3f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
