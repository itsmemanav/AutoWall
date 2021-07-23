# This Script will automatically fetch a High Quality image from Unsplash API and set it as the Desktop Background every hour.

import requests
import os
import sys
import re
from datetime import datetime

from requests.exceptions import HTTPError


def saveWallpaper(wallpaper_url: str, wallpaper_id: str) -> None:

    timestamp = datetime.today().strftime("%Y_%m_%d_%H-%m")
    wallpaper_name = f"{wallpaper_id}_{timestamp}.jpeg"

    # Checking for a folder named 'Wallpapers' in current directory and creating it if it doesn't exist
    if not os.path.isdir('Wallpapers'):
        os.mkdir('Wallpapers')

    os.chdir('Wallpapers')

    res = requests.get(wallpaper_url)

    with open(wallpaper_name, 'wb') as file:
        file.write(res.content)


    # Reading the Accesskey from the file
try:
    with open("accesskey.txt", "r") as file:
        ACCESSKEY = file.readline().strip()
except FileNotFoundError as fnf_error:
    sys.exit(fnf_error)


URL = "https://api.unsplash.com/photos/random"

params = {'query': 'wanderlust',
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
wallpaper_id = ''.join(re.findall('[a-zA-Z]+', r['id']))

saveWallpaper(wallpaper_url, wallpaper_id)
