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
    create_output_folder()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_dir, '..', 'output')  # Move up one directory to 'hustle-bots'
    file_path = os.path.join(output_folder, file_name)

    if os.path.exists(file_path):
        print(f"The following file already exists: {file_path}")
        x = input(f"Please enter \"y\" or \"n\" to conclude action: ").lower()
        if x == 'y':
            os.remove(file_path)
            with open(file_path, 'w') as file:
                file.write(file_data)
            print(f"SAVED FILE --- {file_path}")
        elif x == 'n':
            pass
    else:
        with open(file_path, 'w') as file:
            json.dump(file_data, file, indent=4)
        print(f"SAVED FILE --- {file_path}")