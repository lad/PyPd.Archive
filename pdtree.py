#!/usr/bin/env python

""" A tree data structure oriented towards storing Pd objects. """

import collections
import pdtest

(CHILDREN_ONLY, DEPTH_FIRST, BREADTH_FIRST) = range(3)

class SimpleTree(object):
    """This simple tree abstraction dispenses with the notion of separate
       tree and node classes, and uses a single class for both. All nodes
       in the tree are instances of Simpletree."""

    def __init__(self, value = None):
        (self.value, self._children) = (value, [])

    def __len__(self):
        return len(self._children)

    def __getitem__(self, i):
        if isinstance(i, slice):
            indices = i.indices(len(self._children))
            return [self._children[i] for i in range(*indices)]
            #raise NotImplementedError('PdTree does not support slices')
        return self._children[i]

    def iter(self, order):
        if order == CHILDREN_ONLY:
            return iter(self._children)
        elif order == DEPTH_FIRST:
            return self._depth_first_iter()
        elif order == BREADTH_FIRST:
            return self._breadth_first_iter()
        else:
            raise ValueError('Unknown order type: "%s"' % str(order))

    def _depth_first_iter(self):
        # The root node may be anonymous, if not yield it.
        if self.value is not None:
            yield self

        # Use a stack instead of recursion.
        child_stack = collections.deque(reversed(self._children))
        while True:
            try:
                child = child_stack.pop()
            except IndexError:
                return

            yield child
            if child._children:
                child_stack.extend(reversed(child._children))

    def _breadth_first_iter(self):
        # The root node may be anonymous, if not yield it.
        if self.value is not None:
            yield self

        this_level = self._children

        while this_level:
            next_level = []
            for sib in this_level:
                #yield sib.value
                yield sib
                if sib._children:
                    next_level.extend(sib._children)

            this_level = next_level

    def apply(self, order, fn):
        for node in self.iter(order):
            fn(node)

    def add(self, value):
        t = SimpleTree(value)
        self._children.append(t)
        return t

@pdtest.passfail
def testTraverse():
    def add_vals(tr, vals):
        for (n, children) in vals:
            b = tr.add(n)
            if children:
                add_vals(b, children)

    tree = SimpleTree()
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
    depth_matches = (DEPTH_FIRST,
                   [1, 2, 3, 11, 12, 4, 5, 6, 21, 22, 23, 31, 32, 33, 24, 7])
    breadth_matches = (BREADTH_FIRST,
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
    child_matches = (tree, CHILDREN_ONLY, root_child_values)
    node23_matches = (node23, CHILDREN_ONLY, [31, 32, 33])

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
