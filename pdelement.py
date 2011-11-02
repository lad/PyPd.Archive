#!/usr/bin/env python

import sys

# Element Definitions
#
# We need to maintain the names of each attribute for each PD element. We also
# need to know the order in which the attributes appear in each textual Pd
# object definition.
#   One option is to write a class for each PD element type which would contain
# attribute names and also store the order these attributes appear in the
# object definition.
#   The scheme used here stores the attribute names in order for each PD
# object type. This requires less code to maintain since there is just a
# single list of attributes in order here.
#

# These are built-in to pd-vanilla. The keys are all names that can occur after
# the chunk type. The values are the attributes that are defined for that type.
# Exceptions are:
#     'array-data'      Array data (#A) doesn't actually have an element name.
#                       We use this name for convenience.
#     'canvas-5'        There are two canvas definitions. One with 5 params
#     'canvas-6'        at the start of the patch, 6 params otherwise.

# Internal element name for array data. It's the only Pd data that doesn't have
# an element type, so we use this.
ARRAY_DATA = 'array-data'

VANILLA_ELEMENTS = {
    'array':        ['name', 'size', 'save_flag'],
    ARRAY_DATA:     ['start_idx', 'values'],
    # There are two types of canvas, define both
    'canvas-5':     ['x', 'y', 'width', 'height', 'font_size'],
    'canvas-6':     ['x', 'y', 'width', 'height', 'name', 'open_on_load'],
    'connect':      ['src_id', 'src_out', 'dest_id', 'dest_out'],
    'coords':       ['x1', 'y2', 'x2', 'y1', 'width', 'heigth', 'gop'],
    'declare':      ['path_type', 'path'],
    'floatatom':    ['x', 'y', 'width', 'lower', 'upper', 'label_pos', 'label',
                     'receive', 'send'],
    'import':       ['name'],
    'msg':          ['x', 'y', 'text'],
    'obj':          ['x', 'y', 'type'],
    'restore':      ['x', 'y', 'name'],
    'scalar':       [],
    'struct':       [],
    'symbolatom':   ['x', 'y', 'width', 'lower', 'upper', 'label_pos', 'label',
                     'receive', 'send'],
    'text':         ['x', 'y', 'text']
    }


