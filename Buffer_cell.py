import Component
from Config import Config
from Sizing import Sizing

class BufferCell(Component.Component):
    def __init__(self, component_name, model_key):
        """
        Initialize the BufferCell with its name and model configuration.
        
        Parameters:
        component_name (str): The name of the BufferCell component.
        model_key (str): The model key to look up in the configuration.
        """
        # The standby power is in self.power
        super().__init__(component_name, model_key)
        
        # TODO: Verify if the memories follow the formula
        self.read_power = Sizing.calculate_power(
            float(Config.config[component_name]["read_power"].split(',')[self.model_index].strip())
        )
        self.write_power = Sizing.calculate_power(
            float(Config.config[component_name]["write_power"].split(',')[self.model_index].strip())
        )
        self.read_delay = Sizing.calculate_delay(
            float(Config.config[component_name]["read_delay"].split(',')[self.model_index].strip())
        )
        self.write_delay = Sizing.calculate_delay(
            float(Config.config[component_name]["write_delay"].split(',')[self.model_index].strip())
        )
