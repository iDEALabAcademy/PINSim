from Config import Config
from Hardware import Hardware

class Network:
    """
    Network class to read and store network configuration settings from the configuration file.
    """
    _config = Config.config
    name = "Network"
    type = str(_config["NetworkConfig"]["type"])

    @classmethod
    def _load_cnn_config(cls):
        """
        Load the CNN-specific configuration settings.
        """
        cls.kernel_number = int(cls._config["NetworkConfig"]["kernel_number"])
        cls.kernel_width = int(cls._config["NetworkConfig"]["kernel_width"])
        cls.kernel_height = int(cls._config["NetworkConfig"]["kernel_height"])
        cls.stride = int(cls._config["NetworkConfig"]["stride"])
        cls.padding = int(cls._config["NetworkConfig"]["padding"])
        cls.kernel_size = cls.kernel_height * cls.kernel_width
        cls.total_weights = cls.kernel_size * cls.kernel_number
        cls.output_feature_map_width = cls.calculate_output_height(Hardware.pixel_array_width)
        cls.output_feature_map_height = cls.calculate_output_height(Hardware.pixel_array_height)
        cls.output_feature_map_size = cls.output_feature_map_height * cls.output_feature_map_width

    @classmethod
    def _load_other_config(cls):
        """
        Load the configuration settings for non-CNN networks.
        """
        cls.hidden_node = int(cls._config["NetworkConfig"]["hidden_node"])
        cls.total_weights = int(Hardware.pixel_array_width) * int(Hardware.pixel_array_height) * cls.hidden_node

    @classmethod
    def initialize(cls):
        """
        Initialize the Network class by loading the appropriate configuration settings.
        """
        if cls.type == "CNN":
            cls._load_cnn_config()
        else:
            cls._load_other_config()

    @classmethod
    def calculate_output_height(cls, pixel_array_height):
        """
        Calculate the output height of the feature map.
        
        Parameters:
        pixel_array_height (int): The height of the input pixel array.
        
        Returns:
        int: The output height of the feature map.
        """
        if cls.type == "CNN":
            return ((pixel_array_height - cls.kernel_height + (2 * cls.padding)) // cls.stride) + 1
        else:
            return cls.hidden_node

    @classmethod
    def print_detail(cls, tab=""):
        """
        Print the details of the network configuration.
        
        Parameters:
        tab (str): The tab character(s) to prepend to each line. Default is an empty string.
        
        Returns:
        str: A string representation of the network configuration details.
        """
        tab += "\t"
        result = "****************************\n"
        attrs = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("_")]
        for attr in attrs:
            value = getattr(cls, attr)
            result += tab + f"{attr} = {value}\n"
        return result

# # To use this 'static' class, you first initialize it with configuration.
# Network.initialize()
