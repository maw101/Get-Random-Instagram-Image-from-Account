import requests, json, random


def format_instagram_url(account_name):
	"""Generates a URL to an Accounts JSON file"""
	return f'https://www.instagram.com/{account_name}/?__a=1'


def get_json(account_name):
	"""Fetches JSON content for a given Instagram Account"""
	url = format_instagram_url(account_name)
	try:
		# send a HTTP request to the server and save
		# the HTTP response in a response object called r
		r = requests.get(url)
		# raise exception if response not successful
		r.raise_for_status()
	except requests.exceptions.HTTPError as http_err:
		print("HTTP Error Occurred:", http_err)
	else:
		return json.loads(r.text)


def get_timeline_media(json_page_data):
	"""Gets all image media from an Instagram users JSON page data"""
	return json_page_data['graphql']['user']['edge_owner_to_timeline_media']['edges'];


def get_random_index(item_count):
	"""Generates a random integer 0 (item_count-1) inclusive."""
	return random.randint(0, (item_count - 1))


def get_random_images_json(timeline_media):
	"""Returns the JSON data for a random single Instagram images from a collection of images JSON."""
	random_index = get_random_index(len(timeline_media))
	return timeline_media[random_index]['node']


def get_image_url(image_json):
	"""Returns an images URL from an Instagram images JSON data."""
	return image_json['display_url']


def get_random_images_url(account_name):
	"""Returns a random Instagram images URL given an Instagram Account Name."""
	# process json
	page_json = get_json(account_name) # get json for the whole page
	timeline_media = get_timeline_media(page_json) # get the json just for the images

	random_images_json = get_random_images_json(timeline_media) # get the json for just one image
	return get_image_url(random_images_json) # get the image url