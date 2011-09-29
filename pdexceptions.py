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


class InvalidPdLine(PdException):
    """This is the only exception this module currently throws - when it
       encounters a line in cannot parse."""

    def __init__(self, pd_line, err_text = 'Invalid line', ex = None):
        super(InvalidPdLine, self).__init__('%s:%d "%s"' % \
                                            (err_text, pd_line.line_num, \
                                            pd_line.text))
        (self.pd_line, self.ex) = (pd_line, ex)