import itertools
from collections import namedtuple

import FastGrid
from Util import Util
from Grid_3 import Grid
from SafeDict import SafeDict

CacheEntry = namedtuple('CacheEntry', ['hash_key', 'str_repr', 'score', 'hit_count'])


class Cache:
    """Stores information about grids"""

    def __init__(self):
        self.cache = SafeDict([])

    def contains_key(self, k: int) -> bool:
        if self.cache[k] is not None:
            return True
        return False

    def __getitem__(self, cache_key):
        return self.cache[cache_key]

    def __setitem__(self, cache_key, value):
        self.cache[cache_key] = value


class GridCache(Cache):
    def contains_grid(self, g: FastGrid) -> bool:
        if self.cache[hash(g)] is not None:
            return True
        return False

    def __getitem__(self, g: FastGrid):
        return self.cache[hash(g)]

    def __setitem__(self, g: FastGrid, value):
        self.cache[hash(g)] = value