# These are the object types built-in to pd-vanilla. The keys are the object
# type name that appears after the x/y parameters (chunk-type obj x y type).
# The values are the attributes for the object.
VANILLA_OBJECTS = {
    '!=':           ['rhs'],
    '%':            ['rhs'],
    '&&':           ['rhs'],
    '&':            ['rhs'],
    '*':            ['rhs'],
    '*~':           ['rhs'],
    '+':            ['rhs'],
    '+~':           ['rhs'],
    '-':            ['rhs'],
    '-~':           ['rhs'],
    '/':            ['rhs'],
    '/~':           ['rhs'],
    '<':            ['rhs'],
    '<<':           ['rhs'],
    '<=':           ['rhs'],
    '==':           ['rhs'],
    '>':            ['rhs'],
    '>=':           ['rhs'],
    '>>':           ['rhs'],
    '|':            ['rhs'],
    '||':           ['rhs'],
    'abs':          [],
    'abs~':         [],
    'adc~':         ['inputs'],
    'append':       ['template_name', 'fields'],
    'arraysize':    ['array_name'],
    'atan':         [],
    'atan2':        [],
    'bag':          [],
    'bang':         [],
    'bang~':        [],
    'bendin':       ['channel'],
    'bendout':      ['channel'],
    'biquad~':      ['coeffs'],
    'block~':       ['size', 'overlap', 'resampling'],
    'bng':          ['size', 'hold', 'interrupt', 'init',
                     'send', 'receive', 'label', 'label_x', 'label_y', 'font',
                     'font_size', 'bg_color', 'fg_color', 'label_color'],
    'bp~':          ['freq', 'q'],
    'catch~':       ['bus_name'],
    'change':       ['init'],
    'clip':         ['lower', 'upper'],
    'clip~':        ['lower', 'upper'],
    'closebang':    [],
    'cnv':          ['size', 'width', 'height', 'send',
                     'receive', 'label', 'label_x', 'label_y', 'font',
                     'font_size', 'bg_color', 'label_color', 'reserved'],
    'cos':          [],
    'cos~':         [],
    'cpole~':       ['re', 'im'],
    'cputime':      [],
    'ctlin':        ['controller', 'channel'],
    'ctlout':       ['controller', 'channel'],
    'czero_rev~':   ['re', 'im'],
    'czero~':       ['re', 'im'],
    'dac~':         ['outputs'],
    'dbtopow':      [],
    'dbtopow~':     [],
    'dbtorms':      [],
    'dbtorms~':     [],
    'declare':      ['path_type', 'path'],
    'delay':        ['ms'],
    'delread~':     ['buf', 'ms'],
    'delwrite~':    ['buf', 'ms'],
    'div':          ['rhs'],
    'dmstodb':      [],
    'drawcurve':    [],
    'drawnumber':   [],
    'drawpolygon':  [],
    'drawsymbol':   [],
    'drunk':        ['upper', 'step'],
    'element':      [],
    'env~':         ['window', 'period'],
    'exp':          [],
    'expr':         ['expr'],
    'expr~':        ['expr'],
    'exp~':         ['base'],
    'fft~':         [],
    'filledcurve':  [],
    'filledpolygon': [],
    'float':        ['init'],
    'framp~':       [],
    'ftom':         [],
    'ftom~':        [],
    'get':          [],
    'getsize':      [],
    'hip~':         ['freq'],
    'hradio':       ['size', 'new_old', 'init', 'number',
                     'send', 'receive', 'label', 'label_x', 'label_y', 'font',
                     'font_size', 'bg_color', 'fg_color', 'label_color',
                     'default_value'],
    'hslider':      ['width', 'height', 'bottom', 'top',
                     'log', 'init', 'send', 'receive', 'label', 'label_x',
                     'label_y', 'font', 'font_size', 'bg_color', 'fg_color',
                     'label_color', 'default_value', 'steady_on_click'],
    'ifft~':        [],
    'import':       ['name'],
    'initbang':     [],
    'inlet':        ['name'],
    'inlet~':       ['name'],
    'int':          ['init'],
    'key':          [],
    'keyname':      [],
    'keyup':        [],
    'line':         ['init', 'grain_rate'],
    'line~':        [],
    'list':         ['init'],
    'loadbang':     [],
    'log':          [],
    'log~':         ['base'],
    'lop~':         ['freq'],
    'makefilename': ['format'],
    'makenote':     ['velocity', 'duration'],
    'makesymbol':   ['format'],
    'max':          [],
    'max~':         [],
    'metro':        ['ms'],
    'midiin':       [],
    'midiout':      [],
    'midirealtimein': [],
    'min':          [],
    'min~':         [],
    'mod':          ['value'],
    'moses':        ['value'],
    'mtof':         [],
    'mtof~':        [],
    'namecanvas':   [],
    'nbx':          ['size', 'height', 'min', 'max', 'log',
                     'init', 'send', 'receive', 'label', 'label_x', 'label_y',
                     'font', 'font_size', 'bg_color', 'fg_color',
                     'label_color', 'log_height'],
    'netreceive':   ['port_num', 'tcp_udp'],
    'netsend':      ['tcp_udp'],
    'noise~':       [],
    'notein':       ['channel'],
    'noteout':      ['channel'],
    'openpanel':    [],
    'osc~':         ['freq'],
    'outlet':       ['name'],
    'outlet~':      ['name'],
    'pack':         ['format'],
    'pgmin':        ['channel'],
    'pgmout':       ['channel'],
    'phasor~':      ['freq'],
    'pipe':         ['data_type', 'delay'],
    'plot':         [],
    'pointer':      [],
    'poly':         ['num_voices', 'steal_voices'],
    'polytouchin':  ['channel'],
    'polytouchout': ['channel'],
    'pow':          ['value'],
    'powtodb':      [],
    'pow~':         [],
    'print':        ['prefix'],
    'print~':       ['prefix'],
    'q8_rsqrt~':    [],
    'q8_sqrt~':     [],
    'qlist':        [],
    'random':       ['max'],
    'readsf~':      ['num_channels', 'buf_size'],
    'realtime':     [],
    'receive':      ['src'],
    'receive~':     ['src'],
    'rfft~':        [],
    'rifft~':       [],
    'rmstodb':      [],
    'rmstodb~':     [],
    'route':        ['format'],
    'rpole~':       ['re'],
    'rsqrt~':       [],
    'rzero_rev~':   ['re'],
    'rzero~':       ['re'],
    'samphold~':    [],
    'samplerate~':  [],
    'savepanel':    [],
    'select':       [],
    'send':         ['dest'],
    'send~':        ['dest'],
    'serial':       [],
    'set':          [],
    'setsize':      [],
    'sig~':         ['init'],
    'sin':          [],
    'snapshot~':    ['ms'],
    'soundfiler':   [],
    'spigot':       ['init'],
    'sqrt':         [],
    'sqrt~':        [],
    'stripnote':    [],
    'struct':       [],
    'sublist':      ['template_name', 'field'],
    'swap':         [],
    'switch~':      [],
    'symbol':       ['init'],
    'sysexin':      [],
    'table':        ['name', 'size'],
    'tabosc4~':     ['table'],
    'tabplay~':     ['table'],
    'tabread':      ['table'],
    'tabread4':     ['table'],
    'tabread4~':    ['table'],
    'tabread~':     ['table'],
    'tabreceive~':  ['table'],
    'tabsend~':     ['array_name'],
    'tabwrite':     ['table'],
    'tabwrite~':    ['table'],
    'tan':          [],
    'textfile':     [],
    'threshold~':   ['val', 'deb_time', 'rest_time'],
    'throw~':       ['name'],
    'timer':        [],
    'toggle':       ['size', 'init', 'send', 'receive',
                     'label', 'label_x', 'label_y', 'font', 'font_size',
                     'bg_color', 'fg_color', 'label_color', 'init_value',
                     'default_value'],
    'touchin':      ['channel'],
    'touchout':     ['channel'],
    'trigger':      ['format'],
    'unpack':       ['format'],
    'until':        [],
    'value':        [],
    'vcf~':         ['q'],
    'vd~':          ['buf'],
    'vline~':       [],
    'vradio':       ['size', 'new_old', 'init', 'number',
                     'send', 'receive', 'label', 'label_x', 'label_y', 'font',
                     'font_size', 'bg_color', 'fg_color', 'label_color',
                     'default_value'],
    'vslider':      ['width', 'height', 'bottom', 'top',
                     'log', 'init', 'send', 'receive', 'label', 'label_x',
                     'label_y', 'font', 'font_size', 'bg_color', 'fg_color',
                     'label_color', 'default_value', 'steady_on_click'],
    'vsnapshot~':   [],
    'vu':           ['width', 'height', 'receive', 'label',
                     'label_x', 'label_y', 'font', 'font_size', 'bg_color',
                     'label_color', 'scale', 'reserved'],
    'wrap~':        [],
    'writesf~':     [],
    }

