class Network():

    def __init__(self, config):
        self.name = "Network"
        self.network_type = str(config["NetworkConfig"]["network_type"])
        if self.network_type == "CNN":
            self.kernel_number = int(config["NetworkConfig"]["kernel_number"])
            self.kernel_width = int(config["NetworkConfig"]["kernel_width"])
            self.kernel_height = int(config["NetworkConfig"]["kernel_height"])
            self.stride = int(config["NetworkConfig"]["stride"])
            self.padding = int(config["NetworkConfig"]["padding"])
            self.kernel_size = self.kernel_height * self.kernel_width
            self.total_weights = self.kernel_size * self.kernel_number #total number of weights
            # self.hedden_node = 0
        else:
            self.hedden_node = int(config["NetworkConfig"]["hedden_node"])
            self.total_weights = int(config["HardwareConfig"]["pixel_array_width"]) * int(config["HardwareConfig"]["pixel_array_height"]) * self.hedden_node
            # self.kernel_number = 0
            # self.kernel_width = 0
            # self.kernel_height = 0
            # self.stride = 0
            # self.padding = 0
            # self.kernel_size = 0
    def calculate_output_height(self,pixel_array_height):
    # Calculate the output size for one dimension
        if self.network_type == "CNN":
            return ((pixel_array_height - self.kernel_height + (2 * self.padding)) // self.stride) + 1
        else:
            return self.hedden_node

    def print_detail(self, tab = ""):
        tab += "\t"
        result = ""
        result += ('****************************\n')
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                 result += tab + f"{attr} = {value}\n"
        return result
