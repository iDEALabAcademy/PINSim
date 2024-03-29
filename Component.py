from Config import Config
from Sizing import Sizing

class Component:
    def __init__(self, name, model):
        self.name = name
        self.model = int(Config.config["HardwareConfig"][model])
        self.power = Sizing.calculate_power(float(Config.config[name]["power"].split(',')[self.model].strip()))
        self.delay = Sizing.calculate_delay(float(Config.config[name]["delay"].split(',')[self.model].strip()))
        self.area = Sizing.calculate_area(float(Config.config[name]["area"].split(',')[self.model].strip()))
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
    
    def print_detail(self, tab=""):
        tab += "\t"
        result = ""
        result += ('****************************\n')
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                if isinstance(value, float):  # Check if the value is a float
                    # Format float in scientific notation with three decimal places
                    formatted_value = f"{value:.3e}"  
                    result += tab + f"{attr} = {formatted_value}\n"
                else:
                    result += tab + f"{attr} = {value}\n"
        return result



