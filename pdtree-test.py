#!/usr/bin/env python

""" Tests for pdtree.py """

import pdtest
import pdtree

@pdtest.passfail
def testTraverse():
    def add_vals(tr, vals):
        for (n, children) in vals:
            b = tr.add(n)
            if children:
                add_vals(b, children)

    tree = pdtree.SimpleTree()
    vals = [(1, None),
            (2, None),
            (3, [(11,  None), (12, None)]),
            (4, None),
            (5, None),
            (6, [(21, None), (22, None),
                 (23, [(31, None), (32, None), (33, None)]), (24, None)]),
            (7, None)]
    add_vals(tree, vals)

    # A depth/breadth first search should yield the values in this order
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

    # Check children-only iterator

    root_child_values = [1, 2, 3, 4, 5, 6, 7]
    child_matches = (tree, pdtree.CHILDREN_ONLY, root_child_values)
    node23_matches = (node23, pdtree.CHILDREN_ONLY, [31, 32, 33])

    for node, order, matches in [child_matches, node23_matches]:
        for tval, mval in zip(node.iter(order), matches):
            if tval.value != mval:
                raise pdtest.Unexpected('node', mval, tval.value)


    # Check child access

    for i in range(len(tree)):
        if tree[i].value != root_child_values[i]:
            raise pdtest.Unexpected('child value', str(root_child_values[i]),
                                    str(tree[i]))

    # Check slice access

    match_nodes = tree[0:len(root_child_values)]
    match = [node.value for node in match_nodes]
    if root_child_values != match:
        raise pdtest.Unexpected('root child values', str(root_child_values),
                                str(match))

def test():
    testTraverse()

if __name__ == '__main__':
    test()

