import unittest
from flankers.scrawler import Scrawler

__author__ = 'lorenzo'


class CrawlerTest(unittest.TestCase):
    """
    Test for crawling RSS-feeds. Use the run_test() method.
    """

    class mock_Item():
        """
        A mock class for the Item() model in the datastore
        """
        def __init__(self, t, l, pub, summ):
            from time import time, strptime, gmtime, struct_time
            self.title = str(t)
            self.link = str(l)
            from datetime import datetime
            self.stored = datetime(*gmtime(time())[:6])
            # parsing time.struct_time string into a tuple
            # there is for sure a better way to do it
            result = tuple((int(st.strip().split('=')[1])) for i, st in enumerate(pub[17:-1].split(',')))

            self.published = datetime(*result[:6])
            self.summary = summ

        def store(self):
            return {v: getattr(self, v) for v in dir(self) if not v.startswith('_') and not v == 'store'}

    def test_crawl_local(self):
        url = "http://localhost:8080/cron/startcrawling"
        from scripts.remote.remote import get_curling
        res = get_curling(url)
        print res

    def run_test(self):
        """
        Prints Feed object and multiple attributes if the Item() mock object
        """
        s = Scrawler()
        items = s.load_links()
        print items[0]
        for i in xrange(0, 1):
            try:
                item = s.read_feed(items[i])
            except ValueError:
                continue
            print item  # this is a list of feeds
            item = self.mock_Item(str(item['title']), str(item['link']), str(item['published_parsed']), str(item['summary'].encode('utf-8')))
            for k, v in item.store().items():
                print k+': ', v

            print "\n"

    def test_feedparser(self):
        import feedparser
        d = feedparser.parse('http://photojournal.jpl.nasa.gov/rss/new')
        print d

    def test_catch_summary(self):
        value = '''<table><tr>
<td><ahref="http://photojournal.jpl.nasa.gov/catalog/PIA19775"><imgalt=""border="0"height="100"src="http://photojournal.jpl.nasa.gov/thumb/PIA19775.jpg"style="vertical-align: middle;"width="122"/></a>\n\t\t\t\t\n\t\t\t\t</td>
\n\t\t\t\t<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n\t\t\t\t\t\t</td>
\n\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\tTarget: &nbsp;<ahref="http://solarsystem.nasa.gov/planets/profile.cfm?Object=Earth">Earth</a>\n\t\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<br/>Mission: &nbsp;\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<ahref="http://terra.nasa.gov">Terra</a>\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\t\n\n\t\t\t\t\t\t<br/>
Instrument: &nbsp;\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<ahref="http://asterweb.jpl.nasa.gov/">ASTER</a>\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t<br/>\n\t\t\t\t\t\n\t\t\t\t\tImageCredit: NASA/GSFC/METI/ERSDAC/JAROS,
                andU.S./JapanASTERScienceTeam\n\t\t\t\t\t</td>
</tr></table>\n\t\t\t\t\t<br/>'''
        from bs4 import BeautifulSoup
        import re

        body = BeautifulSoup(value, "lxml").body

        outlines1 = body.find(text=re.compile('.Target:'))

        print outlines1



    # look for media types: https://aerospaceblog.wordpress.com/feed/