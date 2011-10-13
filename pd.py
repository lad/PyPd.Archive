#!/usr/bin/env python

""" Classes for reading, parsing and manipulating Pure Data (.pd) files:

    PdFile: opens and read Pd patch files
    PdPatch: parsed representation of a Pd patch file
    PdObject: parsed representation of each Pd element/object"""

import sys
import collections
import pdelement
import pdtree
from pdexceptions import *
import pdtest

__author__ = "Louis A. Dunne"
__copyright__ = "Copyright 2011, Louis A. Dunne"
__credits__ = ["Louis A. Dunne"]
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = "Louis A. Dunne"
__status__ = "Alpha"

# Some constants we need to recognize in the patch file
NCHUNK = '#N'
CCHUNK = '#C'
ACHUNK = '#A'
XCHUNK = '#X'
CANVAS = 'canvas'       # Since there are two different canvas definitions
CANVAS5 = 'canvas5'     # we need to distinguish them. CANVAS5/CANVAS6 are
CANVAS6 = 'canvas6'     # internal names only, never exposed.
RESTORE = 'restore'
CONNECT = 'connect'
STRUCT = 'struct'
OBJ = 'obj'
ARRAY_DATA = 'array-data'


class PdObject(object):
    def __init__(self, text, line_num):
        self.line_num = line_num
        params = text.split(' ')
        try:
            self.chunk = params[0]
            params = params[1:]

            # "#N canvas" or "#N struct"
            if self.chunk == NCHUNK:
                self.element = params[0]
                params = params[1:]
            # "#C restore"
            elif self.chunk == CCHUNK:
                self.element = params[0]
                params = params[1:]
                if self.element != RESTORE:
                    raise ValueError('Invalid chunk element combination: ' \
                                     '"%s %s"' % (self.chunk, self.element))
            # "#A array-data"
            elif self.chunk == ACHUNK:
                # Array data definitions don't have an element name, so we
                # use this as a placeholder
                self.element = ARRAY_DATA
            # "#X ..."
            elif self.chunk == XCHUNK:
                # every other object
                self.element = params[0]
                params = params[1:]
            else:
                raise ValueError('Unrecognized chunk type: "%s"' % self.chunk)

        except IndexError, ex:
            raise ValueError('Too few values to parse in "%s"' % text)

        (self.attr_names, self.attrs, self.extra_params, self.known) = \
                                    pdelement.get(self.element, params)

    @staticmethod
    def factory(lines):
        """This is a generator which takes lines of text from a patch file
           and assembles multiple lines into a single logical line. Each
           line is used to create a PdObject and then yielded to the caller."""

        (text, start_line_num) = ('', None)

        for line_num, line in enumerate(lines):
            line = line.rstrip('\n')
            if line and not line.isspace():
                if start_line_num is None:
                    # start a new object
                    text = line
                    start_line_num = line_num
                else:
                    # a contination line. make sure there's some space between
                    # this and the params of the previous line
                    if text[-1] != ' ':
                        text += ' '
                    text += line

                # The end-of-line ';' can be escaped with a preceeding '\'
                if len(text) > 1 and text[-1] == ';' and text[-2] != '\\':

                    # Now we have a full logical Pd object (drop the ";" char)
                    yield PdObject(text[:-1], start_line_num)

                    # When we come back into the generator we need start a new
                    # object
                    start_line_num = None

    def __getitem__(self, attr_name):
        """Access Pd attributes by name. Raises exception if not found."""
        if attr_name == 'element':
            return self.element
        elif attr_name == 'chunk':
            return self.chunk
        elif attr_name == 'known':
            return self.known
        else:
            return self.attrs[attr_name]

    def __setitem__(self, attr_name, attr_value):
        """First draft of a simple setitem.  We may need a lot of contraints
           here to prevent the patch becoming invalid.

           May also allow the constaints to be relaxed, perhaps in a
           transaction for bundling up a bunch of changes that would otherwise
           result in an invalid patch during the intermediate changes, but
           would be valid once all changes are complete."""

        if attr_name == 'element':
            self.element = attr_value
        elif attr_name == 'chunk':
            self.chunk = attr_value
        elif attr_name == 'known':
            raise AttributeError('Cannot set PdObject.known. It is a ' \
                                 'read-only value')
        else:
            self.attrs[attr_name] = attr_value
        return self

    def get(self, attr_name):
        """Access Pd attributes by name. Returns None if not found."""
        if attr_name == 'element':
            return self.element
        elif attr_name == 'chunk':
            return self.chunk
        elif attr_name == 'known':
            return self.known
        else:
            return self.attrs.get(attr_name)

    def __str__(self):
        """Returns a textual representation suitable for storing in a Pd
           patch file."""

        vals = [self.attrs[k] for k in self.attr_names \
                              if self.attrs[k] is not None]
        if self.extra_params:
            vals += self.extra_params

        # Special case for canvas and array-data
        if self.chunk == ACHUNK:
            return ' '.join([self.chunk] + vals)
        else:
            return ' '.join([self.chunk, self.element] + vals)

    def name(self):
        """Returns the element name or the object name if the element is an
           'obj'"""

        if self.element == OBJ:
            return self.attrs.get('type') or self.element
        elif self.element == CANVAS:
            return 'canvas %s' % self.get('name')
        else:
            return self.element


