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

        self._buffer_memory = Buffer.Buffer("Buffer", "buffer_model") #in MLP all the parameters are zero
        #TODO: add controller here
        self._controller = Controller("ControlUnit", "decoder_model")

        if Hardware.weight_precision > self._global_memory.bus_size or (Network.type == "CNN" and Hardware.weight_precision > self._buffer_memory.bus_size):
            raise ValueError( "The bus size should be greater than weight precision")

        #delay
        self.total_normal_delay = self._pixel_array.total_delay_in_normal + self._adc_array.total_delay_in_normal
        self.total_sensing_delay = self._pixel_array.total_delay_in_sensing + self._adc_array.total_delay_in_sensing
        self.computing_delay = self._pixel_array.total_delay_in_compute  + self._adc_array.total_delay_in_compute + self._global_memory.total_read_delay + self._buffer_memory.total_write_delay + self._buffer_memory.total_read_delay #TODO: we can add global write here
        self.total_delay = max(self.total_normal_delay, self.total_sensing_delay,  self.computing_delay)

        #power
        self.total_power = self._pixel_array.total_power + self._adc_array.total_power + self._global_memory.total_write_power +  self._global_memory.total_read_power + self._global_memory.total_power + self._buffer_memory.total_write_power + self._buffer_memory.total_read_power + self._buffer_memory.total_power

        #system area
        self.total_area = self.area + self._pixel_array.total_area + self._adc_array.total_area + self._global_memory.total_area + self._buffer_memory.total_area


        #Framrate:
        self.FPS_normal = 1/self.total_normal_delay
        self.FPS_sensing = 1/self.total_sensing_delay
        self.FPS_computing = 1/self.computing_delay
        #TODO: Add TOpS

    def print_detail(self, tab = ""):
        result = ""
        result += super().print_detail()
        tab = '\t'
        result += self._pixel_array.print_detail(tab)
        result += self._adc_array.print_detail(tab)
        result += self._global_memory.print_detail(tab)
        result += self._controller.print_detail(tab)
        if Network.type == "CNN":
            result += self._buffer_memory.print_detail(tab)
        result += Network.print_detail(tab)
        return result