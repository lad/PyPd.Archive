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
    print 'Usage: %s [ -r <pd-install-dir> ] [ -i <dir> ] ...' % sys.argv[0]
    print 'where:'
    print '\t-r <pd-install-dir> saves the location of your PD installation'
    print '\t-i <dir> saves each directory and uses these to search for PD'
    print '\t         abstractions when parsing PD patch files'
    print '\t-u <key> removes <key> from the config fie'

if __name__ == '__main__':
    # Use getopt() for compatibility with older pythons
    try:
        options, args = getopt.getopt(sys.argv[1:],
                                      "r:i:u:h",
                                      ["root=", "include=", "unset=", "help"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    (pd_root, include_dirs, unset_keys) = (None, [], [])

    for opt,arg in options:
        if opt in ('-r', '--root'):
            pd_root = arg
        elif opt in ('-i', '--include'):
            include_dirs.append(os.path.realpath(arg))
        elif opt in ('-u', '--unset'):
            unset_keys.append(arg)
        elif opt in ('-h', '--help'):
            usage()
            sys.exit(0)

    # Check for trailing arguments and ensure at least one option was given
    if args or not (pd_root or include_dirs or unset_keys):
        usage()
        sys.exit(1)

    if not os.path.isdir(pdplatform.pref_dir):
        os.makedirs(pdplatform.pref_dir)

    cfg = pdconfig.PdConfigParser(pdplatform.pref_file)

    if pd_root:
        pd_root = os.path.realpath(pd_root)
        cfg.set('pd_root', pd_root)

    if include_dirs:
        cfg.setm('include', include_dirs)

    if unset_keys:
        for key in unset_keys:
            cfg.unset(key)
