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

        #parameters: 
        self.parallelism_level = int(config["HardwareConfig"]["parallelism_level"])
        #power:
        self.global_memory_write_power = self.total_write_in_global()
        self.global_memory_read_power = self.total_read_in_global()
        self.buffer_memory_write_power = self.total_write_in_buffer()
        self.buffer_memory_read_power = self.total_read_in_buffer()

        #delay
        self.sensing_pixel_array_delay = self._pixel_array.total_delay_in_sensing
        self.sensing_adc_array_delay = self._adc_array.total_delay_in_sensing * self._pixel_array.height

        self.compute_pixel_array_delay = self._pixel_array.total_delay_in_compute
        self.compute_adc_array_delay = (self._adc_array.total_delay_in_compute *  self._network.calculate_output_height(self._pixel_array.height)  * self._network.kernel_number) / self.parallelism_level
        #TODO: memory delays
        self.sensing_delay = self.total_sensing_delay()
        
        self.computing_delay = self._pixel_array.total_delay_in_compute + (self._adc_array.total_delay_in_compute *  self._network.calculate_output_height(self._pixel_array.height)) 
        
    def total_write_in_global(self):
        return self._global_memory.write_power_per_weight * self._network.total_weights
    
    def total_read_in_global(self):
        return self._global_memory.read_power_per_weight * self._network.total_weights
    
    def total_write_in_buffer(self):
        return self._buffer_memory.write_power_per_weight * self._network.total_weights
    
    def total_read_in_buffer(self):
        return self._network.calculate_output_height(self._pixel_array.height) * self._buffer_memory.read_power_per_weight * self._network.total_weights

    def total_sensing_delay(self):
        return self.sensing_pixel_array_delay + self.sensing_adc_array_delay

    def total_compute_delay(self):
        pass

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