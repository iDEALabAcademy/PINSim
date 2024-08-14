import configparser
import os
class Config:
    """
    Config class to read and store configuration settings from a configuration file.
    """
    # Initialize the config parser
    config = configparser.ConfigParser()
    
    # Read the configuration file
    
    config.read(os.path.join('Examples','Example3','CNN.ini'))
    #config.read('config.ini')

# Assuming config.ini has sections [NetworkConfig] and [HardwareConfig] with the necessary settings
