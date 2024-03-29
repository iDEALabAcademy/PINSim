import configparser

class Config():
    config = configparser.ConfigParser()
    config.read('config.ini')

# Assuming config.ini has sections [NetworkConfig] and [HardwareConfig] with the necessary settings

    
