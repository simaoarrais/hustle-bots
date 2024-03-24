import os
import json

def create_output_folder():
    """
    Create the 'output' folder if it doesn't exist.

    Returns:
        bool: True if the folder was created, False if it already exists.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_dir, '..', 'output')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        return True
    return False

def check_file_exists_output(file_path):
    """
    Check if a file exists in the 'output' folder.

    Args:
        file_path (str): Path of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_dir, '..', 'output')
    if os.path.exists(os.path.join(output_folder, file_path)):
        return True
    return False

def read_json_file(file_path):
    """
    Read a JSON file from the 'output' folder.

    Args:
        file_path (str): Path of the JSON file to read.

    Returns:
        dict: Python dictionary containing data from the JSON file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'output', file_path)
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json_file(logger, file_path=None, data=[], overwrite=False, ):
    """
    Save a Python object as JSON data in the 'output' folder.

    Args:
        file_path (str, optional): Path of the JSON file to save. Defaults to 'default.json'.
        data (object, optional): Python object to save as JSON data. Defaults to [].
        overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.
        logger (Logger, optional): Optional logger object for logging messages.

    Returns:
        bool: True if the file was saved successfully, False if the file already exists and overwrite is False.
    """
    if file_path is None:
        file_path = 'default.json'
    
    if not '/' in file_path:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'output', file_path)

    # If the file doesn't exist or overwrite is True
    if not os.path.exists(file_path) or overwrite:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        if logger:
            logger.info(f"SAVED FILE: {file_path}")
        return True

    return False
