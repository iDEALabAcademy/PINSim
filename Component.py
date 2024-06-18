from Config import Config
from Sizing import Sizing

class Component:
    def __init__(self, component_name, model_key):
        """
        Initialize the Component with its name and model configuration.
        
        Parameters:
        component_name (str): The name of the component.
        model_key (str): The model key to look up in the configuration.
        """
        self.component_name = component_name
        self.model_index = int(Config.config["HardwareConfig"][model_key])
        
        # Fetch power, delay, and area from configuration and calculate their values
        self.power = Sizing.calculate_power(
            float(Config.config[component_name]["power"].split(',')[self.model_index].strip())
        )
        self.delay = Sizing.calculate_delay(
            float(Config.config[component_name]["delay"].split(',')[self.model_index].strip())
        )
        self.area = Sizing.calculate_area(
            float(Config.config[component_name]["area"].split(',')[self.model_index].strip())
        )
        
        # Initialize total power, delay, and area with calculated values
        self.total_power = self.power
        self.total_delay = self.delay
        self.total_area = self.area

    def set_power(self, component_name, model_key):
        """
        Set the power attribute for the component.
        
        Parameters:
        component_name (str): The name of the component.
        model_key (str): The model key to look up in the configuration.
        """
        self.model_index = int(Config.config["HardwareConfig"][model_key])
        self.power = Sizing.calculate_power(
            float(Config.config[component_name]["power"].split(',')[self.model_index].strip())
        )
        self.total_power = self.power

    def set_delay(self, component_name, model_key):
        """
        Set the delay attribute for the component.
        
        Parameters:
        component_name (str): The name of the component.
        model_key (str): The model key to look up in the configuration.
        """
        self.model_index = int(Config.config["HardwareConfig"][model_key])
        self.delay = Sizing.calculate_delay(
            float(Config.config[component_name]["delay"].split(',')[self.model_index].strip())
        )
        self.total_delay = self.delay
    
    def set_area(self, component_name, model_key):
        """
        Set the area attribute for the component.
        
        Parameters:
        component_name (str): The name of the component.
        model_key (str): The model key to look up in the configuration.
        """
        self.model_index = int(Config.config["HardwareConfig"][model_key])
        self.area = Sizing.calculate_area(
            float(Config.config[component_name]["area"].split(',')[self.model_index].strip())
        )
        self.total_area = self.area
    
    def get_power(self):
        """
        Get the total power of the component.
        
        Returns:
        float: The total power.
        """
        return self.total_power

    def get_delay(self):
        """
        Get the total delay of the component.
        
        Returns:
        float: The total delay.
        """
        return self.total_delay

    def get_area(self):
        """
        Get the total area of the component.
        
        Returns:
        float: The total area.
        """
        return self.total_area
    
    def print_detail(self, tab=""):
        """
        Print the details of the component.
        
        Parameters:
        tab (str): The tab character(s) to prepend to each line. Default is an empty string.
        
        Returns:
        str: A string representation of the component details.
        """
        tab += "\t"
        result = "****************************\n"
        for attribute, value in self.__dict__.items():
            if not attribute.startswith('_'):
                if isinstance(value, float):
                    # Format float in scientific notation with three decimal places
                    formatted_value = f"{value:.3e}"  
                    result += f"{tab}{attribute} = {formatted_value}\n"
                else:
                    result += f"{tab}{attribute} = {value}\n"
        return result
