from Hardware import Hardware
class Sizing:
    technology_size = Hardware.technology_size
    
    area_conversion = {
        180: 19,
        130: 6.4,
        90: 2.8,
        65: 1.5,
        45: 1,
        32: 0.46,
        22: 0.23
    }
    delay_conversion = {
        180: 10,
        130: 4.16,
        90: 3.44,
        65: 2.85,
        45: 1,
        32: 1,
        22: 0.78
    }
    power_conversion = {
        180: 3.95,
        130: 2.05,
        90: 1.02,
        65: 0.67,  
        45: 1,
        32: 0.43,
        22: 0.22
    }


    @classmethod
    def calculate_power(self, power):
        if self.technology_size in self.power_conversion:
            return power * self.power_conversion[self.technology_size]
        else:
            raise ValueError("Target technology node not in conversion factors.")

    @classmethod
    def calculate_area(self, area):
        if self.technology_size in self.area_conversion:
            return area * self.area_conversion[self.technology_size]
        else:
            raise ValueError("Target technology node not in conversion factors.")

    @classmethod
    def calculate_delay(self, delay):
        if self.technology_size in self.delay_conversion:
            return delay * self.delay_conversion[self.technology_size]
        else:
            raise ValueError("Target technology node not in conversion factors.")


    