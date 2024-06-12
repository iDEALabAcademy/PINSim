from Hardware import Hardware
class Sizing:
    technology_size = Hardware.technology_size
    area_conversion = {
        180: 12,
        130: 4.3,
        90: 1.9,
        65: 1,
        45: 0.66,
        32: 0.31,
        22: 0.15
    }
    delay_conversion = {
        180: 3.57,
        130: 1.49,
        90: 1.2,
        65: 1,
        45: 0.35,
        32: 0.31,
        22: 0.27
    }
    power_conversion = {
        180: 5.78,
        130: 2.99,
        90: 1.53,
        65: 1,  
        45: 1.49,
        32: 0.63,
        22: 0.33
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


    