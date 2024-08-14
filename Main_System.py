from Component import Component
import Adc_array
import Pixel_array
import Global
import Buffer
from Controller import Controller
from Network import Network
from Hardware import Hardware
import math

class Main_System(Component):
    def __init__(self, component_name, model_key):
        """
        Initialize the Main_System with its name and model configuration.
        
        Parameters:
        component_name (str): The name of the Main_System component.
        model_key (str): The model key to look up in the configuration.
        """
        super().__init__(component_name, model_key)
        
        # Create the network
        Network.initialize()
        
        # Create the pixel array
        self._pixel_array = Pixel_array.PixelArray("PixelArray", "pixel_array_model")
        
        # Create the ADC array
        self._adc_array = Adc_array.AdcArray("AdcArray", "adc_array_model")
        
        # Create the global memory
        self._global_memory = Global.Global("Global", "global_model")
        
        # Create the buffer memory (in MLP all the parameters are zero)
        self._buffer_memory = Buffer.Buffer("Buffer", "buffer_model")
        
        # TODO: Check with others
        self._controller = Controller("ControlUnit", "decoder_model")

        if Hardware.weight_precision > self._global_memory.bus_size or (Network.type == "CNN" and Hardware.weight_precision > self._buffer_memory.bus_size):
            raise ValueError("The bus size should be greater than weight precision")

        # Calculate delays
        self.total_normal_delay = self._pixel_array.total_delay_in_normal + self._adc_array.total_delay_in_normal + self._controller.total_delay_in_normal
        self.total_sensing_delay = self._pixel_array.total_delay_in_sensing + self._adc_array.total_delay_in_sensing + self._controller.total_delay_in_sensing
        
        # Add clock to the delay
        self.computing_delay = (
            self._pixel_array.total_delay_in_compute +
            self._adc_array.total_delay_in_compute +
            self._global_memory.total_read_delay +
            self._buffer_memory.total_write_delay +
            self._buffer_memory.total_read_delay +
            self._controller.total_delay_in_compute
        )
        self.total_delay = self.delay + max(self.total_normal_delay, self.total_sensing_delay, self.computing_delay)



        self.total_power_in_sensing = self.power + self._pixel_array.total_power_in_sensing + self._adc_array.total_power_in_sensing + self._controller.total_power_in_sensing + self._global_memory.total_power + self._buffer_memory.total_power
        self.total_power_in_normal = self.power + self._pixel_array.total_power_in_normal + self._adc_array.total_power_in_normal + self._controller.total_power_in_normal + self._global_memory.total_power + self._buffer_memory.total_power
        self.total_power_in_compute =  self.power + self._pixel_array.total_power_in_compute + self._adc_array.total_power_in_compute + self._controller.total_power_in_compute + self._global_memory.total_read_power + self._buffer_memory.total_write_power + self._buffer_memory.total_read_power + self._global_memory.total_power + self._buffer_memory.total_power
        
        # Calculate power
        self.total_power = (
            self.power +
            self._pixel_array.total_power +
            self._adc_array.total_power +
            (Hardware.op_percentage[2] / 100.0 * self._global_memory.total_read_power) +
            self._global_memory.total_power +
            (Hardware.op_percentage[2] / 100.0 * self._buffer_memory.total_write_power) +
            (Hardware.op_percentage[2] / 100.0 * self._buffer_memory.total_read_power) +
            self._buffer_memory.total_power +
            self._controller.total_power
        )

        # Calculate system area
        self.total_area = (
            self.area +
            self._pixel_array.total_area +
            self._adc_array.total_area +
            self._global_memory.total_area +
            self._buffer_memory.total_area +
            self._controller.total_area
        )

        # Calculate frame rate
        self.FPS_normal = 1 / self.total_normal_delay
        self.FPS_sensing = 1 / self.total_sensing_delay
        self.FPS_computing = 1 / self.computing_delay
        
        # TODO: Add TOpS calculation

    def print_detail(self, tab=""):
        """
        Print the details of the Main_System component.
        
        Parameters:
        tab (str): The tab character(s) to prepend to each line. Default is an empty string.
        
        Returns:
        str: A string representation of the component details.
        """
        result = ""
        result += super().print_detail(tab)
        tab = '\t'
        result += self._pixel_array.print_detail(tab)
        result += self._adc_array.print_detail(tab)
        result += self._global_memory.print_detail(tab)
        result += self._controller.print_detail(tab)
        if Network.type == "CNN":
            result += self._buffer_memory.print_detail(tab)
        result += Network.print_detail(tab)
        return result