class PdPatch(object):
    """This is a container type abstraction for a Pure Data patch or sub-patch.
       These are represented by the Pd "canvas" type. All patch files start
       with a top-level canvas declaration, and may contain further canvas
       declarations to indicate sub-patches.

       Objects are accessed via their object-ids, which can change if objects
       are inserted or deleted. This is an unfortunate side-effect of the
       Pd patch file format. An additional problem is that object-ids are
       only unique within their own patch or sub-patch. Since all sub-patches
       restart object-ids at zero, there will be many objects with the same
       Pd object-id.

       An easier way to access specific objects is use the select() method
       specifying the attributes of the objects to match. Alternatively the
       filter built-in can be used with any callable to select objects.  See
       example in the documentation for the select() method."""

    def __init__(self, patch_text):
        """Create a PdPatch object from the textual description given in
           "patch_text"."""

        self._patch_text = patch_text

        factory = PdObject.factory(patch_text)

        # First line should be the canvas definition
        self.canvas = factory.next()
        if self.canvas.element != CANVAS:
            raise InvalidPdLine(text, line_num)

        # We need to store each object in a tree so that we can keep track
        # of sub-patches
        self._tree = pdtree.SimpleTree(self.canvas)

        cur_node = self._tree
        for obj in factory:
            if obj.element == CANVAS:
                branch = pdtree.SimpleTree(obj)
                cur_node.addBranch(branch)
                cur_node = branch
            elif obj.element == RESTORE:
                cur_node.add(obj)
                cur_node = cur_node.parent
            else:
                cur_node.add(obj)

    def __len__(self):
        return len(self._tree)

    def __getitem__(self, key):
        """Objects within a patch are accessed using their object IDs.  IDs
           start at zero for the first object in the patch, excluding the
           starting canvas definition.

           The first object in a sub-patch starts at ID zero again. The IDs in
           the parent patch take up where they left off when the sub-patch
           returns to its parent.

           To locate an object in a sub-patch you must first locate the
           canvas object for that sub-patch. See select() for an easier way to
           access objects.

           Slices are not supported, since in Pure Data terms a part of a patch
           would not be a valid patch. It would not start with a canvas
           definition and would not have correctly numbered object IDs. The
           exception would be a slice starting at the beginning of the patch,
           but this is not a common or useful way of accessing parts of a Pd
           patch."""

        if isinstance(key, slice):
            raise NotImplementedError('PdPatch does not support slices')

        return self._tree[i]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise NotImplementedError('PdPatch does not support slices')
        else:
            self._tree[i] = value

    def __delitem__(self, key):
        pass

    def __reversed__(self):
        """There's no point in reversing a patch."""

        raise NotImplementedError('PdPatch does not support reversed()')

    def __contains__(self, obj):
        for (node, obj_id, level) in self._tree:
            if node.value == obj:
                return True

        return False

    def __str__(self):
        return ';\r\n'.join(str(node.value) for node in self)

    def __iter__(self):
        # The object ids must be generated dynamically, as they change when
        # the tree is modified. The root node (a canvas object) and connect
        # object are given the id of -1 as they don't actually have ids in Pd
        # patches.
        obj_id = -1

        it = iter(self._tree)
        (node, level) = it.next()
        yield (node, obj_id, level)

        # Need to keep track of the object id as we move up and down levels
        # in the tree
        obj_id_stack = collections.deque()
        last_level = 1

        for (node, level) in it:
            if node.value.element == CONNECT:
                # Connect objects have no valid id
                yield (node, -1, level)
            else:
                # Work out the object-id
                if level == last_level:
                    obj_id += 1
                elif level == (last_level - 1):
                    # returning from sub-patch
                    obj_id = obj_id_stack.pop() + 1
                else:
                    # entering sub-patch
                    obj_id_stack.append(obj_id)
                    obj_id = 0

                last_level = level
                yield (node, obj_id, level)

    def apply(self, fn):
        return self._tree.apply(fn)

    def add(self, key, value):
        raise NotImplementedError('Not implemented yet')

    def insert(self, i, key, value):
        raise NotImplementedError('Not implemented yet')

    def select(self, **kwargs):
        selected = []
        for (node, obj_id, level) in self._tree:
            match = True
            for key, value in kwargs.items():
                if node.value.get(key) != value:
                    match = False
                    break
            if match:
                selected.append((node, obj_id, level))

        return selected

