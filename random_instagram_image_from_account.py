import requests, json


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