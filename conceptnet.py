from functools import lru_cache
from urllib.parse import urlencode

import requests

import cache_util
import generator_util

URL = "http://api.conceptnet.io/c/en/{}?"

_LOCATION_ARGUMENTS = cache_util.HashableDict(
    rel="/r/AtLocation",
    limit=100
)
_HASA_ARGUMENTS = cache_util.HashableDict(
    rel="/r/HasA",
    limit=200
)
_DEFAULT_ARGUMENTS = cache_util.HashableDict(
    limit=200
)

# HELPERS
_PROHIBITED_SEARCH_TERMS = "a", "your", "my", "her", "his", "its", "their", "be", "an", "the", "you", "are"


def _remove_prohibited_words(word):
    return [part for part in word.split(" ") if part not in _PROHIBITED_SEARCH_TERMS]


def normalise(word):
    return " ".join(_remove_prohibited_words(word)).lower()


@lru_cache(maxsize=20)
def _get_data(word, arguments=None):
    if not arguments:
        arguments = _DEFAULT_ARGUMENTS
    splitted_word = _remove_prohibited_words(word)
    search_term = "_".join(splitted_word)
    url = URL.format(search_term) + urlencode(arguments, False, "/")
    return requests.get(url).json()


def _get_edges(word, arguments=None):
    return _get_data(word, arguments)["edges"]


def _get_weight_and_word(edge, word):
    end_label = edge["end"]["label"]
    if not end_label == word:
        return edge["weight"], end_label


def _get_relation_label(edge):
    return edge["rel"]["label"]


def _get_from_relation(word, edges, relation_name):
    return [_get_weight_and_word(edge, word) for edge in edges if _get_relation_label(edge) == relation_name]


# EXTRACTING INFO

def get_weighted_related_words(word, limit=50):
    edges = _get_edges(word, cache_util.HashableDict(limit=limit))
    return [(edge["weight"], edge["end"]["label"]) for edge in edges if edge["end"]["label"] != word]


def get_weighted_related_locations(word):
    edges = _get_edges(word, _LOCATION_ARGUMENTS)
    return _get_from_relation(word, edges, "AtLocation")


def get_weighted_has(word):
    edges = _get_edges(word, _HASA_ARGUMENTS)
    return _get_from_relation(word, edges, "HasA")


def get_weighted_properties(word):
    edges = _get_edges(word)
    return _get_from_relation(word, edges, "HasProperty")


def get_weighted_antonyms(word):
    edges = _get_edges(word)
    return _get_from_relation(word, edges, "Antonym")


# pp.pprint(get_weighted_related_words("cat", 45))


related_location_generator = generator_util.create_weighted_generator(get_weighted_related_locations)
