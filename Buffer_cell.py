import Component

class BufferCell(Component.Component):
    def __init__(self, name, model, config, sub_component=None):
        super().__init__(name, model, config, sub_component)
        self.read_power = float(config[name]["read_power"].split(',')[self.model].strip())
        self.write_power = float(config[name]["write_power"].split(',')[self.model].strip())
        self.read_delay = float(config[name]["read_delay"].split(',')[self.model].strip())
        self.write_delay = float(config[name]["write_delay"].split(',')[self.model].strip())
        