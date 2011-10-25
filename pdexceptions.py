#!/usr/bin/env python

""" All PyPD exceptions are defined here."""

__author__ = "Louis A. Dunne"
__copyright__ = "Copyright 2011, Louis A. Dunne"
__credits__ = ["Louis A. Dunne"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Louis A. Dunne"
__status__ = "Alpha"

class PdException(Exception):
    """All exceptions defined in this package will be sub-classed from this."""
    def __init__(self, *args):
        super(PdException, self).__init__(*args)

class PdInvalidPatch(PdException):
    def __init__(self, *args):
        super(PdInvalidPatch, self).__init__(*args)


class InvalidPdLine(PdException):
    def __init__(self, line_text, line_num, err_text = 'Invalid line',
                 ex = None):
        super(InvalidPdLine, self).__init__('%s:%d "%s"' % \
                                            (err_text, line_num, \
                                            line_text))
        (self.line_text, self.line_num, self.ex) = (line_text, line_num, ex)
