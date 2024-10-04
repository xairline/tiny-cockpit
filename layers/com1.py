from layers.base import LayerBase


class COM1(LayerBase):
    def __init__(self, xp, display):
        super().__init__("COM1", xp, display)
        self.add_dataref("sim/cockpit2/radios/actuators/com1_frequency_hz_833", freq=3)
        self.add_dataref(
            "sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833", freq=3
        )
        self.add_dataref("sim/cockpit2/radios/actuators/com2_frequency_hz_833", freq=3)
        self.add_dataref(
            "sim/cockpit2/radios/actuators/com2_standby_frequency_hz_833", freq=3
        )

    def show(self, values):
        try:
            com1_active = (
                values["sim/cockpit2/radios/actuators/com1_frequency_hz_833"]
                / 1000
                / 1000
            )
            com1_standby = (
                values["sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833"]
                / 1000
                / 1000
            )
            title = "COM 1"
            self.display.show(
                title,
                "ACT:   " + f"{com1_active:.3f}",
                "STBY: " + f"{com1_standby:.3f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