# Aliases
aliases = [('vsl', 'vslider'), ('hsl', 'hslider'), ('tgl', 'toggle'),
           ('hdl', 'hradio'),  ('vdl', 'vradio'),  ('v', 'value'),
           ('s', 'send'),      ('s~', 'send~'),
           ('r', 'receive'),   ('r~', 'receive~'),
           ('b', 'bang'),      ('del', 'delay'),
           ('f', 'float'),     ('i', 'int'),
           ('t', 'trigger'),   ('sel', 'select')]

# add new dict keys for the aliases, pointing to existing values
VANILLA_OBJECTS.update([(a[0], VANILLA_OBJECTS[a[1]]) for a in aliases])

# We need these every time we see an 'obj', so save them here...
OBJ_ATTRS = VANILLA_ELEMENTS['obj']
OBJ_NUM_ATTRS = len(OBJ_ATTRS)
TYPE_INDEX = 2

def is_num_or_var(text):
    # Return known if the object is just a number or dollar-arg,
    # otherwise it's an unknown abstraction.
    try:
        if len(text) > 2 and text[:2] == '\$':
            return True
        else:
            float(text)
            return True
    except ValueError, ex:
        return False

def make_dict(attrs, params):
    kv = dict(zip(attrs, params))

    len_params = len(params)
    len_attrs = len(attrs)
    if len_params < len_attrs:
        # If we don't have enough parameters set the remaining attributes to
        # None
        kv.update([(k, None) for k in attrs[len_params:]])
        extra_params = []
    else:
        # Save the additional parameters that we don't have attributes for
        extra_params = params[len_attrs:]

    return (kv, extra_params)


