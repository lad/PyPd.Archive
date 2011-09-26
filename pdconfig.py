
import ConfigParser

class PdConfigParser(object):
    """Get/Set values in a PyPD config file."""

    SECTION = 'install'

    def __init__(self, filename):
        """Reads the given filename using ConfigParser.RawConfigParser"""

        self.filename = filename
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.filename)

        if not self.config.has_section(self.SECTION):
            self.config.add_section(self.SECTION)

    def set(self, key, value, write = True):
        """Sets the given key/value. The config file is re-written unless
           the write keyword is set to False"""

        self.config.set(self.SECTION, key, value)
        if write:
            self.write()

    def setm(self, items, write = True):
        """Sets the multiple key/value. "items" is expected to be a list
           of (key,value) tuples. The config file is re-written unless
           the write keyword is set to False"""

        for key, value in items:
            self.config.set(self.SECTION, key, value)
        if write:
            self.write()

    def get(self, key):
        """Return the value for the given key"""

        return self.config.get(self.SECTION, key)

    def get_startswith(self, keystart):
        """Return all values that start with the given string."""

        keys = self.config.options(self.SECTION)
        keys.sort()
        return [self.config.get(self.SECTION, key) \
                for key in  keys if key.startswith(keystart)]

    def write(self):
        """Write the config data out to the config file."""

        fd = None
        try:
            fd = open(self.filename, 'w')
            self.config.write(fd)
        finally:
            if fd:
                fd.close()
