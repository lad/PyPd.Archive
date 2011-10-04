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
__version__ = "0.1"
__maintainer__ = "Louis A. Dunne"
__status__ = "Alpha"

# Some constants we need to recognize in the patch file
NCHUNK = '#N'
CCHUNK = '#C'
ACHUNK = '#A'
XCHUNK = '#X'
CANVAS = 'canvas'
CANVAS0 = 'canvas0'     # canvas on the first line has a different definition
RESTORE = 'restore'
STRUCT = 'struct'
OBJ = 'obj'


class PdParsedLine:
    """A parsed representation of a logical Pd line. This takes a PdLine object
       and makes the attributes available via their defined names.

       Attributes can be accessed and modified like a dict:
          obj['attribute_name'] or          (throws exception if not found)
          obj.get('attribute_name')         (returns None if not found)

        Printing the object should result in text appropriate for storing in
        a Pd patch file."""

    def __init__(self, line_text, line_num):
        params = line_text.split(' ')

        # There are various line formats to deal with. All lines start with
        # a chunk type, and most chunk types are followed by an element
        # type, except '#A' (array data).
        try:
            self.chunk = params[0]
            params = params[1:]

            # "#N canvas" or "#N struct"
            if self.chunk == NCHUNK:
                self.element = params[0]
                params = params[1:]

                if self.element != CANVAS and self.element != STRUCT:
                    raise InvalidPdLine(line_text, line_num, '"%s" is not ' \
                                        'valid with a #N chunk type. Only #N ' \
                                        'canvas and #N struct are valid.' \
                                        % str(self.element))

                if line_num == 0:
                    # The first canvas definition is different to all other
                    # canvas definitions so we have to special case it.
                    self.element = CANVAS0

            # "#C restore"
            elif self.chunk == CCHUNK:
                self.element = params[0]
                params = params[1:]
                if self.element != RESTORE:
                    raise InvalidPdLine(line_text, line_num, '"%s" is not ' \
                                        'valid with a #N chunk type. Only #C ' \
                                        'restore is valid.' % str(self.element))

            # "#A array-data"
            elif self.chunk == ACHUNK:
                self.element = '<array-data>'
                self.known = True

            # "#X ..."
            elif self.chunk == XCHUNK:
                self.element = params[0]
                params = params[1:]

            else:
                raise InvalidPdLine(line_text, line_num,
                                    'Unrecognized chunk type')
        except IndexError, ex:
            raise InvalidPdLine(line_text, line_num, ex = ex)

        # Lookup the attributes defined for the element type. The exception
        # is array data (#A) which doesn't have an element name.

        if self.chunk == ACHUNK:
            (self.attr_defs, self.known) = (pdelement.array_def, True)
        else:
            (self.attr_defs, self.known) = pdelement.get(self.element, params)

        # Make a dict (self.attrs) to break out each parameter from the Pd
        # text line. The keys come from the attribute definition
        # (self.attr_defs), the values are the text line.

        self.last_list = False
        len_defs = len(self.attr_defs)
        len_params = len(params)

        if len_params > len_defs:
            # Put extra params as a list in the last attribute
            self.attrs = dict(zip(self.attr_defs[:-1], params[:len_defs-1]))
            self.attrs[self.attr_defs[-1]] = params[len_defs-1:]
            self.last_list = True
        elif len_params < len_defs:
            # Add attributes for the params we have
            self.attrs = dict(zip(self.attr_defs, params))
            # Set remaining attributes to None
            self.attrs.update(dict([(k, None) \
                              for k in self.attr_defs[len_params:]]))
        else:
            # Same number of params and attributes
            self.attrs = dict(zip(self.attr_defs, params))


    def __getitem__(self, attr_name):
        """Access Pd attributes by name. Raises exception if not found."""
        return self.attrs[attr_name]

    def get(self, attr_name):
        """Access Pd attributes by name. Returns None if not found."""
        return self.attrs.get(attr_name)

    def __str__(self):
        """Returns a textual representation suitable for storing in a Pd
           patch file."""

        # Get all attributes values in the order they appear in the
        # attribute definition, excluding any values set to None.
        if self.last_list:
            # In this case the we had more parameters than attributes so the
            # last attribute is already a list of values
            vals = [self.attrs[s] \
                        for s in self.attr_defs[:-1] if self.attrs[s]] + \
                   [s for s in self.attrs[self.attr_defs[-1]] if s]
        else:
            vals = [self.attrs[s] for s in self.attr_defs if self.attrs[s]]

        # Special case the canvas on line 0 and array-data
        if self.chunk == ACHUNK:
            return ' '.join([self.chunk] + vals)
        elif self.element == CANVAS0:
            return ' '.join([self.chunk, CANVAS] + vals)
        else:
            return ' '.join([self.chunk, self.element] + vals)

    def name(self):
        """Returns the element name or the object name if the element is an
           'obj'"""

        if self.element == OBJ:
            return self.attrs.get('obj_type') or self.element
        else:
            return self.element

