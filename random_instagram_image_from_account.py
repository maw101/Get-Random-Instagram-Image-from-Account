"""
Provides functions to get a random image URL of a given Instagram account and
the facility to display this.

This module provides functions to randomly get an images URL from a specified 
Instagram account - given as a command line argument. Functions also allow for 
displaying of an image at a given URL.
"""


import requests
import json
import random
import argparse
# imports for displaying the image
from PIL import Image
from io import BytesIO


def format_instagram_url(account_name):
    """Generates a URL to an Accounts JSON file"""
    return f'https://www.instagram.com/{account_name}/?__a=1'


def get_json(account_name):
    """Fetches JSON content for a given Instagram Account"""
    url = format_instagram_url(account_name)
    try:
        # send a HTTP request to the server and save
        # the HTTP response in a response object called r
        request_response = requests.get(url)
        # raise exception if response not successful
        request_response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print("HTTP Error Occurred:", http_err)
    else:
        return json.loads(request_response.text)


def get_timeline_media(json_page_data):
    """Gets all image media from an Instagram users JSON page data"""
    return json_page_data['graphql']['user']['edge_owner_to_timeline_media']['edges']


def get_random_index(item_count):
    """Generates a random integer 0 (item_count-1) inclusive."""
    return random.randint(0, (item_count - 1))


def get_random_images_json(timeline_media):
    """Returns the JSON data for a random single Instagram images from a 
    collection of images JSON."""
    random_index = get_random_index(len(timeline_media))
    return timeline_media[random_index]['node']


def get_image_url(image_json):
    """Returns an images URL from an Instagram images JSON data."""
    return image_json['display_url']


def get_random_images_url(account_name):
    """Returns a random Instagram images URL given an Instagram Account Name."""
    # process json
    page_json = get_json(account_name) # get whole page json
    timeline_media = get_timeline_media(page_json) # get image json

    # get a single images json
    random_images_json = get_random_images_json(timeline_media) 
    return get_image_url(random_images_json) # get the image url


def display_image_at_url(url):
    """Fetches an Image from a given URL and displays it to the user."""
    # request the image and display it once fetched
    try:
        # send a HTTP request to the server and save the HTTP
        # response in a response object called image_response
        image_response = requests.get(url)
        # raise exception if response not successful
        image_response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print("HTTP Error Occurred:", http_err)
    else:
        img = Image.open(BytesIO(image_response.content))
        img.show()


if __name__ == '__main__':
    # parse command line arguments
    PARSER = argparse.ArgumentParser(description='Parse Instagram Account Name')
    PARSER.add_argument("account_name", nargs=1, help='Instagram Account Name')
    ARGS = PARSER.parse_args()

    # get account name argument value
    ACCOUNT_NAME = ARGS.account_name[0]
    print("Retrieving Random Image from Instagram Account @%s" % ACCOUNT_NAME)

    # get a random images URL
    IMAGE_URL = get_random_images_url(ACCOUNT_NAME)
    # fetch image at this URL and display it
    display_image_at_url(IMAGE_URL)
