import numpy as np
import itertools
from heapq import heappush, heappop
from collections import defaultdict

class Vert:
    def __init__(self, pos, next=None, parent=None):
        self.pos = np.array(pos).copy()
        self.next = next
        self.parent = parent
        self.support = None

    def __eq__(self, other):
        if type(other) is tuple:
            return tuple(self.pos) == other
        else:
            return tuple(self.pos) == tuple(other.pos)

    def __hash__(self):
        return hash(tuple(self.pos))


class DNDict:
    '''Default dictionary with support for np.ndarray->tuple key conversion
    '''
    def __init__(self, default_func, insert_after_missing=False):
        self._missing = default_func
        self._dict = {}
        self.insert_after_missing = insert_after_missing

    def __delitem__(self, key):
        if type(key) is np.ndarray:
            key = tuple(key)
        if key in self._dict:
            del self._dict[key]

    def __getitem__(self, key):
        if type(key) is np.ndarray:
            key = tuple(key)
        if key in self._dict:
            return self._dict[key]
        else:
            ret = self._missing(key)
            if self.insert_after_missing:
                self[key] = ret
            return ret

    def __setitem__(self, key, obj):
        if type(key) is np.ndarray:
            key = tuple(key)
        self._dict[key] = obj


# mostly from https://docs.python.org/2/library/heapq.html
class PQ:
    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of vertexs to entries
        self.REMOVED = '<removed-vertex>'    # placeholder for a removed vertex
        self.counter = itertools.count()     # unique sequence count

    def __contains__(self, obj):
        if type(obj) is np.ndarray: obj = tuple(obj)
        return obj in self.entry_finder

    def top_key(self):
        while self.pq:
            if self.pq[0][-1] is self.REMOVED:
                heappop(self.pq)
            else:
                return self.pq[0][0]

    def push(self, obj, priority):
        'Add a new vertex or update the priority of an existing vertex'
        if type(obj) is np.ndarray: obj = tuple(obj)
        if obj in self.entry_finder:
            self.remove(obj)
        count = next(self.counter)
        entry = [priority, count, obj]
        self.entry_finder[obj] = entry
        heappush(self.pq, entry)

    def remove(self, obj):
        'Mark an existing vertex as REMOVED.  Raise KeyError if not found.'
        if type(obj) is np.ndarray: obj = tuple(obj)
        entry = self.entry_finder.pop(obj)
        entry[-1] = self.REMOVED

    def pop(self):
        'Remove and return the lowest priority vertex. Raise KeyError if empty.'
        while self.pq:
            priority, count, vertex = heappop(self.pq)
            if vertex is not self.REMOVED:
                del self.entry_finder[vertex]
                return vertex
        raise KeyError('pop from an empty priority queue')

    def __iter__(self):
        while self.top_key() is not None:
            yield self.pop()
