import Component
from Config import Config
from Sizing import Sizing
class BufferCell(Component.Component):
    def __init__(self, name, model):
        # the standby power is in self.power
        super().__init__(name, model)
        #TODO: are the memories follow the formulla?
        self.read_power = Sizing.calculate_power(float(Config.config[name]["read_power"].split(',')[self.model].strip()))
        self.write_power = Sizing.calculate_power(float(Config.config[name]["write_power"].split(',')[self.model].strip()))
        self.read_delay = Sizing.calculate_delay(float(Config.config[name]["read_delay"].split(',')[self.model].strip()))
        self.write_delay = Sizing.calculate_delay(float(Config.config[name]["write_delay"].split(',')[self.model].strip()))
        