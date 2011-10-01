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
    """Callable class for a simple tree style output."""

    def __init__(self, tabstop = 2):
        self.ts = tabstop
        self.reset()

    def reset(self):
        self.tab = 0
        self.output = []

    def __call__(self, pd_line):
        if pd_line.obj_id == 0:
            self.tab += self.ts
        self.output.append('%-6s%s%s' % (str(pd_line.obj_id),
                                         ' ' * self.tab, pd_line.p.name()))
        if pd_line.p.element == 'restore':
            self.tab -= self.ts

    def __str__(self):
        return '\n'.join(self.output)

    def empty(self):
        return not self.output

class OutputAbstractions(object):
    """Callable class which generates a list of the abstractions found in
       the patch file and stores them in different ways."""

    MISSING = '** MISSING **'

    def __init__(self, dirs, action, pd_root = None):
        # Read the user prefs file and use pdextra.Extras() to generate a list
        # of all abstractions in the PD installation

        cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
        if not pd_root:
            pd_root = cfg.get('pd_root')

        include_dirs = cfg.getm('include') + dirs
        if pd_root:
            include_dirs.append(os.path.join(pd_root, 'extra'))

        self.extra = pdextra.Extras(include_dirs)
        self.extra.populate()
        self.action = action
        self.unknowns = {}
        self.depends = set()
        self.missing = set()

    def reset(self):
        self.unknowns = {}

    def __call__(self, pd_line):
        if not pd_line.p.known:
            name = pd_line.p.name()
            d = name.split('/')[-1]
            paths = self.extra.files.get(d)
            if self.action == EXTRA:
                if not paths:
                    paths = [self.MISSING]
                self.unknowns[name] = list(paths)
            elif self.action == DEPEND:
                if not paths:
                    paths = ['%s "%s"' % (self.MISSING, d)]
                self.depends.update(list(paths))
            elif self.action == MISSING and not paths:
                self.missing.add(name)

    def __str__(self):
        if self.action == EXTRA:
            return '\n'.join(['%-20s%s' % (name, ' '.join(paths)) \
                            for (name, paths) in self.unknowns.items()])
        elif self.action == DEPEND:
            return '\n'.join(self.depends)
        elif self.action == MISSING:
            return '\n'.join(self.missing)

    def empty(self):
        if self.action == EXTRA:
            return not self.unknowns
        elif self.action == DEPEND:
            return not self.depends
        elif self.action == MISSING:
            return not self.missing

def examples():
    print """
pdlist examples
---------------

...todo...

"""
    sys.exit(1)

def usage():
    print """
Usage: %s [OPTION]... [FILE]...
Show information about the Pure data patch file given in FILE.

Options:
  -e, --extra       Print objects found in the patch file which are not known
                    to PD vanilla.
  -m, --missing     Print objects not found in any search directory.
  -t, --tree        Print a tree of the structure of the patch file.
  -d, --depend      Print a list of the directories needed for the abstractions
                    used in the patch file.
  -i, --include     Add a directory to the list of directories that will be
                    searched when objects are found in the patch file which are
                    not known to PD vanilla.
  -p, --pd          Override the pd install dir value from the user's prefs
                    file (%s).
  -n, --nonames     Don't output filenames when multiple files are given.
  -h, --help        Prints this help
  -x, --examples    Print some examples.
""" % (os.path.basename(sys.argv[0]), pdplatform.pref_file)
    sys.exit(1)


##### MAIN #####


if __name__ == '__main__':

    # First get options and args...

    try:
        options, args = getopt.getopt(sys.argv[1:],
                'emtdi:p:nhx', ['extra', 'missing', 'tree', 'depend',
                                'include=', 'pd=', 'nonames', 'help',
                                'examples'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    (EXTRA, MISSING, TREE, DEPEND) = range(1, 5)
    (action, include_dirs, pd_root, print_names) = (None, [], None, True)

    for opt,arg in options:
        if opt in ('-e', '--extra'):
            if action:
                usage()
            action = EXTRA
        elif opt in ('-m', '--missing'):
            if action:
                usage()
            action = MISSING
        elif opt in ('-t', '--tree'):
            if action:
                usage()
            action = TREE
        elif opt in ('-d', '--depend'):
            if action:
                usage()
            action = DEPEND
        elif opt in ('-i', '--include'):
            include_dirs.append(os.path.realpath(arg))
        elif opt in ('-p', '--pd'):
            pd_root = os.path.realpath(arg)
        elif opt in ('-n', '--nonames'):
            print_names = False
        elif opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-x', '--examples'):
            examples()

    if not args or not action:
        usage()

    # Pick an output class based on the options given

    if action in (EXTRA, DEPEND, MISSING):
        # Add the directory containing the patch file to the search dirs
        out = OutputAbstractions(include_dirs, action, pd_root = pd_root)
    elif action == TREE:
        out = OutputTree()
    else:
        usage()
        sys.exit(1)

    # Run through each file. The output object gets applied to each node
    # in a tree of objects parsed from each file.

    try:
        if print_names and len(args) == 1:
            print_names = False
        for fname in args:
            out.reset()
            if print_names:
                print '\n%s' % fname

            f = pd.PdFile(fname)
            f.tree.applyDF(out)

            if not out.empty():
                print out
    except Exception, ex:
        print 'File:', fname
        traceback.print_exc(ex)
