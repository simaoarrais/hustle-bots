import os
import json

def create_output_folder():
    """Create the 'output' folder if it doesn't exist."""
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def save_json_file(file_name, file_data):
    create_output_folder()

    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
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