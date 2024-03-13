import Component
import math

class AdcArray(Component.Component):

    def __init__(self, name, model, config, sub_component=None):
        super().__init__(name, model, config, sub_component)
        self._adc = Component.Component("Adc", "adc_model", config)# one ADC model
        self._cp_adc = Component.Component("AdcComputeAddon", "adc_cp_model", config)# one compute addon in ADC model
        self.total_adcs_in_compute = int(config["HardwareConfig"]["adc_number"]) * int(config["HardwareConfig"]["parallelism_level"]) #in compute mode
        self.total_adcs_in_sensing = math.ceil(int(config["HardwareConfig"]["adc_number"]) / float(config["HardwareConfig"]["box_size"])) #in sensing mode
        self.is_cp_in_adc = int(config["HardwareConfig"]["cp_in_adc"])  #check location of compute addons
        self.cp_per_adc = int(config["HardwareConfig"]["cp_per_adc"])   #numbe of compute addons per each ADC
        self._cp_percentage = float(config["HardwareConfig"]["cp_percentage"])


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
        return self.is_cp_in_adc * self.total_adcs_in_compute * self._cp_adc.get_power() * self.cp_per_adc

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