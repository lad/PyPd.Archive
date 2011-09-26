#!/usr/bin/env python

import os
import sys
import getopt
import pdplatform
import pdconfig

"""Query the user for the PD root directory, save in user prefs file"""

def query_user():
    pd_root = raw_input('Enter the path to your PD installation: ')
    include_dirs = []
    while True:
        d = raw_input('Enter additional paths to PD directories (. to '
                      'finish): ')
        if d == '.':
            break
        else:
            include_dirs.append(d)

    return (pd_root, include_dirs)

def usage():
    print 'Usage: %s -r <pd-install-dir> [-i <dir>] ...' % sys.argv[0]
    print 'where:'
    print '\t<pd-install-dir> is the root directory of your PD installation'
    print '\t<dir> is any directory of PD abstractions'

if __name__ == '__main__':
    try:
        options, args = getopt.getopt(sys.argv[1:],
                                      "r:i:h", ["root=", "include=", "help"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    if not options and not args:
        (pd_root, include_dirs) = query_user()
    else:
        include_dirs = []
        for opt,arg in options:
            if opt in ('-r', '--root'):
                pd_root = arg
            elif opt in ('-i', '--include'):
                include_dirs.append(arg)
            elif opt in ('-h', '--help'):
                usage()
                sys.exit(0)

    if args:
        usage()
        sys.exit(1)

    pd_root = os.path.realpath(pd_root)
    include_dirs = [('include_%d' % (i + 1), os.path.realpath(inc_dir)) \
                    for (i, inc_dir) in enumerate(include_dirs)]

    if not os.path.isdir(pdplatform.pref_dir):
        os.makedirs(pdplatform.pref_dir)

    cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
    cfg.setm([('pd_root', pd_root)] + include_dirs)
