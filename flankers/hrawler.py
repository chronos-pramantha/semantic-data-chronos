import webapp2
from bs4 import BeautifulSoup
import feedparser

from config.config import _DEBUG

__author__ = 'Lorenzo'


class Hrawler(webapp2.RequestHandler):
    """
    Index `http://adsabs.harvard.edu` resources using the Chronos' Cloud
    """
    def get(self):
        """
        Handler for the cronjob: `/cron/hrawling`
        :return:
        """
        self.fetch_concept_and_store()

    def fetch_concept_and_store(self):
        """
        Loop through all the concepts in the datastore (using memcache) and
        fetch the results from ADS. Spot the link to RSS feed. Pass the feed to
        Scrawler. Store them flagged as 'paper'.

        Notes:
            http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&arxiv_sel=astro-ph&text=black+holes
            Get RSS feed for this query:
            href="http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?type=RSS&data_type=RSS&cookie=56705cb2d631026"

        :return:
        """
        pass


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/hrawling', Hrawler),
], debug=_DEBUG)
