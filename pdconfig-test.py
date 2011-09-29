#!/usr/bin/env python

import os
import sys
import pdconfig
import pdtest

#
# Test Data
#
KV = dict([('key1',      '/some/path/on/disk'),
           ('include_1', '/include1/path/on/disk'),
           ('include_2', '/include2/path/on/disk'),
           ('include_3', '/include3/path/on/disk'),
           ('include_4', '/include4/path/on/disk'),
           ('include_5', '/include5/path/on/disk'),
           ('key2',      'the value for key2')])
FILE_TEXT = '[install]\n%s' % '\n'.join(['%s = %s' % (k,v) \
                                          for k,v in KV.items()])
FILE_NAME = 'pdconfig.test1.cfg'

def verifyItems(cfg, items):
    for k, v in items:
        if cfg[k] != v:
            raise pdtest.Unexpected(k, v, cfg[k])

@pdtest.passfail
def readBasic(filename):
    cfg = pdconfig.PdConfigParser(filename)
    verifyItems(cfg, KV.items())
    return cfg

@pdtest.passfail
def setRead(cfg):
    items = [('set%d' % d,'set value%d' % d) for d in range(10)]
    for k,v in items:
        cfg.set(k, v)
    verifyItems(cfg, items)

@pdtest.passfail
def setmRead(cfg):
    key = 'setm'
    items = ['setm_value%d' % d for d in range(1, 10)]
    cfg.setm(key, items)

    got = cfg.getm(key)
    got.sort()
    if got != items:
        raise pdtest.Unexpected(k, items, ', '.join(got))

@pdtest.passfail
def unsetRead(cfg):
    items = [('unset%d' % d,'unset value%d' % d) for d in range(10)]
    for k,v in items:
        cfg.set(k, v)

    for i, (k, v) in enumerate(items[:]):
        if i % 2:
            cfg.unset(k)
            items.remove((k,v))

    verifyItems(cfg, items)

@pdtest.passfail
def unsetmRead(cfg):
    key = 'unsetm'
    items = ['unsetm_value%d' % d for d in range(1, 20)]

    cfg.setm(key, items)
    cfg.unsetm(key)

    got = cfg.getm(key)
    if got:
        raise pdtest.Unexpected(k, '[]', str(got))

def test():
    fd = None
    try:
        fd = open(FILE_NAME, 'w+')
        fd.write(FILE_TEXT)
    finally:
        if fd:
            fd.close()

    cfg = readBasic(FILE_NAME)
    setRead(cfg)
    setmRead(cfg)
    unsetRead(cfg)
    unsetmRead(cfg)

    os.remove(FILE_NAME)

if __name__ == '__main__':
    test()
