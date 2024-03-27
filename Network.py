from Config import Config

class Network:
    _config = Config.config
    name = "Network"
    type = str(_config["NetworkConfig"]["type"])

    @classmethod
    def _load_cnn_config(self):
        self.kernel_number = int(self._config["NetworkConfig"]["kernel_number"])
        self.kernel_width = int(self._config["NetworkConfig"]["kernel_width"])
        self.kernel_height = int(self._config["NetworkConfig"]["kernel_height"])
        self.stride = int(self._config["NetworkConfig"]["stride"])
        self.padding = int(self._config["NetworkConfig"]["padding"])
        self.kernel_size = self.kernel_height * self.kernel_width
        self.total_weights = self.kernel_size * self.kernel_number

    @classmethod
    def _load_other_config(self):
        self.hidden_node = int(self._config["NetworkConfig"]["hidden_node"])
        self.total_weights = int(self._config["HardwareConfig"]["pixel_array_width"]) * int(self._config["HardwareConfig"]["pixel_array_height"]) * self.hidden_node

    @classmethod
    def initialize(self):
        if self.type == "CNN":
            self._load_cnn_config()
        else:
            self._load_other_config()

    @classmethod
    def calculate_output_height(self, pixel_array_height):
        if self.type == "CNN":
            return ((pixel_array_height - self.kernel_height + (2 * self.padding)) // self.stride) + 1
        else:
            return self.hidden_node

    @classmethod
    def print_detail(self, tab=""):
        tab += "\t"
        result = ""
        result += '****************************\n'
        attrs = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("_")]
        for attr in attrs:
            value = getattr(self, attr)
            result += tab + f"{attr} = {value}\n"
        return result

# # To use this 'static' class, you first initialize it with configuration.
# Network.initialize()

