# This Script will automatically fetch a High Quality image from Unsplash API and set it as the Desktop Background every hour.

import requests
import os
import sys
import re
import ctypes
from datetime import datetime


from requests.exceptions import HTTPError


def saveWallpaper(wallpaper_url: str, wallpaper_id: str) -> str:
    # Fetches the raw wallpaper from the API response and stores it as a 'jpeg' under ./Wallpapers

    timestamp = datetime.today().strftime("%Y_%m_%d_%H-%m")
    wallpaper_name = f"{wallpaper_id}_{timestamp}.jpeg"

    # Creating a folder named 'Wallpapers' under current directory if it doesn't exist
    if not os.path.isdir('Wallpapers'):
        os.mkdir('Wallpapers')

    os.chdir('Wallpapers')

    # Before saving wallpaper, check if cleanup is required.
    cleanUp()

    res = requests.get(wallpaper_url)

    # Saving the wallpaper as - '<id>_<timestamp>.jpeg'
    with open(wallpaper_name, 'wb') as file:
        file.write(res.content)

    return os.path.abspath(wallpaper_name)


def changeWallpaper(wallpaper_path: str) -> None:
    # Updates the Wallpaper to the absolute image path passed as an argument
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 0)


def getTimeStamp(filename):
    modification_time = os.path.getmtime(filename)
    return datetime.fromtimestamp(modification_time)


def cleanUp() -> None:
    # Perform cleanup if number of saved wallpapers exceeded 5.
    if len(os.listdir()) >= 5:
        oldest_file = min(os.listdir(), key=getTimeStamp)
        os.remove(oldest_file)


def main() -> None:

    # Reading the Accesskey from the file
    try:
        with open("accesskey.txt", "r") as file:
            ACCESSKEY = file.readline().strip()
    except FileNotFoundError as fnf_error:
        print("Error: You need an accesskey in order to access the Unsplash API. Please refer the README.md file for more details.")
        sys.exit(fnf_error)

    URL = "https://api.unsplash.com/photos/random"

    params = {'query': 'nature',
              'orientation': 'landscape', 'w': '1920', 'h': '1080'}

    headers = {'Authorization': f"Client-ID {ACCESSKEY}"}

    # Sending request to Unsplash API and parsing response as JSON
    try:
        res = requests.get(URL, headers=headers, params=params)

        res.raise_for_status()

    except HTTPError as http_error:
        sys.exit(http_error)

    except Exception as err:
        print(f'Error: {err}')

    else:
        r = res.json()

    wallpaper_url = r['urls']['raw']
    wallpaper_id = ''.join(re.findall('[a-zA-Z0-9]+', r['id']))

    wallpaper_path = saveWallpaper(wallpaper_url, wallpaper_id)

    changeWallpaper(wallpaper_path)


if __name__ == "__main__":
    main()
