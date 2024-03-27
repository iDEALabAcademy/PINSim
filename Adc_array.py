import Component
from Network import Network 
import math
from Hardware import Hardware
class AdcArray(Component.Component):

    def __init__(self, name, model):
        super().__init__(name, model)
        self._adc = Component.Component("Adc", "adc_model")# one ADC model

        self._cp_adc = Component.Component("AdcComputeAddon", "adc_cp_model")# one compute addon in ADC model
        # TODO: the network config should add to this code (remove ADC_number)
        self._parallelism_level = Hardware.parallelism_level

        if Network.type == "CNN":
            self.total_adcs_in_compute = math.ceil(Hardware.adc_number / Network.kernel_width) * Hardware.parallelism_level #in compute mode with CNN
        else:
            self.total_adcs_in_compute = Hardware.parallelism_level #In MLP minimum ADC for reading the result of whole focal plane is 1
            
        self.total_adcs_in_sensing = math.ceil(Hardware.adc_number // Hardware.box_size) #in sensing mode
        self.total_adcs_in_normal =  Hardware.adc_number #in normal mode
        self.is_cp_in_adc = Hardware.cp_in_adc  #check location of compute addons
        self.cp_per_adc = Hardware.cp_per_adc  #numbe of compute addons per each ADC
        self._cp_percentage = Hardware.cp_percentage


        self.total_power_in_compute = self.power + self.power_adcs(self.total_adcs_in_compute) + self.power_adc_compute_addon()
        self.total_delay_in_compute = self.delay + self.delay_adcs() + self.delay_adc_compute_addon()

        self.total_power_in_sensing = self.power + self.power_adcs(self.total_adcs_in_sensing) 
        self.total_delay_in_sensing = self.delay + self.delay_adcs()

        self.total_power = ((self.total_power_in_compute * self._cp_percentage) + (self.total_power_in_sensing * ( 100 - self._cp_percentage)))/100.0
        self.total_area =  self.area + self.area_adcs() + self.area_adc_compute_addon()
        self.total_delay = max(self.total_delay_in_sensing, self.total_delay_in_compute)


    def power_adcs(self,adc_number):
       return adc_number * self._adc.get_power()
    
    def delay_adcs(self):
        return self._adc.get_delay()

    def area_adcs(self):
        return max(self.total_adcs_in_compute, self.total_adcs_in_sensing) * self._adc.get_area() #reuse ADC in sensing and computing

    def power_adc_compute_addon(self):
        return self.is_cp_in_adc * self.total_adcs_in_compute * self._cp_adc.get_power() * self.cp_per_adc * self._parallelism_level

    def delay_adc_compute_addon(self):
        return self.is_cp_in_adc * self._cp_adc.get_delay()

    def area_adc_compute_addon(self):
        return self.is_cp_in_adc * self.total_adcs_in_compute * self._cp_adc.get_area() * self.cp_per_adc

    def print_detail(self, tab = ""):
        result = ""
        result += super().print_detail(tab)
        tab += '\t'
        result += self._adc.print_detail(tab)
        if self.is_cp_in_adc == 1:
            result += self._cp_adc.print_detail(tab)
        return result