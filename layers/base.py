class LayerBase:
    def __init__(self, name, xp, display):
        self.name = name
        self.xp = xp
        self.display = display

    def add_dataref(self, dataref, freq=1):
        self.xp.AddDataRef(dataref, freq)

    def show(self, values):
        pass
