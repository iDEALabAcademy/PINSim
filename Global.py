import Component
import Global_cell
import Network
class Global(Component.Component):
    def __init__(self, name, model, config, sub_component=None):
        super().__init__(name, model, config, sub_component)
        self._global_cell = Global_cell.GlobalCell("GlobalCell", "global_model", config)  # one buffer cell
        self._weight_precision = int(config["HardwareConfig"]["weight_precision"])
        self.bus_size = int(config[name]["bus_size"])
        self._cp_percentage = float(config["HardwareConfig"]["cp_percentage"])

        self._network = Network.Network(config)
        self.memory_bit_size = self._weight_precision * self._network.kernel_size * self._network.kernel_number
        self.memory_size = self.convert_size(self.memory_bit_size)
        self.read_power_per_weight = self._global_cell.read_power * self._weight_precision
        self.write_power_per_weight = self._global_cell.write_power * self._weight_precision
        self.read_delay_per_weight = self._global_cell.read_delay * (self.bus_size/self._weight_precision) #TODO: check it with others
        self.write_delay_per_weight = self._global_cell.write_delay * (self.bus_size/self._weight_precision) #TODO: check it with others
        self.read_per_kernel = self.read_power()
        self.delay_per_kernel = self._global_cell.read_delay * (self.bus_size/self._weight_precision) #TODO: check it with others

        self.total_delay = self.delay + self.delay_per_kernel
        self.total_power = self.power + self._network.kernel_size * self.read_power_per_weight #power for reading each kernel
        self.total_area = self.area + (self.memory_bit_size * self._global_cell.total_area)

    def read_power(self):
        return self._network.kernel_size * self.read_power_per_weight 
    
     
    def convert_size(self,size_in_bits):
        """
        Convert a size from bits to more readable units (KB, MB, GB, etc.)

        :param size_in_bits: Size in bits
        :return: A string representing the size in a more readable format
        """
        # Define the conversion constants
        B = 8
        KB = 1024 * B  # 1 Kilobyte = 1024 * 8 bits
        MB = KB * 1024  # 1 Megabyte = 1024 Kilobytes
        GB = MB * 1024  # 1 Gigabyte = 1024 Megabytes
        TB = GB * 1024  # 1 Terabyte = 1024 Gigabytes

        # Convert the size to a more readable format
        if size_in_bits >= TB:
            return f"{size_in_bits / TB:.2f} TB"
        elif size_in_bits >= GB:
            return f"{size_in_bits / GB:.2f} GB"
        elif size_in_bits >= MB:
            return f"{size_in_bits / MB:.2f} MB"
        elif size_in_bits >= KB:
            return f"{size_in_bits / KB:.2f} KB"
        elif size_in_bits >= B:
            return f"{size_in_bits / B:.2f} Bytes"
        else:
            return f"{size_in_bits} bits"

    def print_detail(self, tab = ""):
        result = ""
        result += super().print_detail(tab)
        tab += '\t'
        result += self._global_cell.print_detail(tab)
        return result