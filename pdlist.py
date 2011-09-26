#!/usr/bin/env python

"""Utility for examaning the contents of PD patch files. Main features are:
   . List the objects in the patch file in a tree style.
   . List the abstractions used in the patch file and where the directories
     their locations.
   . List the directories references by any abstractions in the patch file."""

import sys
import os
import traceback
import getopt
import pd
import pdextra
import pdplatform
import pdconfig

class OutputTree(object):
    """Callable class for a simple tree style output. An object of the class
       should be called for each line in the patch file."""
    def __init__(self, tabstop = 2):
        self.tab = 0
        self.ts = tabstop
    def __call__(self, pd_line):
        if pd_line.obj_id == 0:
            self.tab += self.ts
        print '%-6s%s%s' % (str(pd_line.obj_id),
                            ' ' * self.tab, pd_line.o.name())
        if pd_line.o.element == 'restore':
            self.tab -= self.ts

class AccumlateUnknown(object):
    """Callable class which generates a list of all abstractions in the patch
       file which are not known to PD. Also uses the pdextra.Extra class
       to search a list of directories for the unknown abstractions."""

    def __init__(self, dirs, pd_root = None):
        cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
        if not pd_root:
            pd_root = cfg.get('pd_root')

        include_dirs = [os.path.join(pd_root, 'extra')] + \
                       cfg.get_startswith('include') + dirs

        self.extra = pdextra.Extras(include_dirs)
        self.extra.populate()
        self.unknowns = {}

    def __call__(self, pd_line):
        if not pd_line.o.known:
            name = pd_line.o.name()
            d = name.split('/')[-1]
            paths = self.extra.files.get(d) or ['** MISSING **']
            self.unknowns[name] = paths

    def __str__(self):
        return '\n'.join(['%-20s%s' % (name, ' '.join(paths)) \
                          for (name, paths) in self.unknowns.items()])

def usage():
    print """
Usage: %s [-p pd-install-dir] [-i include-dir] [-i include-dir] ...
       {-u | -t | -d} file1.pd [file2.pd] ...
where:
       -p   Override the pd install dir value from the user's prefs file
            (%s).
       -i   Add a directory to the list of directories that will be searched
            when unknown objects are found in the patch file.
       -u   Print unknown objects found in the patch file.
       -u   Print a tree of the structure of the patch file.
       -d   Print a list of the directories needed for the abstractions used
            in the patch file.
""" % (os.path.basename(sys.argv[0]), pdplatform.pref_file)


##### MAIN #####


if __name__ == '__main__':
    try:
        options, args = getopt.getopt(sys.argv[1:],
                "p:i:utdh", ["pd=", "include=", "unknown", "tree",
                           "dependencies", "help"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    (pd_root, include_dirs, unknown, tree, depend) = (None, [], False, False,
                                                      False)

    for opt,arg in options:
        if opt in ('-p', '--pd'):
            pd_root = os.path.realpath(arg)
        elif opt in ('-t', '--tree'):
            tree = True
        elif opt in ('-u', '--unknown'):
            unknown = True
        elif opt in ('-d', '--dependencies'):
            depend = True
        elif opt in ('-i', '--include'):
            include_dirs.append(os.path.realpath(arg))
        elif opt == '-h':
            usage()
            sys.exit(0)

    if not args:
        usage()
        sys.exit(1)

    if unknown or depend:
        # Add the directory containing the patch file to the search dirs
        out = AccumlateUnknown(include_dirs, pd_root = pd_root)
    elif tree:
        out = OutputTree()
    else:
        usage()
        sys.exit(1)

    try:
        output_name = len(args) > 1
        for fname in args:
            if output_name:
                print '\n%s' % fname

            f = pd.PdFile(fname)
            f.tree.applyDF(out)
            if unknown:
                print out
            elif depend:
                s = set()
                for val in out.unknowns.values():
                    for v in val:
                        s.add(v)

                print '\n'.join(s)
    except Exception, ex:
        print 'File:', fname
        traceback.print_exc(ex)
