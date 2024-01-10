class Network():

    def __init__(self, config):
        self.name = "Network"
        self.kernel_number = int(config["CnnConfig"]["kernel_number"])
        self.kernel_width = int(config["CnnConfig"]["kernel_width"])
        self.kernel_height = int(config["CnnConfig"]["kernel_height"])
        self.stride = int(config["CnnConfig"]["stride"])
        self.padding = int(config["CnnConfig"]["padding"])
        self.kernel_size = self.kernel_height * self.kernel_width
        self.total_weights = self.kernel_size * self.kernel_number #total number of weights
    def calculate_output_height(self,pixel_array_height):
    # Calculate the output size for one dimension
        return ((pixel_array_height - self.kernel_height + (2 * self.padding)) // self.stride) + 1

    def print_detail(self, tab = ""):
        tab += "\t"
        result = ""
        result += ('****************************\n')
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                 result += tab + f"{attr} = {value}\n"
        return result
