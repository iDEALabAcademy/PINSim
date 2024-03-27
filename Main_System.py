import Component
import Adc_array
import Pixel_array
import Global
import Buffer
from Network import Network
from Hardware import Hardware
import math

class Main_System(Component.Component):

    def __init__(self, name, model):
        super().__init__(name, model)
        #Create the network
        Network.initialize()
        #Create the pixel array
        self._pixel_array = Pixel_array.PixelArray("PixelArray", "pixel_array_model")
        #create the readout
        self._adc_array = Adc_array.AdcArray("AdcArray", "adc_array_model")
        #Create the Global memory
        self._global_memory = Global.Global("Global", "global_model")
        if Network.type == "CNN":
            #Create the Buffer memory
            self._buffer_memory = Buffer.Buffer("Buffer", "buffer_model")
        #TODO: add controller here


        if Hardware.weight_precision > self._global_memory.bus_size or (Network.type == "CNN" and Hardware.weight_precision > self._buffer_memory.bus_size):
            #TODO: raise an error
            print( "The bus size should be greater than weight precision")
            
        #power:
        self.global_memory_write_power = self._global_memory.write_power_per_weight * Network.total_weights
        self.global_memory_read_power = self._global_memory.read_power_per_weight * Network.total_weights
        if Network.type == "CNN":
            self.buffer_memory_write_power = self._buffer_memory.write_power_per_weight * Network.total_weights
            self.buffer_memory_read_power = Network.calculate_output_height(self._pixel_array.height) * self._buffer_memory.read_power_per_weight * Network.total_weights
        self.pixel_array_power = self._pixel_array.total_power
        self.adc_power = self._adc_array.total_power
        
        if Network.type == "CNN":
            # self.buffer_memory_write_power = self._buffer_memory.write_power_per_weight * Network.total_weights
            # self.buffer_memory_read_power = Network.calculate_output_height(self._pixel_array.height) * self._buffer_memory.read_power_per_weight * Network.total_weights
            self.total_power = self.pixel_array_power + self.adc_power + self.global_memory_write_power +  self.global_memory_read_power + self._global_memory.total_power + self.buffer_memory_write_power + self.buffer_memory_read_power + self._buffer_memory.total_power
        else:
            self.total_power = self.pixel_array_power + self.adc_power + self.global_memory_write_power +  self.global_memory_read_power + self._global_memory.total_power

        
        #delay
        #pixel array
        self.sensing_pixel_array_delay = self._pixel_array.total_delay_in_sensing
        self.compute_pixel_array_delay = self._pixel_array.total_delay_in_compute 
        #ADC array for whole network
        self.sensing_adc_array_delay = self._adc_array.total_delay_in_sensing * math.ceil(self._pixel_array.height/float(self._pixel_array.box_size))
        if Network.type == "CNN":
            self.compute_adc_array_delay = (self._adc_array.total_delay_in_compute * Network.calculate_output_height(self._pixel_array.height)  * Network.kernel_number) / Hardware.parallelism_level
        else:
            self.compute_adc_array_delay = self._adc_array.total_delay_in_compute * (Network.hidden_node/Hardware.parallelism_level)
        #memory delays
        self.global_memory_write_delay = self._global_memory.write_delay_per_weight * Network.total_weights
        self.global_memory_read_delay = self._global_memory.read_delay_per_weight * Network.total_weights
        
        if Network.type == "CNN":
            self.buffer_memory_write_delay = self._global_memory.write_delay_per_weight * Network.total_weights
            self.buffer_memory_read_delay = self._global_memory.read_delay_per_weight * Network.total_weights * Network.calculate_output_height(self._pixel_array.height)

        #system delay
        self.sensing_delay = self.sensing_pixel_array_delay + self.sensing_adc_array_delay
        if Network.type == "CNN":
            self.computing_delay = self.compute_pixel_array_delay + self.compute_adc_array_delay + self.global_memory_read_delay + self.buffer_memory_write_delay + self.buffer_memory_read_delay #TODO: we can add global write here
        else:
            self.computing_delay = self.compute_pixel_array_delay + self.compute_adc_array_delay + self.global_memory_read_delay
        self.total_delay = max(self.sensing_delay,  self.computing_delay)
        #system area
        if Network.type == "CNN":
            self.total_area = self.area + self._adc_array.total_area + self._adc_array.total_area + self._global_memory.total_area + self._buffer_memory.total_area
        else:
            self.total_area = self.area + self._adc_array.total_area + self._adc_array.total_area + self._global_memory.total_area 

        #Framrate:
        self.FPS_sensing = 1/self.sensing_delay
        self.FPS_computing = 1/self.computing_delay
        

    def print_detail(self, tab = ""):
        result = ""
        result += super().print_detail()
        tab = '\t'
        result += self._pixel_array.print_detail(tab)
        result += self._adc_array.print_detail(tab)
        result += self._global_memory.print_detail(tab)
        if Network.type == "CNN":
            result += self._buffer_memory.print_detail(tab)
        result += Network.print_detail(tab)
        return result