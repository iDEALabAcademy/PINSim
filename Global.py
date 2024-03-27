import Component
import Global_cell
from Network import Network
from Config import Config
from Hardware import Hardware
class Global(Component.Component):
    def __init__(self, name, model):
        super().__init__(name, model)
        self._global_cell = Global_cell.GlobalCell("GlobalCell", "global_model")  # one buffer cell
        self.bus_size = int(Config.config[name]["bus_size"])
        
        self.read_power_per_weight = self._global_cell.read_power * Hardware.weight_precision
        self.write_power_per_weight = self._global_cell.write_power * Hardware.weight_precision
        self.read_delay_per_weight = self._global_cell.read_delay
        self.write_delay_per_weight = self._global_cell.write_delay  
                
        if Network.type == "CNN":
            self.memory_bit_size = Hardware.weight_precision * Network.kernel_size * Network.kernel_number
        else: #MLP
            self.memory_bit_size = Hardware.weight_precision * Network.hidden_node * Hardware.pixel_array_height * Hardware.pixel_array_width
            
        #All of them are per weight
        self.total_delay = self.delay + self._global_cell.total_delay       
        self.total_power = self.power + (self._global_cell.total_power * self.memory_bit_size) #static power of memory
        self.total_area = self.area + (self.memory_bit_size * self._global_cell.total_area)
            

        self.memory_size = self.convert_size(self.memory_bit_size)
        self.number_of_weight_read_per_clock = self.bus_size/Hardware.weight_precision
        
    def read_power(self):
        return Network.kernel_size * self.read_power_per_weight 
    
     
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