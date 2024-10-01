from layers.base import LayerBase


class COM2(LayerBase):
    def __init__(self, xp, display):
        super().__init__("COM2", xp, display)
        self.add_dataref("sim/cockpit2/radios/actuators/com2_frequency_hz_833", freq=20)
        self.add_dataref(
            "sim/cockpit2/radios/actuators/com2_standby_frequency_hz_833", freq=20
        )
        self.add_dataref("sim/cockpit2/radios/actuators/com2_frequency_hz_833", freq=20)
        self.add_dataref(
            "sim/cockpit2/radios/actuators/com2_standby_frequency_hz_833", freq=20
        )

    def show(self, values):
        try:
            com2_active = (
                values["sim/cockpit2/radios/actuators/com2_frequency_hz_833"]
                / 1000
                / 1000
            )
            com2_standby = (
                values["sim/cockpit2/radios/actuators/com2_standby_frequency_hz_833"]
                / 1000
                / 1000
            )
            title = "COM 2"
            self.display.show(
                title,
                "ACT:   " + f"{com2_active:.3f}",
                "STBY: " + f"{com2_standby:.3f}",
            )
        except Exception as e:
            print(f"Error: {e}")
            pass
