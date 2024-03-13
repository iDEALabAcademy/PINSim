import Component

class GlobalCell(Component.Component):
    def __init__(self, name, model, config, sub_component=None):
        # the standby power is in self.power
        super().__init__(name, model, config, sub_component)
        #TODO: are the memories follow the formulla?
        self.read_power = self._sizing.calculate_power(float(config[name]["read_power"].split(',')[self.model].strip()))
        self.write_power = self._sizing.calculate_power(float(config[name]["write_power"].split(',')[self.model].strip()))
        self.read_delay = self._sizing.calculate_delay(float(config[name]["read_delay"].split(',')[self.model].strip()))
        self.write_delay = self._sizing.calculate_delay(float(config[name]["write_delay"].split(',')[self.model].strip()))