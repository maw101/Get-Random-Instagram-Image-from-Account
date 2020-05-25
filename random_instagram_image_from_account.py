"""
Provides functions to get a random image URL of a given Instagram account and
the facility to display this.

This module provides functions to randomly get an images URL from a specified
 Instagram account - given as a command line argument. Functions also allow for
 displaying of an image at a given URL.
"""

import json
import argparse
import random
from io import BytesIO # for opening the image
from PIL import Image # for displaying the image
import requests

def format_instagram_url(account_name):
    """Generates a URL to an Accounts JSON file.

        Args:
    		account_name (str): the Instagram account name
    	Returns:
    		str: formatted URL to the JSON file for the Instagram account

    """
    return f'https://www.instagram.com/{account_name}/?__a=1'


def get_json(account_name):
    """Fetches JSON content for a given Instagram Account.

        Args:
    		account_name (str): the Instagram account name
    	Returns:
    		json object: Instagram accounts page JSON

    """
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
    """Gets all image media from an Instagram users JSON page data.

        Args:
    		json_page_data (json object): Instagram accounts page JSON
    	Returns:
    		collection of all timeline media from the page

    """
    return json_page_data['graphql']['user']['edge_owner_to_timeline_media']['edges']


def get_random_index(item_count):
    """Generates a random integer 0 (item_count-1) inclusive.

        Args:
    		item_count (int): upper bound (non-inclusive) for random range
    	Returns:
    		int: a random integer in range [0, item_count)

    """
    return random.randint(0, (item_count - 1))


def get_random_images_json(timeline_media):
    """Returns the JSON data for a random single Instagram image from a
    collection of images JSON.

        Args:
    		timeline_media: collection of all timeline media from the page
    	Returns:
    		single instance of a timeline media item

    """
    random_index = get_random_index(len(timeline_media))
    return timeline_media[random_index]['node']


def get_image_url(image_json):
    """Returns an images URL from an Instagram images JSON data.

        Args:
    		image_json (json object): JSON data for a given media instance
    	Returns:
    		str: the URL for the media instance

    """
    return image_json['display_url']


def get_random_images_url(account_name):
    """Returns a random Instagram images URL given an Instagram Account Name.

        Args:
    		account_name (str): the name of the Instagram account
    	Returns:
    		str: a randomly chosen media instance's URL

    """
    # process json
    page_json = get_json(account_name) # get whole page json
    timeline_media = get_timeline_media(page_json) # get image json

    # get a single images json
    random_images_json = get_random_images_json(timeline_media)
    return get_image_url(random_images_json) # get the image url


def display_image_at_url(url):
    """Fetches an Image from a given URL and displays it to the user.

        Args:
    		url (str): the URL for the given media instance

    """
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
