import Component
import Adc_array
import Pixel_array
import Global
import Buffer
import Network
import math

class Main_System(Component.Component):

    def __init__(self, name, model, config, sub_component=None):
        super().__init__(name, model, config, sub_component)
        #Create the pixel array
        self._pixel_array = Pixel_array.PixelArray("PixelArray", "pixel_array_model", config)
        #create the readout
        self._adc_array = Adc_array.AdcArray("AdcArray", "adc_array_model", config)
        #Create the Global memory
        self._global_memory = Global.Global("Global", "global_model", config)
        #Create the Buffer memory
        self._buffer_memory = Buffer.Buffer("Buffer", "buffer_model", config)
        #Create the network
        self._network = Network.Network(config)


        #power:
        self.global_memory_write_power = self.total_write_in_global()
        self.global_memory_read_power = self.total_read_in_global()
        self.buffer_memory_write_power = self.total_write_in_buffer()
        self.buffer_memory_read_power = self.total_read_in_buffer()


        
    def total_write_in_global(self):
        return self._global_memory.write_power_per_weight * self._network.total_weights
    
    def total_read_in_global(self):
        return self._global_memory.read_power_per_weight * self._network.total_weights
    
    def total_write_in_buffer(self):
        return self._buffer_memory.write_power_per_weight * self._network.total_weights
    
    def total_read_in_buffer(self):
        return self._network.calculate_output_height(self._pixel_array.height) * self._buffer_memory.read_power_per_weight * self._network.total_weights

    def print_detail(self, tab = ""):
        result = ""
        result += super().print_detail()
        tab = '\t'
        result += self._pixel_array.print_detail(tab)
        result += self._adc_array.print_detail(tab)
        result += self._global_memory.print_detail(tab)
        result += self._buffer_memory.print_detail(tab)
        result += self._network.print_detail(tab)
        return result