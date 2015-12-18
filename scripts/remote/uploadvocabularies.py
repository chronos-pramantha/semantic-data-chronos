"""
Dumps vocabularies into remote datastore with POST requests.
Usage examples:
    python uploadvocabularies.py http://localhost:10080/sparql
    python uploadvocabularies.py http://localhost:8080/sparql
    python uploadvocabularies.py http://chronostriples.appspot.com/sparql
"""

__author__ = ['lorenzo', 'niels']

import sys
import urllib

from remote import post_curling
from config.config import _VOCS, _VOC_GRAPH_ID
from config.secret import _CLIENT_TOKEN


def _upload_all(url):
    """
    Fetch the vocabularies from taxonomy.projectchronos.eu and dump them into
    the GraphShard via POST on `/sparql` handler
    :param url: the url of the server where the `/sparql` endpoint is working
    :return:
    """
    for k, v in _VOCS.items():
        # fetch the vocabulary in NTRIPLES
        triples = urllib.urlopen(v)
        # dump the vocabulary via `/sparql`
        post_curling(url, {'token': _CLIENT_TOKEN, 'triple': triples.read(),
                           'graph_id': _VOC_GRAPH_ID}, display=True)

        # spot the `owl:sameAs` links and serialize to NTRIPLES
        linked = find_sameas_links(k, url)
        # dump the `owl:sameAs` links in the vocabulary
        post_curling(url, {'token': _CLIENT_TOKEN, 'triple': linked,
                           'graph_id': _VOC_GRAPH_ID}, display=True)


def find_sameas_links(voc, url):
    """
    From a JSON-LD vocabulary, spot the `owl:sameAs` link in the entities and
    dump the relations in the GraphShard.

    Example of result:
        <http://ontology.projectchronos.eu/astronomy/Planetary_system>
        <http://ontology.projectchronos.eu/chronos/relConcept>
        <http://graph.projectchronos.eu/data/concept/<concept label>>

    :param voc: slug of the vocabulary (astronomy, engineering, ...)
    :param url: a url to a vocabulary in JSON-LD
    :return:
    """
    from flankers.textsemantics import TextSemantics

    jsonld = urllib.urlopen(url + '?format=jsonld')  # add the parameter

    result = str()
    subject = '<http://ontology.projectchronos.eu/{}/{}>'.format(voc)
    predicate = '<http://ontology.projectchronos.eu/chronos/relConcept>'
    object = '<http://graph.projectchronos.eu/data/concept/{}>'

    # get the JSON-LD from ontology
    # for entity:
    #     get the sameAs
    #     fetch the sameAs from taxonomy
    #     if `relatedConcepts` != 0:
    #         for `relatedConcepts` from JSON:
    #             create triples for each related concept
    #     else: perform textsemantics.py on `abstract`
    #               semantics = TextSemantics(abstract)
    #               labels = semantics.find_related_concepts()
    #               create triple for each label
    #     concatenate triple to result

    return result


if __name__ == "__main__":
    _upload_all(sys.argv[1])

