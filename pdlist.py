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
import pdplatform
import pdconfig
import pdincludes

(VANILLA, EXTENDED, MISSING, TREE, DEPEND) = range(1, 6)


class PdOpts(object):
    MULTI_OPTS_ERR = 'Please specify one of {-v|-e|-m|-t|-d}'
    def __init__(self, argv):
        self.argv = argv
        options, self.args = getopt.getopt(argv[1:],
                'vemtdi:p:nhx', ['vanilla', 'extended', 'missing', 'tree',
                                'depend', 'include=', 'pd=', 'nonames',
                                'help', 'examples'])

        self.action = None
        self.include_dirs = []
        self.pd_root = None
        self.print_names = True

        for opt,arg in options:
            if opt in ('-v', '--vanilla'):
                if self.action:
                    raise getopt.GetoptError(self.MULTI_OPTS_ERR)
                self.action = VANILLA
            if opt in ('-e', '--extended'):
                if self.action:
                    raise getopt.GetoptError(self.MULTI_OPTS_ERR)
                self.action = EXTENDED
            elif opt in ('-m', '--missing'):
                if self.action:
                    raise getopt.GetoptError(self.MULTI_OPTS_ERR)
                self.action = MISSING
            elif opt in ('-t', '--tree'):
                if self.action:
                    raise getopt.GetoptError(self.MULTI_OPTS_ERR)
                self.action = TREE
            elif opt in ('-d', '--depend'):
                if self.action:
                    raise getopt.GetoptError(self.MULTI_OPTS_ERR)
                self.action = DEPEND
            elif opt in ('-i', '--include'):
                self.include_dirs.append(os.path.realpath(arg))
            elif opt in ('-p', '--pd'):
                self.pd_root = os.path.realpath(arg)
            elif opt in ('-n', '--nonames'):
                self.print_names = False
            elif opt in ('-h', '--help'):
                self.usage()
            elif opt in ('-x', '--examples'):
                self.examples()

        if not self.args or not self.action:
            raise getopt.GetoptError('No options given.')
        elif self.action in (VANILLA, EXTENDED) and self.include_dirs:
            raise getopt.GetoptError('-i is not valid with -v or -e')

    @staticmethod
    def usage(argv0 = None):
        # Check like this to handle being imported
        if not argv0:
            argv0 = sys.argv[0]
        print """
Usage: %s [OPTION]... [FILE]...
Show information about the Pure data patch file given in FILE.

Options:
-v, --vanilla     Print objects found in the patch file which are not known
                  to PD vanilla. If the patch is compatible with PD vanilla
                  no output is shown.
-e, --extended    Print objects found in the patch file which are not known
                  to PD extended. If the patch is compatible with PD extended
                  no output is shown.
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
""" % (os.path.basename(argv0), pdplatform.pref_file)

    def examples(self):
        print """
pdlist examples
---------------

...todo...

"""


##### MAIN #####


if __name__ == '__main__':

    # First get options and args...

    try:
        opts = PdOpts(sys.argv)
    except getopt.GetoptError, err:
        print str(err)
        PdOpts.usage()
        sys.exit(1)

    if not opts.pd_root:
        cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
        opts.pd_root = cfg.get('pd_root')
    opts.include_dirs.append(os.path.join(opts.pd_root, 'extra'))

    inc = pdincludes.PdIncludes(opts.include_dirs)
    exit_codes = []

    if not opts.print_names:
        if opts.action in (DEPEND, MISSING):
            summry_output = set()

    for fname in opts.args:
        try:
            if opts.print_names:
                print '%s' % fname,

            f = pd.PdFile(fname, inc)
            if opts.action == TREE:
                if opts.print_names:
                    print
                for (node, obj_id, level) in f.patch:
                    print '%s%s' % (' ' * (level * 4), node.value.name())

                exit_codes.append(0)

            elif opts.action == VANILLA:
                names = set([node.value.name() for (node, obj_id, level) in \
                             f.patch.select(vanilla = False)])
                if names:
                    if opts.print_names:
                        print 'is not pd-vanilla compatible. Missing:'
                    for name in names:
                        print '\t',name
                elif opts.print_names:
                    print 'is vanilla compatible'

                exit_codes.append(bool(names))

            elif opts.action == EXTENDED:
                names = set([node.value.name() for (node, obj_id, level) in \
                             f.patch.select(known = False)])
                if names:
                    if opts.print_names:
                        print 'is not pd-extended compatible. Missing:'
                    for name in names:
                        print '\t',name
                elif opts.print_names:
                    print 'is pd-extended compatible'

                exit_codes.append(bool(names))

            elif opts.action == MISSING:
                names = set([node.value.name() for (node, obj_id, level) in \
                             f.patch.select(known = False)])
                if opts.print_names:
                    print
                    for name in names:
                        print '\t',name
                else:
                    summry_output.update(names)

                exit_codes.append(bool(names))

            elif opts.action == DEPEND:
                def fn(node_id_level):
                    return bool(node_id_level[0].value.include)

                includes = set([node.value.include \
                                for (node, o, l) in filter(fn, f.patch) \
                                for node.value.include in node.value.include])

                if opts.print_names:
                    print
                    if includes:
                        print '    %s' % '\n    '.join(includes)
                elif includes:
                    summry_output.update(includes)

                exit_codes.append(0)

        except Exception, ex:
            if opts.print_names:
                print
            print '***** Failed to parse file "%s"' % fname
            print str(ex)
            exit_codes.append(1)
            #traceback.print_exc(ex)

    if not opts.print_names and opts.action in (DEPEND, MISSING):
        out = list(summry_output)
        out.sort()
        print '\n'.join(out)

    # Exit with 0 for success or 1 for error
    sys.exit(any(exit_codes))
