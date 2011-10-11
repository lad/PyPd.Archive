#!/usr/bin/env python

""" Classes for reading, parsing and manipulating Pure Data (.pd) files:

    PdFile: opens and read Pd patch files.
    PdLine: plain text representation of each logical Pd line.
    PdParsedLine: parsed representation of each line/object """

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
        return self.attrs[attr_name]

    def get(self, attr_name):
        """Access Pd attributes by name. Returns None if not found."""
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
        else:
            return self.element


class PdPatchFilter(object):
    pass

class PdPatch(object):
    """This is a container type abstraction for a Pure Data patch or sub-patch.
       These are represented by the Pd "canvas" type. All patch files start
       with a top-level canvas declaration, and may contain further canvas
       declarations to indicate sub-patches.

       Objects are accessed via their object-ids, which can change if objects
       are inserted or deleted. This is an unfortunate side-effect of the
       Pd patch file format.

       An easier way to access specific objects is to create a PdPatchFilter
       object to describe the desired objects, then use the select() method
       to iterate through the selected objects."""

    def __init__(self, patch_text):
        """Create a PdPatch object from the textual description given in
           "patch_text"."""

        self._patch_text = patch_text

        factory = PdObject.factory(patch_text)

        self.canvas = factory.next()
        if self.canvas.element != CANVAS:
            # First line should be the canvas definition
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
           canvas object for that sub-patch. See PdPatchFilter for an easier
           way to access objects.

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

        pass

    def __delitem__(self, key):
        pass

    def __iter__(self):
        return self.iter()

    def __reversed__(self):
        """There's no point in reversing a patch."""

        raise NotImplementedError('PdPatch does not support reversed()')

    def __contains__(self):
        pass

    def __str__(self):
        return ';\r\n'.join(str(node.value) for node in self)

    def __iter__(self):
        return iter(self._tree)

    def apply(self, fn):
        return self._tree.apply(fn)

    def insert(self, key, value):
        pass

    def select(self, obj_filter):
        pass

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

    for (node, obj_id, level) in f.patch:
        print '%-4d %s%s' % (obj_id, ' ' * (level * 4), str(node.value))
        #print i.value
        #print '%d   %s' % (i.value.known, i.value)
