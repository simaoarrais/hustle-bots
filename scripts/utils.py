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

def save_json_file(file_path=None, data=None, logger=None):
    if data is None:
        return None

    # Create output folder
    create_output_folder()

    # Define the file path
    if file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(current_dir, '..', 'output')  # Move up one directory to 'hustle-bots'
        file_path = os.path.join(output_folder, 'default.json')

    # If the file doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logger.info(f"SAVED FILE: {file_path}")

    else:
        # Prompt to overwrite the file
        print(f"The following file already exists: {file_path}")
        x = input(f"Please enter \"y\" or \"n\" to conclude action: ").lower()

        if x == 'n':
            pass

        elif x == 'y':
            os.remove(file_path)
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logger.info(f"SAVED FILE: {file_path}")