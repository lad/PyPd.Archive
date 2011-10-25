#!/usr/bin/env python

import os
import sys
import collections
import pdplatform
import pdconfig

class PdIncludes:

    def __init__(self, dirs, populate = True, cache = False):
        if isinstance(dirs, str):
            raise TypeError('"dirs" argument should be an iterable of ' \
                            'directories.')
        self._dirs = dirs
        self._files = collections.defaultdict(set)
        if populate:
            self.populate()
        # TODO use a cache file

    def populate(self):
        for rootdir in self._dirs:
            for root, dirs, files in os.walk(rootdir):
                for f in files:
                    if f.endswith('.pd') or f.endswith('.dll'):
                        name = os.path.splitext(f)[0]
                        self._files[name].add(root)

    def __contains__(self, path):
        return os.path.splitext(path)[0] in self._files

    def __getitem__(self, key):
        val = self.get(key)
        if not val:
            raise KeyError("'%s'" % str(key))
        return val

    def get(self, key):
        val = self._files[key]
        if not val:
            keydir = os.path.dirname(key)
            if keydir:
                k = os.path.basename(key)
                dirs = self._files[k]
                for valdir in dirs:
                    if os.path.basename(valdir) == keydir:
                        return [valdir]
        return val

    def __str__(self):
        return '\n'.join(self._dirs)

def extra():
    cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
    pd_root = cfg.get('pd_root')
    exdir = os.path.join(pd_root, 'extra')
    return PdIncludes([exdir])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
        pd_root = cfg.get('pd_root')
        exdir = os.path.join(pd_root, 'extra')
        inc = PdIncludes([exdir])

        for name in sys.argv[1:]:
            dirs = inc.get(name)
            if dirs:
                for d in dirs:
                    print name,d
