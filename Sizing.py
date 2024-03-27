from Hardware import Hardware
class Sizing:
    technology_size = Hardware.technology_size

    @classmethod
    def calculate_power(self, power):
        # todo: impliment the formulla
        return power *(self.technology_size/self.technology_size)
    @classmethod
    def calculate_area(self, area):
        # todo: impliment the formulla
        return area
    @classmethod
    def calculate_delay(self, delay):
        # todo: impliment the formulla
        return delay
    