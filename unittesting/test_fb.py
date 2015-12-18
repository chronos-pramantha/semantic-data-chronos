import unittest
import json
import urllib

from flankers.fbstore import FBStore, generate_token
from flankers.tools import spot_urls

__author__ = 'Lorenzo'


class FBTests(unittest.TestCase):
    def test_get(self):
        aliases = ['GuntersSpacePage', 'SETIInstitute']
        for a in aliases:
            url = 'https://graph.facebook.com/{}/posts?{}&limit=5'.format(a, generate_token())
            response = urllib.urlopen(url)
            response = json.loads(response.read())
            if 'error' not in response.keys():
                print response
                print spot_urls(response['data'][0]['message'])
            else:
                print response['error']['message'], response['error']['type']