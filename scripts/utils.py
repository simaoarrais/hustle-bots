import os
import json

import requests

def create_output_folder():
    """
    Create the 'output' folder inside the 'hustle-bots' directory.

    Returns:
        str: The path of the output folder (either newly created or existing).
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hustle_bots_dir = os.path.abspath(os.path.join(current_dir, '..'))  # Go up two levels to 'hustle-bots'
    output_folder = os.path.join(hustle_bots_dir, 'output')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    return output_folder

def create_logs_folder():
    """
    Create the 'logs' folder inside the 'hustle-bots' directory.

    Returns:
        str: The path of the output folder (either newly created or existing).
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hustle_bots_dir = os.path.abspath(os.path.join(current_dir, '..'))  # Go up two levels to 'hustle-bots'
    logs_folder = os.path.join(hustle_bots_dir, 'logs')

    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    
    return logs_folder

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

def get_next_post(file_path, logger):
        if check_file_exists_output(file_path):
            post_data = read_json_file(file_path)
            if isinstance(post_data, list) and len(post_data) > 0:
                logger.info(f'Fetch new post from {file_path}')
                return post_data[0]
        return None

def remove_post_from_file(file_path, post_data, logger):
    if check_file_exists_output(file_path):
        posts = read_json_file(file_path)
        updated_posts = [post for post in posts if post != post_data]
        save_json_file(logger=logger, file_path=file_path, data=updated_posts, overwrite=True)
        delete_file(file_path=file_path, logger=logger)
        logger.info(f'Removed posted post from {file_path}.')
        
def delete_file(file_path, logger):
    """
    Delete a file given its file path.

    Args:
        file_path (str): Path of the file to delete.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            logger.info(f'File \'{file_path}\' does not exist.')
            return False
    except Exception as e:
        logger.warning(f'Error occurred while deleting file: {e}')
        return False

def save_post_image(file_path, post_id, post_url):
    response = requests.get(post_url)
    file_path = f'{post_id}.jpg'

    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path