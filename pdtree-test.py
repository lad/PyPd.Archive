#!/usr/bin/env python

""" Tests for pdtree.py """

import pdtest
import pdtree

TEST_VALS = [(1, None),
             (2, None),
             (3, [(11,  None), (12, None)]),
             (4, None),
             (5, None),
             (6, [(21, None), (22, None),
                  (23, [(31, None), (32, None), (33, None)]), (24, None)]),
             (7, None)]

def add_vals(tr, vals):
    for (n, children) in vals:
        b = tr.add(n)
        if children:
            add_vals(b, children)

@pdtest.passfail
def testTraverse():
    tree = pdtree.SimpleTree()
    add_vals(tree, TEST_VALS)

    # A depth/breadth first search should yield these values in order
    depth_matches = (pdtree.DEPTH_FIRST,
                   [1, 2, 3, 11, 12, 4, 5, 6, 21, 22, 23, 31, 32, 33, 24, 7])
    breadth_matches = (pdtree.BREADTH_FIRST,
                     [1, 2, 3, 4, 5, 6, 7, 11, 12, 21, 22, 23, 24, 31, 32, 33])

    # Check both depth and breadth first

    for order, matches in [depth_matches, breadth_matches]:
        for tval, mval in zip(tree.iter(order), matches):
            if tval.value != mval:
                raise pdtest.Unexpected('node', mval, tval.value)
            if tval.value == 23:
                # Save node 23 for test below
                node23 = tval

    # children-only iterator

    expected = [1, 2, 3, 4, 5, 6, 7]
    child_matches = (tree, pdtree.CHILDREN_ONLY, expected)
    node23_matches = (node23, pdtree.CHILDREN_ONLY, [31, 32, 33])

    for node, order, matches in [child_matches, node23_matches]:
        for tval, mval in zip(node.iter(order), matches):
            if tval.value != mval:
                raise pdtest.Unexpected('node', mval, tval.value)

@pdtest.passfail
def testChild():
    tree = pdtree.SimpleTree()
    add_vals(tree, TEST_VALS)

    expected = [1, 2, 3, 4, 5, 6, 7]

    for i in range(len(tree)):
        if tree[i].value != expected[i]:
            raise pdtest.Unexpected('child value', str(expected[i]),
                                    str(tree[i].value))

@pdtest.passfail
def testSlice():
    tree = pdtree.SimpleTree()
    add_vals(tree, TEST_VALS)

    # Check basic slice notation

    expected = [1, 2, 3, 4, 5, 6, 7]

    match_nodes = tree[0:len(expected)]
    match = [node.value for node in match_nodes]
    if expected != match:
        raise pdtest.Unexpected('testSlice', str(expected), str(match))

    # Check extended slice notation

    expected = [2, 4, 6]
    match_nodes = tree[1:6:2]
    match = [node.value for node in match_nodes]
    if expected != match:
        raise pdtest.Unexpected('testSlice', str(expected), str(match))

@pdtest.passfail
def testInsert():
    tree = pdtree.SimpleTree()
    add_vals(tree, TEST_VALS)

    tree.insert(0, 0)
    subt = tree.insert(3, 25)
    subt.add(251)
    subt.add(252)
    subt.add(253)
    tree.insert(7, 55)

    match = []
    def p(node):
        match.append(node.value)

    # accumulate children only using apply and check results
    tree.apply(pdtree.CHILDREN_ONLY, p)
    expected = [0, 1, 2, 25, 3, 4, 5, 55, 6, 7]
    if expected != match:
        raise pdtest.Unexpected('testInsert', str(expected), str(match))

    # check for expected children
    expected = [0, 1, 2, 25, 3, 4, 5, 55, 6, 7]
    match = [n.value for n in tree.iter(pdtree.CHILDREN_ONLY)]
    if expected != match:
        raise pdtest.Unexpected('testInsert', str(expected), str(match))

    # check for expected children on sub-tree
    expected = [251, 252, 253]
    match = [n.value for n in subt.iter(pdtree.CHILDREN_ONLY)]
    if expected != match:
        raise pdtest.Unexpected('testInsert', str(expected), str(match))


def test():
    testTraverse()
    testChild()
    testSlice()
    testInsert()

if __name__ == '__main__':
    test()
