#!/usr/bin/env python

"""Simple utility classes useful in manipulating Pure Data patch files."""

def toPdColor(red, green, blue):
    """RGB to PD format color"""
    return (red * -65536) + (green * -256) + (blue * -1)

