from Config import Config

class Hardware:
    _config = Config.config
    name = "Hardware"
    pixel_array_width   = int(_config["HardwareConfig"]["pixel_array_width"])
    pixel_array_height  = int(_config["HardwareConfig"]["pixel_array_height"])
    adc_number          = int(_config["HardwareConfig"]["adc_number"])
    op_percentage       = [float(item) for item in _config["HardwareConfig"]["operations_percentage"].split(',')] #percentage of normal, sensig and computing ( total should be 100)
    box_size            = int(_config["HardwareConfig"]["box_size"])
    technology_size     = int(_config["HardwareConfig"]["technology_size"])
    pixel_model         = int(_config["HardwareConfig"]["pixel_model"])
    pixel_array_model   = int(_config["HardwareConfig"]["pixel_array_model"])
    main_system_model   = int(_config["HardwareConfig"]["main_system_model"])
    adc_model           = int(_config["HardwareConfig"]["adc_model"])
    adc_array_model     = int(_config["HardwareConfig"]["adc_array_model"])
    adc_cp_model        = int(_config["HardwareConfig"]["adc_cp_model"])
    pixel_cp_model      = int(_config["HardwareConfig"]["pixel_cp_model"])
    cp_in_pixel         = int(_config["HardwareConfig"]["cp_in_pixel"])
    cp_in_adc           = int(_config["HardwareConfig"]["cp_in_adc"])
    cp_per_pixel        = int(_config["HardwareConfig"]["cp_per_pixel"])
    cp_per_adc          = int(_config["HardwareConfig"]["cp_per_adc"])
    parallelism_level   = int(_config["HardwareConfig"]["parallelism_level"])
    buffer_model        = int(_config["HardwareConfig"]["buffer_model"])
    global_model        = int(_config["HardwareConfig"]["global_model"])
    weight_precision    = int(_config["HardwareConfig"]["weight_precision"])

    



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

