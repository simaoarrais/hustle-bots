import os
import json

def create_output_folder():
    """Create the 'output' folder if it doesn't exist."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_dir, '..', 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def save_json_file(file_name, file_data):
    # Create output folder
    create_output_folder()

    # Define the file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_dir, '..', 'output')  # Move up one directory to 'hustle-bots'
    file_path = os.path.join(output_folder, file_name)

    # If the file doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump(file_data, json_file, indent=4)
        print(f"SAVED FILE --- {file_path}")

    else:
        # Prompt to overwrite the file
        print(f"The following file already exists: {file_path}")
        x = input(f"Please enter \"y\" or \"n\" to conclude action: ").lower()

        if x == 'n':
            pass

        elif x == 'y':
            os.remove(file_path)
            with open(file_path, 'w') as json_file:
                json.dump(file_data, json_file)
            print(f"SAVED FILE --- {file_path}")