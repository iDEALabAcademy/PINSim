import Component
import Network
import math
import Sizing
from Hardware import Hardware
from Network import Network

class PixelArray(Component.Component):
    def __init__(self, component_name, model_key):
        """
        Initialize the PixelArray with its name and model configuration.
        
        Parameters:
        component_name (str): The name of the PixelArray component.
        model_key (str): The model key to look up in the configuration.
        """
        super().__init__(component_name, model_key)
        self._pixel = Component.Component("Pixel", "pixel_model")  # One pixel model
        self._sizing = Sizing.Sizing()
        self._cp_pixel = Component.Component("PixelComputeAddon", "pixel_cp_model")  # One compute addon model for pixel

        self.outfmap_height = Network.calculate_output_height(Hardware.pixel_array_height)
        self.total_pixels = Hardware.pixel_array_width * Hardware.pixel_array_height
        self.active_pixels = math.ceil(Hardware.pixel_array_width / float(Hardware.box_size)) * math.ceil(Hardware.pixel_array_height / float(Hardware.box_size))
        
        # Calculate power consumption in different modes
        self.total_power_in_normal = self.power + (self._pixel.get_power() * self.total_pixels)  # Assume all the pixels are on
        self.total_power_in_compute = self.power + self.power_pixel_compute_addon() + self.power_pixels()  # Object detection mode
        self.total_power_in_sensing = self.power + (self._pixel.get_power() * self.active_pixels)  # Event detection mode
        self.total_power = (
            (self.total_power_in_normal * Hardware.op_percentage[0]) +
            (self.total_power_in_sensing * Hardware.op_percentage[1]) +
            (self.total_power_in_compute * Hardware.op_percentage[2])
        ) / 100.0
        
        # Calculate delay in different modes
        self.total_delay_in_normal = self.delay + self.delay_pixels() * Hardware.pixel_array_height  # Read pixel values row by row
        self.total_delay_in_sensing = self.delay + self.delay_pixels() * math.ceil(Hardware.pixel_array_height / float(Hardware.box_size))
        
        if Network.type == "CNN":
            self.total_delay_in_compute = self.delay + (self.delay_pixel_compute_addon() + self.delay_pixels()) * (
                self.outfmap_height * math.ceil(Network.output_feature_map_width / Network.kernel_width) * Network.kernel_number / Hardware.parallelism_level
            )
        else:
            self.total_delay_in_compute = self.delay + (self.delay_pixel_compute_addon() + self.delay_pixels()) * self.outfmap_height / Hardware.parallelism_level

        self.total_delay = max(self.total_delay_in_compute, self.total_delay_in_sensing, self.total_delay_in_normal)
        self.total_area = self.area + self.area_pixel_compute_addon() + self.area_pixels()

    def power_pixel_compute_addon(self):
        """
        Calculate the power consumption of the pixel compute addon.
        
        Returns:
        float: The power consumption of the pixel compute addon.
        """
        return Hardware.cp_in_pixel * self.total_pixels * self._cp_pixel.get_power() * Hardware.cp_per_pixel

    def delay_pixel_compute_addon(self):
        """
        Calculate the delay of the pixel compute addon.
        
        Returns:
        float: The delay of the pixel compute addon.
        """
        return Hardware.cp_in_pixel * self._cp_pixel.get_delay()

    def area_pixel_compute_addon(self):
        """
        Calculate the area of the pixel compute addon.
        
        Returns:
        float: The area of the pixel compute addon.
        """
        return Hardware.cp_in_pixel * self.total_pixels * self._cp_pixel.get_area() * Hardware.cp_per_pixel

    def power_pixels(self):
        """
        Calculate the total power consumption of the pixels.
        
        Returns:
        float: The total power consumption of the pixels.
        """
        return self.total_pixels * self._pixel.get_power()

    def delay_pixels(self):
        """
        Calculate the total delay of the pixel array.
        
        Returns:
        float: The total delay of the pixel array.
        """
        return self._pixel.get_delay()

    def area_pixels(self):
        """
        Calculate the total area of the pixel array.
        
        Returns:
        float: The total area of the pixel array.
        """
        return self.total_pixels * self._pixel.get_area()

    def print_detail(self, tab=""):
        """
        Print the details of the PixelArray component.
        
        Parameters:
        tab (str): The tab character(s) to prepend to each line. Default is an empty string.
        
        Returns:
        str: A string representation of the component details.
        """
        result = super().print_detail(tab)
        tab += '\t'
        result += self._pixel.print_detail(tab)
        if Hardware.cp_in_pixel == 1:
            result += self._cp_pixel.print_detail(tab)
        return result
