#!/usr/bin/env python

import os
import collections
import pdplatform
import pdconfig

class Extras:

    def __init__(self, dirs, cache = False):
        self.dirs = dirs
        self.files = collections.defaultdict(set)
        # TODO use a cache file

    def populate(self):
        for rootdir in self.dirs:
            for root, dirs, files in os.walk(rootdir):
                for f in files:
                    if f.endswith('.pd') or f.endswith('.dll'):
                        name = os.path.splitext(f)[0]
                        self.files[name].add(root)


if __name__ == '__main__':
    cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
    e = Extras([os.path.join(cfg.get('pd_root'), 'extra')])
    e.populate()

    for name, paths in e.files.items():
        print '%-40s%s' % (name, ' '.join(paths))
