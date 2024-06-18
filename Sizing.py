from Hardware import Hardware

class Sizing:
    """
    Sizing class to calculate power, area, and delay based on technology size.
    """
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
    def calculate_power(cls, power):
        """
        Calculate the power based on the technology size.
        
        Parameters:
        power (float): The base power value.
        
        Returns:
        float: The adjusted power value based on the technology size.
        """
        if cls.technology_size in cls.power_conversion:
            return power * cls.power_conversion[cls.technology_size]
        else:
            raise ValueError("Target technology node not in conversion factors.")

    @classmethod
    def calculate_area(cls, area):
        """
        Calculate the area based on the technology size.
        
        Parameters:
        area (float): The base area value.
        
        Returns:
        float: The adjusted area value based on the technology size.
        """
        if cls.technology_size in cls.area_conversion:
            return area * cls.area_conversion[cls.technology_size]
        else:
            raise ValueError("Target technology node not in conversion factors.")

    @classmethod
    def calculate_delay(cls, delay):
        """
        Calculate the delay based on the technology size.
        
        Parameters:
        delay (float): The base delay value.
        
        Returns:
        float: The adjusted delay value based on the technology size.
        """
        if cls.technology_size in cls.delay_conversion:
            return delay * cls.delay_conversion[cls.technology_size]
        else:
            raise ValueError("Target technology node not in conversion factors.")
