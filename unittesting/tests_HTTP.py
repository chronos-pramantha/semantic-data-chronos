import unittest
import json
from scripts.remote.remote import get_curling, post_curling
from config.config import _ENV


__author__ = 'Lorenzo'


def test_integrity(res):
    try:
        res = json.loads(res)
        if 'error' not in res.keys():
            return res
        else:
            raise Exception
    except Exception:
        print "the endpoint response was in the wrong format or status 400 or 500"
        print res
        assert False


class HTTPEndpoints(unittest.TestCase):
    def __init__(self, env=None):
        super(HTTPEndpoints, self).__init__()
        if env is not None:
            self.test_env = env
        else:
            self.test_env = 'online'

class Endpoints_Articles(HTTPEndpoints):
    def test_articles_api_base_view(self):
        """
    Test the Articles JSON API: /articles/<version>/
    """
        _VERSION = "v04"
        print "Running test_articles"
        import urllib
        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/"

        first = get_curling(base_url)
        first = test_integrity(first)

        bookmark = first['next']
        print bookmark
        for i in range(0, 10):  # higher the second element of the interval to test more pages
            print i
            if bookmark:
                count_ = 0
                response = urllib.urlopen(bookmark).read()
                response = test_integrity(response)
                for a in response['articles']:
                    # print a['uuid']
                    count_ += 1

                bookmark = response['next']
                print count_, i, bookmark
            else:
                print 'Articles finished'
                return None

    def test_articles_api_type_view(self):
        """
    Test the Articles JSON API: /articles/<version>/?type_of=
    """
        _VERSION = "v04"
        print "Running test_articles TYPE_OF"
        import urllib
        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/filterby?type=feed"

        first = get_curling(base_url)
        first = test_integrity(first)

        bookmark = first['next']
        print bookmark
        for i in range(0, 10):  # higher the second element of the interval to test more pages
            print i
            if bookmark:
                count_ = 0
                response = urllib.urlopen(bookmark).read()
                response = test_integrity(response)
                for a in response['articles']:
                    # print a['uuid']
                    count_ += 1

                bookmark = response['next']
                print count_, i, bookmark
            else:
                print 'Articles by_type finished'
                return None

    def runTest(self):
        run = Endpoints_Articles(env='online')
        run.test_articles_api_base_view()
        run.test_articles_api_type_view()


class Endpoints_Indexer(HTTPEndpoints):
    def test_indexer_base(self):
        """
    Test Indexer Base endpoint
    """
        _VERSION = "v04"
        print "Running test_indexer_base"

        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/indexer"

        response = get_curling(base_url)
        test_integrity(response)

        print "Counted keywords: " + str(json.loads(response)['n_indexed'])

    def runTest(self):
        run = Endpoints_Indexer(env='online')
        run.test_indexer_base()


class Endpoints_N3(HTTPEndpoints):
    def test_n3_endpoints(self):
        """
    Test the N3
    """
        print "Running test_n3_endpoints"
        env = self.test_env

        base_url_resource = _ENV[env]['_SERVICE'] + "/data/webresource"
        base_url_concept = _ENV[env]['_SERVICE'] + "/data/concept"

        test_concepts = []

        # retrieve a test sample from the api
        sample = get_curling(_ENV[env]['_SERVICE'] + '/')
        sample = json.loads(sample)
        # pass the id of the sample in the N3 endpoint
        uuids = [s['uuid'] for s in sample['articles'][0:4]]  # pick a random article id in the response

        # print the resulting ntriples
        [get_curling(url=base_url_resource + '/' + str(u), display=True) for u in uuids]

        assert True

    def runTest(self):
        run = Endpoints_N3(env='online')
        run.test_n3_endpoints()


if __name__ == '__main__':
    two = Endpoints_Articles()
    two.runTest()
    three = Endpoints_Indexer()
    three.runTest()
    four = Endpoints_N3()
    four.runTest()