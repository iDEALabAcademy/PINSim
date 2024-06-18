from Component import Component
from Network import Network
from Hardware import Hardware
import math

class Controller(Component):
    def __init__(self, component_name, model_key):
        """
        Initialize the Controller with its name and model configuration.
        
        Parameters:
        component_name (str): The name of the Controller component.
        model_key (str): The model key to look up in the configuration.
        """
        # TODO: Check with others
        super().__init__(component_name, model_key)
        self._decoder = Component("Decoder", "decoder_model")  # One decoder component
        
        # Calculate delay in different modes
        self.total_delay_in_normal = self.delay + (self._decoder.total_delay * Hardware.pixel_array_height)
        self.total_delay_in_sensing = self.delay + (self._decoder.total_delay * math.ceil(Hardware.pixel_array_height / Hardware.box_size))
        
        # Calculate power consumption in different modes
        self.total_power_in_normal = self.power + self._decoder.total_power
        self.total_power_in_sensing = self.power + self._decoder.total_power  # TODO: We can use a different size of decoder here
        
        if Network.type == "CNN":
            self.total_delay_in_compute = self.delay + (self._decoder.total_delay * Network.output_feature_map_height)
            self.total_area = self.area + self._decoder.total_area * Network.kernel_height 
            self.total_power_in_compute = self.power + self._decoder.total_power * Network.kernel_height 
        else:
            self.total_delay_in_compute = self.delay  # In MLP, all the pixels are connected to the bus
            self.total_area = self.area + self._decoder.total_area
            self.total_power_in_compute = self.power
            
        # Calculate total delay and power
        self.total_delay = max(self.total_delay_in_normal, self.total_delay_in_sensing, self.total_delay_in_compute) 
        self.total_power = (
            self.total_power_in_normal * Hardware.op_percentage[0] +
            self.total_power_in_sensing * Hardware.op_percentage[1] +
            self.total_power_in_compute * Hardware.op_percentage[2]
        )
        
    def print_detail(self, tab=""):
        """
        Print the details of the Controller component.
        
        Parameters:
        tab (str): The tab character(s) to prepend to each line. Default is an empty string.
        
        Returns:
        str: A string representation of the component details.
        """
        result = ""
        result += super().print_detail(tab)
        tab += '\t'
        result += self._decoder.print_detail(tab)
        return result
