"""
Main entrypoint for the Articles Semantic API.
Publishing at http://hypermedia.projectchronos.eu

FORKED FROM https://github.com/mr-niels-christensen/rdflib-appengine/blob/master/src/example/httpserver.py
"""

__author__ = ['niels', 'lorenzo']

import os
import sys
sys.path.insert(0, 'lib')

import webapp2
from webapp2 import RedirectHandler


# * generic tools are in tools.py module
# * tools using Graph() and NDBstore are in graphtools.py module
# * handlers are in the handlers/ package

#
# all the static variables are in config/config.py
#
from config.config import _PATH, _DEBUG

#
# utilities that are used inside handlers are in flankers/
#

#
# handlers loaded from handlers/
#
from handlers.articlesjsonapi import ArticlesJSONv1
from handlers.servicehandlers import DataStoreOperationsAPI
from handlers.dataN3 import PublishWebResources
from handlers.triplestoreservice import DataToTriplestore


class Testing(webapp2.RequestHandler):
    """
    /test: test handler
    """
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        self.response.out.write('Done')
#
### Handlers Order:
# 1. Test handler
# 2. Datastore Operations private API
# 2b.Datastore to Triplestore service
# 3. NTriples API (WebResource)
# 4. NTriples API (Taxonomy concepts)
# 5. NTriples API (Taxonomy DBpedia terms)
# 6. Keywords Filter-By JSON API
# 7. Filtering over resources (wikislugs, missions, events...) JSON API
# 8. Articles Index (filtered) JSON API
# 9. Articles Index JSON API
# 10. Articles Filter-By JSON API
# 11. Articles Base JSON API
#

application = webapp2.WSGIApplication([
    webapp2.Route('/test', Testing),
    webapp2.Route('/articles/v04', RedirectHandler, defaults={'_uri': '/'}),
    webapp2.Route('/articles/v04/', RedirectHandler, defaults={'_uri': '/'}),
    webapp2.Route('/datastore/<name:[a-z]+>', DataStoreOperationsAPI),
    webapp2.Route('/data/webresource/<key:[a-zA-Z0-9-_=]+>', PublishWebResources),
    webapp2.Route('/triplestore/<perform:[a-z]+>', DataToTriplestore),
    webapp2.Route('/keywords/filterby', ArticlesJSONv1),
    webapp2.Route('/resources/filterby', ArticlesJSONv1),
    webapp2.Route('/indexer/filterby', ArticlesJSONv1),
    webapp2.Route('/indexer', ArticlesJSONv1),
    webapp2.Route('/filterby', ArticlesJSONv1),
    webapp2.Route('/', ArticlesJSONv1, name='entrypoint'),
], debug=_DEBUG)

