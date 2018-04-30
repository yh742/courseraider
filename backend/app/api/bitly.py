import requests
import json
from instance.bitly_config import API_KEY, SHORTEN_URL


class BitlyApi:

    def __init__(self):
        self.params = query_params = {
            'access_token': API_KEY,
        }

    def shorten(self, url):
        self.params['longUrl'] = url
        response = requests.get(SHORTEN_URL, params=self.params)
        data = json.loads(response.content)
        if data['status_code'] == 200:
            return data['data']['url']
        else:
            return None