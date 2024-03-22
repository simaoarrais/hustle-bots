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

def save_json_file(file_path=None, data=None, overwrite=False, logger=None):
    if data is None:
        return False

    if file_path is None:
        file_path = 'default.json'
    
    if not '/' in file_path:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'output', file_path)

    # Create output folder
    create_output_folder()

    # If the file doesn't exist or overwrite is True
    if not os.path.exists(file_path) or overwrite:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logger.info(f"SAVED FILE: {file_path}")
        return True

    return False
