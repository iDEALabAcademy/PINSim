class Sizing:
    def __init__(self, config):
        self.technology_size = int(config["HardwareConfig"]["technology_size"])

    def calculate_power(self,power):
        # todo: impliment the formulla
        return power

    def calculate_area(self, area):
        # todo: impliment the formulla
        return area

    def calculate_delay(self, delay):
        # todo: impliment the formulla
        return delay
    