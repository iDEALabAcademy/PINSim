import Main_System as Main_System

if __name__ == '__main__':
    # Initialize the main system with its name and model configuration
    main_system = Main_System.Main_System("MainSystem", "main_system_model")
    
    # Get the details of the main system
    result = main_system.print_detail()
    
    # Print the result to the console
    print(result)
    
    # Write the result to a file named "result.txt"
    with open("result.txt", 'w') as file:
        file.write(result)
