import Main_System as Main_System
import configparser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = configparser.ConfigParser()
    # Read the INI file 
    config.read('config.ini')
    main_system = Main_System.Main_System("MainSystem", "main_system_model", config)
    result = (main_system.print_detail())
    print(result)
    with open("result.txt", 'w') as file:
        file.write(result)

