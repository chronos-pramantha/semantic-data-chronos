from urlparse import urlparse
import json
import logging
from google.appengine.ext import ndb

__author__ = 'Lorenzo'

from handlers.basehandler import BaseHandler

webresource_prop_map = {
    'url': {
        'prop': 'http://schema.org/url',
        'type': 'https://schema.org/URL'
    },
    'title': {
        'prop': 'http://schema.org/headline',
        'type': 'https://schema.org/Text'
    },
    'abstract': {
        'prop': 'https://schema.org/about',
        'type': 'https://schema.org/Text'
    },
    'published': {
        'prop': 'http://schema.org/datePublished',
        'type': 'https://schema.org/DateTime'
    },
}


class PublishWebResources(BaseHandler):
    """
    GET data/webresource/<key>
    Serve datastore model WebResource as a NTRIPLES, for the purpose of the cloud.
    The data is served to graph.projectchronos.eu

    Linked Data to be served (JSON-LD format):
        {
          "@id": "http://graph.projectchronos.eu/data/webresource/<key>",
          "@type": [
              "http://ontology.projectchronos.eu/chronos/webresource",
              "https://schema.org/Article"
          ]
        }

    :return JSON-LD
    #todo: make it return N-Triples
    """
    def get(self, key):
        from datastore.models import WebResource

        try:
            # try if `key` is an ndb.Key
            key = ndb.Key(urlsafe=key)
            obj = key.get()
        except Exception:
            # if `key` is an id()
            key = ndb.Key(WebResource, int(key))
            obj = key.get()
        except:
            # wrong `key` or `id`
            obj = None

        if obj:
            url = str(obj.url)
            author = urlparse(url).netloc
            if obj.type_of == 'tweet' or obj.type_of == 'fb':
                # obj is a tweet
                schema_type = 'https://schema.org/SocialMediaPosting'
            elif obj.type_of == 'media' or obj.type_of == 'movie':
                # obj is link or media
                schema_type = 'https://schema.org/MediaObject'
            else:
                # obj is an article
                schema_type = 'https://schema.org/Article'

            result = {
                "@id": "http://graph.projectchronos.eu/data/webresource/" + key.urlsafe(),
                "@type": schema_type,
                "https://schema.org/author": {
                    '@value': author,
                    '@type': 'https://schema.org/Text'
                },
                "uuid": obj.key.id()
            }
            for k, v in webresource_prop_map.items():
                result[v['prop']] = {
                    '@value': obj.dump_to_json()[k],
                    '@type': v['type']
                }

            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.headers['Content-Type'] = "application/json"
            return self.response.out.write(
                json.dumps(
                    result,
                    indent=2
                )
            )

            #
            # Custom translation to ntriples (to be better designed)
            #
            results = str()
            for k in result.keys():
                if k != '@id':
                    results += '<' + result['@id'] + '>' # add subject
                    if isinstance(result[k], str):
                        results += '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' # predicate
                        results += '<' + result[k] + '> . ' # add object
                    else:
                        if result[k]['@value']:
                            results += '<' + k + '>' # add predicate
                            results += '<' + result[k]['@value'] + '> . ' # add object'''

            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.headers['Content-Type'] = "application/n-triples; charset=utf-8"
            return self.response.out.write(
                results
            )
        else:
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.headers['Content-Type'] = "application/json"
            return self.response.out.write(
                self.json_error_handler(404, exception='Wrong Format of NDB key or wrong resource ID')
            )