class PdLine(object):
    """Abstraction for a logical line from a Pd format patch file."""

    def __init__(self, line_text, line_num, obj_id):
        (self.line_text, self.line_num, self.obj_id) = \
                        (line_text, line_num, obj_id)
        assert self.line_num >= 0
        assert self.obj_id >= -1    # Top level canvas is given an ID of -1

        # This is the parsed object.
        self.p = PdParsedLine(line_text, line_num)

    @staticmethod
    def factory(lines):
        """This is a generator which takes a list of lines from a Pd
           patch file and yields each logical Pd line. It loops through
           the lines, joining them up until the end of line marker (;\\n) is
           hit. Also keeps track of file line numbers and object numbers and
           supplies these to PdLine()"""

        (logical_line, obj_id, parent_ids) = ('', -1, collections.deque())

        for line_num, line in enumerate(lines):
            line = line.rstrip('\n')
            if line and not line.isspace():
                logical_line += line
                if len(logical_line) > 1 and logical_line[-2] != '\\' and \
                   logical_line[-1] == ';':
                    # Now we have a full logical Pd line - make a PdLine
                    # and return it
                    obj = PdLine(logical_line[:-1], line_num, obj_id)
                    element = obj.p.element
                    yield obj

                    # When we come back into the generator we need to figure
                    # out the next object id, and start new logical line
                    logical_line = ''

                    if element == CANVAS:
                        # Each sub-patch starts with a canvas object.  The
                        # objects ids in each sub-patch start at zero.
                        parent_ids.append(obj_id)
                        obj_id = 0
                    elif element == RESTORE:
                        # Sub-patches finish with a restore object. Object
                        # ids then continue where they left off before the
                        # sub-patch.
                        try:
                            # TODO: There are "#C restore;" lines that don't
                            # correspond to previous canvas declarations.
                            # These have no name, but don't know what they're
                            # for yet. Ignore for now.
                            if obj.p.get('name'):
                                obj_id = parent_ids.pop() + 1
                        except:
                            print str(obj)
                            raise
                    else:
                        obj_id += 1

    def __str__(self):
        return self.line_text

class PdFile:
    """Abstraction for a Pd format patch file."""

    def _read(self, filename):
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
            lines = fd.readlines()
        finally:
            if fd:
                fd.close()
            # let exceptions propagate up
        return lines


    def __init__(self, filename):
        # read in the whole file
        lines = self._read(filename)

        # PdLine defines a generator which takes the lines from the patch
        # file and yields each logical Pd line. Each logical line defines
        # a Pd element/object, and may span several physical text lines.
        line_factory = PdLine.factory(lines)

        # first line is supposed to be the top level canvas
        self.canvas = line_factory.next()

        # Store the remaining lines in a list
        self.lines = [line for line in line_factory]

        # _tree will be populated when touched - it will hold a tree
        # representation of the patch and each of its sub-patches.
        self._tree = None

    def get_tree_property(self):
        if not self._tree:
            self._parse()
        return self._tree
    tree = property(get_tree_property)

    def _parse(self):
        self._tree = pdtree.Tree(self.canvas)
        tree_stack = [self._tree]

        try:
            for line in self.lines:
                # Add a branch to the tree when we hit a sub-patch (canvas)
                if line.p.element == CANVAS:
                    t = tree_stack[-1].addBranch(line)
                    tree_stack.append(t)
                # Move back to the parent branch when we return from the
                # sub-patch (a restore with a name)
                elif line.p.element == RESTORE and line.p.get('name'):
                    tree_stack[-1].addLeaf(line)
                    tree_stack.pop()
                # Otherwise all other objects are leaf nodes
                else:
                    tree_stack[-1].addLeaf(line)
        except IndexError:
            print 'Error parsing sub-patch (canvas/restore) around line ' \
                  '%d' % line.line_num
            print '\t"%s"\n' % str(line)
            raise

    def __str__(self):
        return self.filename

##### TESTS #####

def testPdFile1(filename):
    f = PdFile(filename)
    for line in f.lines:
        if str(line) != str(line.p):
            # The lines may differ by whitespace only. Extract all words and
            # compare separately.
            same = all([oword == pword \
                        for (oword, pword) in \
                        zip(str(line).split(), str(line.p).split())])
            if not same:
                raise pdtest.Unexpected(str(line.line_num),
                                        str(line), str(line.p))

@pdtest.passfail
def testPdFile(args):
    fnames = args or ['test1.pd']
    for fname in fnames:
        print fname
        testPdFile1(fname)

def test():
    testPdFile(sys.argv[1:])

if __name__ == '__main__':
    test()
