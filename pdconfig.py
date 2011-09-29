
import ConfigParser

class PdConfigParser(object):
    """Get/Set values in a PyPD config file."""

    SECTION = 'install'

    def __init__(self, filename):
        """Reads the given filename using ConfigParser.RawConfigParser."""

        self.filename = filename
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.filename)

        if self.config.has_section(self.SECTION):
            self.items = dict(self.config.items(self.SECTION))
        else:
            self.config.add_section(self.SECTION)
            self.items = {}


    def set(self, key, value, write = True):
        """Sets the given key/value. The config file is re-written unless
           the write keyword is set to False."""

        self.config.set(self.SECTION, key, value)
        self.items[key] = value
        if write:
            self.write()

    def setm(self, key, values, write = True):
        """Sets the multiple values for the given key. The config file is
           re-written unless the write keyword is set to False."""

        # Each value is saved in a separate key, which removes the need to
        # parse a multi-valued string when reading them back in.

        keystart = '%s_' % key
        # Find the number of existing keys that start with the given key
        n = sum([k.startswith(keystart) for k in self.items.keys()]) + 1

        for i, value in enumerate(values):
            k = '%s_%d' % (key, i + n)
            self.config.set(self.SECTION, k, value)
            self.items[k] = value

        if write:
            self.write()

    # Works like a dict:
    #   obj['key'] will throw an exception if key is not found.
    #   obj.get('key') will return None if not found.

    def __getitem__(self, key):
        """Return the value for the given key."""

        return self.items[key]

    def get(self, key):
        """Return the value for the given key or None if not found."""

        return self.items.get(key)

    def getm(self, key):
        """Return multiple values for keys that start with the given string.
           Returns an empty list if no values are found."""

        keystart = '%s_' % key
        return [self.items[key] for key in self.items.keys() \
                if key.startswith(keystart)]

    def unset(self, key, write = True):
        """Remove a key from the config file. The config file is re-written
           unless the write keyword is set to False. Returns True/False to
           indicate whether the key was found and removed."""

        if self.items.has_key(key):
            self.config.remove_option(self.SECTION, key)
            del self.items[key]
            if write:
                self.write()
            return True
        else:
            return False

    def unsetm(self, key, write = True):
        """Remove multiple keys from the config file that start with the given
           string.  The config file is re-written unless the write keyword is
           set to False. Returns True if one or more keys were removed,
           False otherwise."""

        keystart = '%s_' % key
        def rm(key):
            if key.startswith(keystart):
                return self.unset(key, write = False)

        ret = any(map(rm, self.items.keys()))
        if write:
            self.write()

        return ret

    def write(self):
        """Write the config data out to the config file."""

        fd = None
        try:
            fd = open(self.filename, 'w')
            self.config.write(fd)
        finally:
            if fd:
                fd.close()
