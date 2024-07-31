from collections import defaultdict

"""
Source
https://stackoverflow.com/questions/19399032/accessing-key-in-factory-of-defaultdict
"""

flatten = lambda t: [item for sublist in t for item in sublist]


class ArgDefaultDict(defaultdict):
    def __missing__(self, key):
        if self.default_factory:
            dict.__setitem__(self, key, self.default_factory(key))
            return self[key]
        else:
            defaultdict.__missing__(self, key)
