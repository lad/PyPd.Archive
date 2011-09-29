
"""Test utilities."""

class Unexpected(Exception):
    """Raise when we encounter unexpected data."""

    def __init__(self, k, v, gotv):
        (self.k, self.v, self.gotv) = (k, v, gotv)

    def __str__(self):
        return 'Expected "%s = %s". Got "%s"' % (self.k, self.v, self.gotv)

def passfail(fn):
    """Decorator outputs pass/fail for each test."""

    parent = fn.__name__
    def runfn(*args):
        try:
            ret = fn(*args)
        except Exception, ex:
            print "\n----------"
            print '%s Failed' % parent
            print
            raise

        print '%s: Passed' % parent
        return ret
    return runfn


