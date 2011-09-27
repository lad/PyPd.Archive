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
    def reset(self):
        self.tab = 0
    def __call__(self, pd_line):
        if pd_line.obj_id == 0:
            self.tab += self.ts
        print '%-6s%s%s' % (str(pd_line.obj_id),
                            ' ' * self.tab, str(pd_line.o))
                            #' ' * self.tab, pd_line.o.name())
        if pd_line.o.element == 'restore':
            self.tab -= self.ts

class AccumlateOutput(object):
    """Callable class which generates a list of the abstractions found in
       the patch file and stores them in different ways.
       to search a list of directories for the unknown abstractions."""

    MISSING = '** MISSING **'

    def __init__(self, dirs, action, pd_root = None):
        cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
        if not pd_root:
            pd_root = cfg.get('pd_root')

        include_dirs = [os.path.join(pd_root, 'extra')] + \
                       cfg.get_startswith('include') + dirs

        self.extra = pdextra.Extras(include_dirs)
        self.extra.populate()
        self.action = action
        self.unknowns = {}
        self.depends = set()
        self.missing = set()

    def reset(self):
        self.unknowns = {}

    def __call__(self, pd_line):
        if not pd_line.o.known:
            name = pd_line.o.name()
            d = name.split('/')[-1]
            paths = self.extra.files.get(d)
            if self.action == EXTRAS:
                if not paths:
                    paths = [self.MISSING]
                self.unknowns[name] = list(paths)
            elif self.action == DEPENDS:
                if not paths:
                    paths = ['%s "%s"' % (self.MISSING, d)]
                self.depends.update(list(paths))
            elif self.action == MISSING and not paths:
                self.missing.add(name)

    def __str__(self):
        if self.action == EXTRAS:
            return '\n'.join(['%-20s%s' % (name, ' '.join(paths)) \
                            for (name, paths) in self.unknowns.items()])
        elif self.action == DEPENDS:
            return '\n'.join(self.depends)
        elif self.action == MISSING:
            return '\n'.join(self.missing)

def examples():
    print """
TODO EXAMPLES
"""
    sys.exit(1)

def usage():
    print """
Usage: %s [-p pd-install-dir] [-i include-dir] [-i include-dir] ...
       {-e | -m | -t | -d} file1.pd [file2.pd] ...
where:
       -e   Print objects found in the patch file which are not known to
            PD vanilla.
       -m   Print objects not found in any search directory.
       -t   Print a tree of the structure of the patch file.
       -d   Print a list of the directories needed for the abstractions used
            in the patch file.
       -i   Add a directory to the list of directories that will be searched
            when objects are found in the patch file which are not known to
            PD vanilla.
       -p   Override the pd install dir value from the user's prefs file
            (%s).
       -h   Prints this help
       -x   Print some examples.
""" % (os.path.basename(sys.argv[0]), pdplatform.pref_file)
    sys.exit(1)


##### MAIN #####


if __name__ == '__main__':
    try:
        options, args = getopt.getopt(sys.argv[1:],
                "emtdi:p:hx", ["extra", "missing", "tree", "dependencies",
                               "include=", "pd=", "help", "examples"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    (EXTRAS, MISSING, TREE, DEPENDS) = range(1, 5)
    (action, include_dirs, pd_root) = (None, [], None)

    for opt,arg in options:
        if opt in ('-e', '--extras'):
            if action:
                usage()
            action = EXTRAS
        if opt in ('-m', '--missing'):
            if action:
                usage()
            action = MISSING
        elif opt in ('-t', '--tree'):
            if action:
                usage()
            action = TREE
        elif opt in ('-d', '--dependencies'):
            if action:
                usage()
            action = DEPENDS
        elif opt in ('-i', '--include'):
            include_dirs.append(os.path.realpath(arg))
        if opt in ('-p', '--pd'):
            pd_root = os.path.realpath(arg)
        elif opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-x', '--examples'):
            examples()

    if not args or not action:
        usage()

    if action in (EXTRAS, DEPENDS, MISSING):
        # Add the directory containing the patch file to the search dirs
        out = AccumlateOutput(include_dirs, action, pd_root = pd_root)
    elif action == TREE:
        out = OutputTree()
    else:
        usage()
        sys.exit(1)

    try:
        output_name = len(args) > 1
        for fname in args:
            out.reset()
            if output_name:
                print '\n%s' % fname

            f = pd.PdFile(fname)
            f.tree.applyDF(out)
            if action != TREE:
                print out
    except Exception, ex:
        print 'File:', fname
        traceback.print_exc(ex)