def get(name, params, warn = True):
    """Returns a three valued tuple containing:
        . a list of attribute names in the order they occur in the Pd patch
          file format
        . a dict of attribute names and values from "params"
        . a list of the values from "params" not used in generating the dict.
        . a flag indicating whether this given "name" is a known Pd object, or
          whether "name" is likely to be another abstraction (i.e. another
          patch).

       "name" is used to lookup a list of attribute names defined for each
       Pd element/object.  The dict returned uses the attributes names as
       as keys, and the corresponding value from the given "params" as the
       value for each key.

       Attribute values are set to None if there are too few values in
       "params".  When there are too many parameters the remaining values
       are return as a list in the second argument of the returned tuple.

       The final arg of the return tuple indicates whether a definition was
       found for the given "name". If a definition is not found, the name
       is likely to be an external abstraction.
       """

    # The PD line format is quite inconsistent, so we have to deal with a few
    # special cases here...
    len_params = len(params)

    # Each of these cases attempt to get a list of attribute names for the
    # "name" passed in. The attribute names and the values from "params" are
    # put into a dictionary and returned to the caller.
    # NOTES:
    # - This code is Python 2.6 compatible, so I haven't used the new
    #   collections.OrderedDict.
    # - I've decided against implementing an 2.6 compatible ordered-dict, as
    #   this dict will be exposed to uses of PyPd, and I'd be concerned about
    #   any incompatible edge cases where the custom imlementation may differ
    #   from what is expected of a standard dict.

    if name == 'canvas':
        if len_params == 5:
            name = 'canvas-5'
        else:
            name = 'canvas-6'

        attrs = VANILLA_ELEMENTS[name]
        (kv, extra_params) = make_dict(attrs, params)
        return (attrs, kv, extra_params, True)
    elif name == 'obj':
        # There are a few different 'obj' cases to handle here...

        # All 'obj' should start with x, y and type.
        if len_params >= OBJ_NUM_ATTRS:
            oattrs = VANILLA_OBJECTS.get(params[TYPE_INDEX])
            if oattrs is not None:
                known = True
                attrs = OBJ_ATTRS + oattrs
            else:
                # No definition for this object type, use the minimal 'obj'
                # attributes
                attrs = OBJ_ATTRS
                # Since the type wasn't found, check if it's a a number or
                # dollar-arg (a variable). If not, it's a external abstration.
                known = is_num_or_var(params[TYPE_INDEX])

            (kv, extra_params) = make_dict(attrs, params)

            return (attrs, kv, extra_params, known)
        else:
            # Don't even have x,y,type. Save what we can and return it.
            (kv, extra_params) = make_dict(OBJ_ATTRS, params)
            return (OBJ_ATTRS, kv, extra_params, False)
    else:
        try:
            attrs = VANILLA_ELEMENTS[name]
            known = True
        except KeyError, ex:
            # We may encounter elements which this code doesn't know about.
            # In this case we add an empty definition.
            # - Could just use a defaultdict here and omit the warning.
            #   Is there something better to do here?
            if warn:
                print 'Warning: No built-in definition for %s.' % name
            VANILLA_ELEMENTS[name] = []
            attrs = []
            known = False

        (kv, extra_params) = make_dict(attrs, params)
        return (attrs, kv, extra_params, known)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        (attrs, k, e, known) = get('obj', ['x', 'y', sys.argv[1]])
        print known
        if not known:
            (attrs, k, e, known) = get(sys.argv[1], [], warn = False)

        if known:
            if attrs:
                print ' '.join(attrs)
            else:
                print 'Known but empty definition'
        else:
            print 'No definition for %s' % sys.argv[1]
