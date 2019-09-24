#!/usr/bin/env python

import urllib, urllib2, json, sys, os
from os.path import join, expanduser, isfile, exists
from os import makedirs

# Configurations
# Location to save downloaded wallpapers
# Leave the IMAGE_DIR empty to use default directory /Users/USERNAME/Pictures/BingWallpaper
# Or you can set your own custom directory
IMAGE_DIR = ''
# ISO country code
# eg. 'en-US', 'en-NZ', 'zh-CN' or just leave it empty
COUNTRY_CODE = 'en-SE'
# Download image resolution (select among: 1366x768, 1920x1080 or 1920x1200 (this last one adds a Bing logo on the right corner))
IMAGE_RES = '1920x1080'

def get_wallpaper_path(file_name):
    if '' != IMAGE_DIR.strip():
        dir = IMAGE_DIR
    else:
        dir = join(expanduser("~"), 'Pictures/BingWallpaper')

    if not exists(dir):
        makedirs(dir)

    file_path = join(dir, file_name)
    return file_path


# Download a image with given URL
def download_image(url, download_only=False):
    file_name = url.split(".")[3] + ".jpg"
    file_path = get_wallpaper_path(file_name)

    if isfile(file_path):
        print('Skipped - ' + file_name + ' exists already.')
    else:
        urllib.urlretrieve(url, file_path)
        print('Image downloaded --> ' + file_path)

    if not download_only:
        set_wallpaper(file_path)


# Set Finder wallpaper
# See http://stackoverflow.com/questions/431205/how-can-i-programatically-change-the-background-in-mac-os-x
def set_wallpaper(file_path):
    if isfile(file_path):
        script = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + file_path + "\"'"
        os.system(script)
        print('Wallpaper set to ' + file_path)


# Display help message
def print_help_message():
    msg = '''
Bing Wallpaper for Mac version 1.2
By Declan Gao  http://declangao.me

Bing Wallpaper for Mac can batch download and set Bing image of the day as wallpaper on OS X.

Usage: 
python bing.py [option]

no argument         download today's picture of the day and set it as wallpaper
-d or --download    download and save the last 8 pictures withouth changing the current wallpaper
-h or --help        display this help message
    '''
    print(msg)
    sys.exit()


def main():
    # Check arguments
    if len(sys.argv) == 1:
        flag_download_only= False
    elif len(sys.argv) == 2:
        if '-d' == sys.argv[1] or '--download' == sys.argv[1]:
            flag_download_only = True
        elif '-h' == sys.argv[1] or '--help' == sys.argv[1]:
            print_help_message()
        else:
            print('Invalid argument!')
            print_help_message()
    else:
        print('Invalid arguments!')
        print_help_message()

    # Choose a proper URL
    # The API only returns 8 pictures at most. No need to set the number higher than 8.
    # See http://stackoverflow.com/questions/10639914/is-there-a-way-to-get-bings-photo-of-the-day
    if flag_download_only:
        url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8'
    else:
        # Set n=8 to get only the newest picture of the day
        url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'

    # Use country code if provided
    if '' != COUNTRY_CODE.strip():
        url += '&mkt=' + COUNTRY_CODE

    try:
        # Make the request
        response = urllib2.urlopen(url)
        json_data = json.load(response) # Get JSON

        if 'images' in json_data:
            images = json_data['images']
        else:
            sys.exit('JSON error. Please try again later...')
        
        # Start downloading!
        print('Downloading...')
        for i in range(len(images)):
            url = 'http://www.bing.com' + images[i]['url']
            url = url.replace("1366x768", IMAGE_RES)
            if flag_download_only:
                download_image(url, True)
            else:
                download_image(url)

    except urllib2.HTTPError, e:
        print('Error ' + str(e.code) + '. Please try again later...')
    except urllib2.URLError, e:
        print('Error. Please check your internet connection...')


if __name__ == '__main__':
    main()
