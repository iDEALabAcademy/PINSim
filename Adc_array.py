import Component
from Network import Network 
import math
from Hardware import Hardware
class AdcArray(Component.Component):

    def __init__(self, name, model):
        super().__init__(name, model)
        self._adc = Component.Component("Adc", "adc_model")# one ADC model

        self._cp_adc = Component.Component("AdcComputeAddon", "adc_cp_model")# one compute addon in ADC model

        if Network.type == "CNN":
            self.total_adcs_in_compute = math.ceil(Hardware.adc_number / Network.kernel_width) * Hardware.parallelism_level #in compute mode with CNN
        else:
            self.total_adcs_in_compute = Hardware.parallelism_level #In MLP minimum ADC for reading the result of whole focal plane is 1
        self.total_adcs_in_sensing = math.ceil(Hardware.adc_number / Hardware.box_size) #in sensing mode
        self.total_adcs_in_normal =  Hardware.adc_number #in normal mode

        
        self.operation_delay_in_compute = self.delay + self.delay_adcs() + self.delay_adc_compute_addon()# delay to read one kernel in CNN or one hidden element in MLP
        self.row_delay_in_normal = self.row_delay_in_sensing = self.delay + self.delay_adcs() #delay to read value of one row
        if Network.type == "CNN":
            self.total_delay_in_compute = self.operation_delay_in_compute * (Network.output_feature_map_height * math.ceil(Network.output_feature_map_width/Network.kernel_width)   * Network.kernel_number / Hardware.parallelism_level)
        else:
            self.total_delay_in_compute = self.operation_delay_in_compute * Network.output_feature_map_height  / Hardware.parallelism_level
        self.total_delay_in_sensing = self.delay + self.delay_adcs() * math.ceil(Hardware.pixel_array_height/Hardware.box_size)
        self.total_delay_in_normal = self.delay + self.delay_adcs() * Hardware.pixel_array_height
        
        self.total_power_in_normal = self.power + self.power_adcs(self.total_adcs_in_normal) 
        self.total_power_in_sensing = self.power + self.power_adcs(self.total_adcs_in_sensing) 
        self.total_power_in_compute = self.power + self.power_adcs(self.total_adcs_in_compute)  + self.power_adc_compute_addon()
        
        self.total_power = (self.total_power_in_normal * Hardware.op_percentage[0]) + (self.total_power_in_sensing * Hardware.op_percentage[1]) + ((self.total_power_in_compute * Hardware.op_percentage[2]) )/100.0
        self.total_area =  self.area + self.area_adcs() + self.area_adc_compute_addon()
        self.total_delay = max(self.total_delay_in_normal, self.total_delay_in_sensing, self.total_delay_in_compute)


    def power_adcs(self,adc_number):
       return adc_number * self._adc.get_power()
    
    def delay_adcs(self):
        return self._adc.get_delay()

    def area_adcs(self):
        return max(self.total_adcs_in_compute, self.total_adcs_in_normal) * self._adc.get_area() #reuse ADC in sensing and computing

    def power_adc_compute_addon(self):
        return Hardware.cp_in_adc * self.total_adcs_in_compute * self._cp_adc.get_power() * Hardware.cp_per_adc * Hardware.parallelism_level

    def delay_adc_compute_addon(self):
        return Hardware.cp_in_adc * self._cp_adc.get_delay()

    def area_adc_compute_addon(self):
        return Hardware.cp_in_adc * self.total_adcs_in_compute * self._cp_adc.get_area() * Hardware.cp_per_adc

    def print_detail(self, tab = ""):
        result = ""
        result += super().print_detail(tab)
        tab += '\t'
        result += self._adc.print_detail(tab)
        if Hardware.cp_in_adc == 1:
            result += self._cp_adc.print_detail(tab)
        return result