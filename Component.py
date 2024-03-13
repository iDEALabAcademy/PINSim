import Sizing

class Component:
    def __init__(self, name, model, config, sub_component=None):
        self.name = name
        self.model = int(config["HardwareConfig"][model])
        self._sizing =  Sizing.Sizing(config)
        self._sub_component = sub_component
        self.power = self._sizing.calculate_power(float(config[name]["power"].split(',')[self.model].strip()))
        self.delay = self._sizing.calculate_delay(float(config[name]["delay"].split(',')[self.model].strip()))
        self.area = self._sizing.calculate_area(float(config[name]["area"].split(',')[self.model].strip()))
        self.total_power = self.power
        self.total_delay = self.delay
        self.total_area = self.area

    def set_power(name, model):
        pass

    def set_delay(name, model):
        pass
    
    def set_area(name, model):
        pass
    
    def get_power(self):
        return self.total_power

    def get_delay(self):
        return self.total_delay

    def get_area(self):
        return self.total_area
    
    def print_detail(self, tab = ""):
        tab += "\t"
        result = ""
        result += ('****************************\n')
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                 result += tab + f"{attr} = {value}\n"
        return result


