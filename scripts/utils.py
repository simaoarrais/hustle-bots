import os
import requests
import re

from RedDownloader import RedDownloader


def create_output_folders():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hustle_bots_dir = os.path.abspath(os.path.join(current_dir, '..'))  # Go up one level to 'hustle-bots'

    output_folder = os.path.join(hustle_bots_dir, 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    logs_folder = os.path.join(hustle_bots_dir, 'logs')
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    return output_folder, logs_folder

def standardize_title(title):
    standard_title = title.replace('🔥', '').strip()
    standard_title = standard_title[0].upper() + standard_title[1:]
    return standard_title

def download_video(post):
    url = post['url']
    filename = post['id']
    output = f'../output/'
    file_path = f'{output}{filename}.mp4'

    fallback_url = post['media']['reddit_video']['fallback_url']
    pattern = r'(?<=DASH_)\d+'
    matches = re.findall(pattern, fallback_url)
    quality = matches[0]

    if not os.path.exists(file_path):
        RedDownloader.Download(url , output=filename, destination=output, quality=quality)

    return file_path

def download_photo(post):
    url = post['url']
    filename = post['id']
    output = f'../output/'

    response = requests.get(url)
    file_path = f'{output}{filename}.jpg'

    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path