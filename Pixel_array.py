import Component
import Network
import math
import Sizing
from Hardware import Hardware
from Network import Network

class PixelArray(Component.Component):

    def __init__(self, name, model):
        super().__init__(name, model)
        self._pixel = Component.Component("Pixel", "pixel_model")# one _pixel model
        self._sizing = Sizing.Sizing() 
        self._cp_pixel = Component.Component("PixelComputeAddon", "pixel_cp_model")# one compute addon model for in _pixel
        self.width = Hardware.pixel_array_width
        self.height = Hardware.pixel_array_height
        self.is_cp_in_pixel = Hardware.cp_in_pixel
        self.cp_per_pixel =Hardware.cp_per_pixel
        self._cp_percentage = Hardware.cp_percentage
        self.box_size = Hardware.box_size

        self.outfmap = Network.calculate_output_height(self.height)
        self.total_pixels = self.width * self.height
        self.active_pixels = math.ceil(self.width/float(self.box_size)) * math.ceil(self.height/float(self.box_size))
        self.total_power_in_compute = self.power + self.power_pixel_compute_addon() + self.power_pixels()
        self.total_power_in_sensing = self.power + (self._pixel.get_power() * self.active_pixels) #assume in the sensing mode only central pixels are On.
        self.total_power = ((self.total_power_in_compute * self._cp_percentage) + (self.total_power_in_sensing * ( 100 - self._cp_percentage)))/100.0
        # TODO: check total_delay_in_compute self.outfmap
        self.total_delay_in_compute = self.delay + (self.delay_pixel_compute_addon() + self.delay_pixels()) * self.outfmap
        self.total_delay_in_sensing = self.delay + self.delay_pixels() * math.ceil(self.height/float(self.box_size))

        # self.kernel_delay_in_compute = self.delay + (self.delay_pixel_compute_addon() + self.delay_pixels()) * self.outfmap
        self.row_delay_in_sensing = self.delay + self.delay_pixels()
        
        self.total_delay = max(self.total_delay_in_compute, self.total_delay_in_sensing)
        self.total_area = self.area + self.area_pixel_compute_addon() + self.area_pixels()

    def power_pixel_compute_addon(self):
        return self.is_cp_in_pixel * self.total_pixels * self._cp_pixel.get_power() * self.cp_per_pixel

    def delay_pixel_compute_addon(self):
        return self.is_cp_in_pixel * self._cp_pixel.get_delay()

    def area_pixel_compute_addon(self):
        return self.is_cp_in_pixel * self.total_pixels * self._cp_pixel.get_area() * self.cp_per_pixel

    def power_pixels(self):
       return self.total_pixels * self._pixel.get_power()

    def delay_pixels(self):
        return self._pixel.get_delay()

    def area_pixels(self):
        return self.total_pixels * self._pixel.get_area()
    
   
    def print_detail(self, tab = ""):
        result = ""
        result += super().print_detail(tab)
        tab += '\t'
        result += self._pixel.print_detail(tab)
        if self.is_cp_in_pixel == 1:
            result += self._cp_pixel.print_detail(tab)
        return result