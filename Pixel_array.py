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

        self.outfmap_height = Network.calculate_output_height(Hardware.pixel_array_height)
        self.total_pixels = Hardware.pixel_array_width * Hardware.pixel_array_height
        self.active_pixels = math.ceil(Hardware.pixel_array_width/float(Hardware.box_size)) * math.ceil(Hardware.pixel_array_height/float(Hardware.box_size))
        self.total_power_in_normal = self.power + (self._pixel.get_power() * self.total_pixels) #assume all the pixels are on
        self.total_power_in_compute = self.power + self.power_pixel_compute_addon() + self.power_pixels()
        self.total_power_in_sensing = self.power + (self._pixel.get_power() * self.active_pixels) #assume in the sensing mode only central pixels are On.
        self.total_power = ((self.total_power_in_normal * Hardware.op_percentage[0]) + (self.total_power_in_sensing * Hardware.op_percentage[1]) + (self.total_power_in_compute * Hardware.op_percentage[2]))/100.0
        # TODO: check total_delay_in_compute self.outfmap_height :done
        self.total_delay_in_normal = self.delay + self.delay_pixels() * Hardware.pixel_array_height  # read pixel values row by row 
        self.total_delay_in_sensing = self.delay + self.delay_pixels() * math.ceil(Hardware.pixel_array_height/float(Hardware.box_size))
        if Network.type == "CNN":
            # TODO check with @arman
            self.total_delay_in_compute = self.delay + (self.delay_pixel_compute_addon() + self.delay_pixels()) * (self.outfmap_height * (Network.kernel_width - Network.stride + 1) * Network.kernel_number / Hardware.parallelism_level)
        else:
            self.total_delay_in_compute = self.delay + (self.delay_pixel_compute_addon() + self.delay_pixels()) * self.outfmap_height // Hardware.parallelism_level


        # self.kernel_delay_in_compute = self.delay + (self.delay_pixel_compute_addon() + self.delay_pixels()) * self.outfmap_height
        self.row_delay_in_sensing = self.delay + self.delay_pixels()
        
        self.total_delay = max(self.total_delay_in_compute, self.total_delay_in_sensing, self.total_delay_in_normal)
        self.total_area = self.area + self.area_pixel_compute_addon() + self.area_pixels()

    def power_pixel_compute_addon(self):
        return Hardware.cp_in_pixel * self.total_pixels * self._cp_pixel.get_power() * Hardware.cp_per_pixel

    def delay_pixel_compute_addon(self):
        return Hardware.cp_in_pixel * self._cp_pixel.get_delay()

    def area_pixel_compute_addon(self):
        return Hardware.cp_in_pixel * self.total_pixels * self._cp_pixel.get_area() * Hardware.cp_per_pixel

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
        if Hardware.cp_in_pixel == 1:
            result += self._cp_pixel.print_detail(tab)
        return result