class PdFile(object):
    """Abstraction for a Pd format patch file."""

    def __init__(self, filename):
        self.filename = filename

        fd = None
        try:
            # It's easier and quicker to read the whole file at one and then
            # parse it, but here we use readlines() for the convenience of
            # knowing the original line numbers in the file in case we need to
            # report errors.

            # We use the universal file reader to cope with unix and dos
            # line endings. This means we'll look for lines ending in ';\n'
            # to mark the end of logical Pd lines.
            fd = open(self.filename, 'U')
            self.lines = fd.readlines()
        finally:
            if fd:
                fd.close()
            # let exceptions propagate up

        # Parse all lines creating a patch object.
        self.patch = PdPatch(self.lines)

    def __str__(self):
        return str(self.patch)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        f = PdFile('test1.pd')
    else:
        f = PdFile(sys.argv[1])

    #for (node, obj_id, level) in f.patch:
        #print '%-4d %s%s' % (obj_id, ' ' * (level * 4), str(node.value))
            #node.parent and node.parent.value.element == 'canvas' and \
            #node.parent.value.get('name') == 'player':

    def fn(node_tuple):
        (node, obj_id, level) = node_tuple
        y = node.value.get('y')
        if node.value.element == 'text':
            return True
        else:
            return False

    for (node, oid, level) in f.patch:
        print '%d%s%s' % (oid, ' ' * (level * 4), str(node.value))

    #for (node, oid, level) in filter(fn, f.patch):
        #print str(node.value)
    #vsls = [str(n.value) for (n,o,l) in filter(fn, f.patch)]
    #print '\n'.join(vsls)

    """
    #for (m,i) in f.patch.filter(filt):
    #for (m, i, level) in filter(filt, f.patch):
    for (m,i) in f.patch.select(element = 'text'):
        parents = []
        textobj = str(m.value)
        while m.parent:
            parents.insert(0, m.parent.value)
            m = m.parent

        ts = 0
        for p in parents:
            print '%s%s' % (' ' * ts, str(p.name()))
            ts += 4
        print '%s%-4d %s\n' % (' ' * ts, i, textobj)
    """

