
# Element Definitions
#
# We need to maintain the names of each attribute for each PD element. We also
# need to know the order in which the attributes appear in the lines in the .pd
# file.
#   One option is to write a class for each PD element type which would contain
# attribute names and also store the order these attributes appear in the
# .pd files.
#   The scheme used here stores the attribute names in order for each PD
# element type. These are used to add attributes to a PdParsedLine object when
# each PD line is parsed.
#   This requires less code to maintain since there is just a single list of
# attributes in order here.
#
# TODO: Maybe change this to use a text file that non-programmers can edit.
#

ELEMENT_DEFS = {
    'struct':           [ 'params' ],
    'scalar':           [ 'params' ],
    'connect':          [ 'src_id', 'src_out', 'tgt_id', 'tgt_out' ],
    # special case for canvas on the first line
    'canvas0':          [ 'x', 'y', 'width', 'height', 'font_size' ],
    'canvas':           [ 'x', 'y', 'width', 'height', 'name', 'open_on_load' ],
    'array':            [ 'name', 'size', 'save_flag' ],
    'coords':           [ 'x1', 'y2', 'x2', 'y1', 'width', 'heigth', 'gop' ],
    'floatatom':        [ 'x', 'y', 'width', 'lower', 'upper', 'label_pos',
                          'label', 'receive', 'send' ],
    'symbolatom':       [ 'x', 'y', 'width', 'lower', 'upper', 'label_pos',
                          'label', 'receive', 'send' ],
    'msg':              [ 'x', 'y', 'text' ],
    'obj':              [ 'x', 'y', 'obj_type', 'params' ],
    'restore':          [ 'x', 'y', 'graph_flag', 'name' ],
    'text':             [ 'x', 'y', 'text' ],
    'declare':          [ 'params' ]
    }

OBJECT_DEFS = {
    'inlet':            [ 'x', 'y', 'obj_type' ],
    'outlet':           [ 'x', 'y', 'obj_type' ],
    'send':             [ 'obj_type', 'dest', ],
    'send~':            [ 'obj_type', 'dest', ],
    'receive':          [ 'obj_type', 'src', ],
    'receive~':         [ 'obj_type', 'src', ],
    'pack':             [ 'x', 'y', 'obj_type' ],
    '!=':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '%':                [ 'x', 'y', 'obj_type', 'rhs' ],
    '&':                [ 'x', 'y', 'obj_type', 'rhs' ],
    '&&':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '*':                [ 'x', 'y', 'obj_type', 'rhs' ],
    '*~':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '+':                [ 'x', 'y', 'obj_type', 'rhs' ],
    '+~':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '-':                [ 'x', 'y', 'obj_type', 'rhs' ],
    '-~':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '/':                [ 'x', 'y', 'obj_type', 'rhs' ],
    '/~':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '<':                [ 'x', 'y', 'obj_type', 'rhs' ],
    '<=':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '<~':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '==':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '>':                [ 'x', 'y', 'obj_type', 'rhs' ],
    '>=':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '>>':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '<<':               [ 'x', 'y', 'obj_type', 'rhs' ],
    '||':               [ 'x', 'y', 'obj_type', 'rhs' ],
    'abs':              [ 'x', 'y', 'obj_type' ],
    'adc~':             [ 'x', 'y', 'obj_type', 'inputs' ],
    'append':           [ 'x', 'y', 'obj_type', 'template_name', 'fields' ],
    'sublist':          [ 'x', 'y', 'obj_type', 'template_name', 'field' ],
    'arraysize':        [ 'x', 'y', 'obj_type', 'array_name' ],
    'atan':             [ 'x', 'y', 'obj_type' ],
    'bang':             [ 'x', 'y', 'obj_type' ],
    'biquad~':          [ 'x', 'y', 'obj_type', 'params' ],
    'block~':           [ 'x', 'y', 'obj_type', 'size', 'overlap',
                          'resampling' ],
    'bp~':              [ 'x', 'y', 'obj_type', 'freq', 'q' ],
    'catch~':           [ 'x', 'y', 'obj_type', 'bus_name' ],
    'change':           [ 'x', 'y', 'obj_type', 'init' ],
    'clip':             [ 'x', 'y', 'obj_type', 'lower', 'upper' ],
    'cos':              [ 'x', 'y', 'obj_type' ],
    'cos~':             [ 'x', 'y', 'obj_type' ],
    'sin':              [ 'x', 'y', 'obj_type' ],
    'tan':              [ 'x', 'y', 'obj_type' ],
    'atan':             [ 'x', 'y', 'obj_type' ],
    'atan2':            [ 'x', 'y', 'obj_type' ],
    'dac~':             [ 'x', 'y', 'obj_type', 'outputs' ],
    'rmstodb':          [ 'x', 'y', 'obj_type' ],
    'dbtopow':          [ 'x', 'y', 'obj_type' ],
    'dbtorms':          [ 'x', 'y', 'obj_type' ],
    'powtodb':          [ 'x', 'y', 'obj_type' ],
    'declare':          [ 'x', 'y', 'params' ],
    'delay':            [ 'x', 'y', 'obj_type', 'ms' ],
    'delwrite~':        [ 'x', 'y', 'obj_type', 'buf', 'ms'],
    'delread~':         [ 'x', 'y', 'obj_type', 'buf', 'ms'],
    'vd~':              [ 'x', 'y', 'obj_type', 'params' ],
    'div':              [ 'x', 'y', 'obj_type', 'rhs' ],
    'drawcurve':        [ 'x', 'y', 'obj_type', 'params' ],
    'drawnumber':       [ 'x', 'y', 'obj_type', 'params' ],
    'drawpolygon':      [ 'x', 'y', 'obj_type', 'params' ],
    'drawsymbol':       [ 'x', 'y', 'obj_type', 'params' ],
    'drunk':            [ 'x', 'y', 'obj_type', 'upper', 'step' ],
    'element':          [ 'x', 'y', 'obj_type', 'params' ],
    'env~':             [ 'x', 'y', 'obj_type', 'window', 'period' ],
    'exp':              [ 'x', 'y', 'obj_type', 'params' ],
    'expr':             [ 'x', 'y', 'obj_type', 'params' ],
    'expr~':            [ 'x', 'y', 'obj_type', 'params' ],
    'filledcurve':      [ 'x', 'y', 'obj_type', 'params' ],
    'filledpolygon':    [ 'x', 'y', 'obj_type', 'params' ],
    'float':            [ 'x', 'y', 'obj_type', 'params' ],
    'get':              [ 'x', 'y', 'obj_type', 'params' ],
    'getsize':          [ 'x', 'y', 'obj_type', 'params' ],
    'hip~':             [ 'x', 'y', 'obj_type', 'freq' ],
    'image':            [ 'x', 'y', 'obj_type', 'params' ],
    'inlet':            [ 'x', 'y', 'obj_type', 'params' ],
    'inlet~':           [ 'x', 'y', 'obj_type', 'params' ],
    'int':              [ 'x', 'y', 'obj_type', 'params' ],
    'line':             [ 'x', 'y', 'obj_type', 'params' ],
    'line~':            [ 'x', 'y', 'obj_type', 'params' ],
    'loadbang':         [ 'x', 'y', 'obj_type' ],
    'log':              [ 'x', 'y', 'obj_type' 'params' ],
    'lop~':             [ 'x', 'y', 'obj_type', 'freq' ],
    'makefilename':     [ 'x', 'y', 'obj_type', 'params' ],
    'makenote':         [ 'x', 'y', 'obj_type', 'params' ],
    'stripnote':        [ 'x', 'y', 'obj_type' ],
    'makesymbol':       [ 'x', 'y', 'obj_type', 'params' ],
    'max':              [ 'x', 'y', 'obj_type', 'params' ],
    'max~':             [ 'x', 'y', 'obj_type' ],
    'metro':            [ 'x', 'y', 'obj_type', 'params' ],
    'min':              [ 'x', 'y', 'obj_type', 'params' ],
    'mod':              [ 'x', 'y', 'obj_type', 'params' ],
    'moses':            [ 'x', 'y', 'obj_type', 'value' ],
    'mtof':             [ 'x', 'y', 'obj_type' ],
    'ftom':             [ 'x', 'y', 'obj_type' ],
    'noise~':           [ 'x', 'y', 'obj_type' ],
    'outlet':           [ 'x', 'y', 'obj_type', 'params' ],
    'outlet~':          [ 'x', 'y', 'obj_type', 'params' ],
    'pack':             [ 'x', 'y', 'obj_type', 'params' ],
    'phasor~':          [ 'x', 'y', 'obj_type', 'freq' ],
    'pink~':            [ 'x', 'y', 'obj_type' ],
    'pipe':             [ 'x', 'y', 'obj_type', 'params' ],
    'pointer':          [ 'x', 'y', 'obj_type', 'params' ],
    'poly':             [ 'x', 'y', 'obj_type', 'params' ],
    'pow':              [ 'x', 'y', 'obj_type', 'params' ],
    'random':           [ 'x', 'y', 'obj_type', 'params' ],
    'readsf~':          [ 'x', 'y', 'obj_type', 'params' ],
    'dmstodb':          [ 'x', 'y', 'obj_type' ],
    'route':            [ 'x', 'y', 'obj_type', 'params' ],
    'fft~':             [ 'x', 'y', 'obj_type', 'params' ],
    'ifft~':            [ 'x', 'y', 'obj_type', 'params' ],
    'rfft~':            [ 'x', 'y', 'obj_type', 'params' ],
    'rifft~':           [ 'x', 'y', 'obj_type', 'params' ],
    'framp~':           [ 'x', 'y', 'obj_type' ],
    'samphold~':        [ 'x', 'y', 'obj_type' ],
    'samplerate~':      [ 'x', 'y', 'obj_type' ],
    'select':           [ 'x', 'y', 'obj_type', 'params' ],
    'set':              [ 'x', 'y', 'obj_type', 'params' ],
    'setsize':          [ 'x', 'y', 'obj_type', 'params' ],
    'sig~':             [ 'x', 'y', 'obj_type', 'params' ],
    'snapshot~':        [ 'x', 'y', 'obj_type', 'params' ],
    'vsnapshot~':       [ 'x', 'y', 'obj_type', 'params' ],
    'spigot':           [ 'x', 'y', 'obj_type', 'params' ],
    'sqrt':             [ 'x', 'y', 'obj_type', 'params' ],
    'struct':           [ 'x', 'y', 'obj_type', 'params' ],
    'swap':             [ 'x', 'y', 'obj_type', 'params' ],
    'switch~':          [ 'x', 'y', 'obj_type', 'params' ],
    'symbol':           [ 'x', 'y', 'obj_type', 'params' ],
    'symbolarray':      [ 'x', 'y', 'obj_type', 'params' ],
    'table':            [ 'x', 'y', 'obj_type', 'params' ],
    'tabosc4~':         [ 'x', 'y', 'obj_type', 'params' ],
    'tabread':          [ 'x', 'y', 'obj_type', 'params' ],
    'tabread~':         [ 'x', 'y', 'obj_type', 'params' ],
    'tabread4':         [ 'x', 'y', 'obj_type', 'params' ],
    'tabread4~':        [ 'x', 'y', 'obj_type', 'params' ],
    'tabreceive~':      [ 'x', 'y', 'obj_type', 'params' ],
    'tabwrite':         [ 'x', 'y', 'obj_type', 'params' ],
    'tabwrite~':        [ 'x', 'y', 'obj_type', 'params' ],
    'tabplay~':         [ 'x', 'y', 'obj_type', 'params' ],
    'throw~':           [ 'x', 'y', 'obj_type', 'params' ],
    'timer':            [ 'x', 'y', 'obj_type', 'params' ],
    'trigger':          [ 'x', 'y', 'obj_type', 'params' ],
    'union':            [ 'x', 'y', 'obj_type', 'params' ],
    'unique':           [ 'x', 'y', 'obj_type', 'params' ],
    'unpack':           [ 'x', 'y', 'obj_type', 'params' ],
    'until':            [ 'x', 'y', 'obj_type', 'params' ],
    'value':            [ 'x', 'y', 'obj_type', 'params' ],
    'vline~':           [ 'x', 'y', 'obj_type', 'params' ],
    'writesf~':         [ 'x', 'y', 'obj_type', 'params' ],
    'osc~':             [ 'x', 'y', 'obj_type', 'params' ],
    'plot':             [ 'x', 'y', 'obj_type', 'params' ],
    'soundfiler':       [ 'x', 'y', 'obj_type' ],
    'realtime':         [ 'x', 'y', 'obj_type', 'params' ],
    'cputime':          [ 'x', 'y', 'obj_type' ],
    'notein':           [ 'x', 'y', 'obj_type', 'channel' ],
    'ctlin':            [ 'x', 'y', 'obj_type', 'controller', 'channel' ],
    'pgmin':            [ 'x', 'y', 'obj_type', 'channel' ],
    'bendin':           [ 'x', 'y', 'obj_type', 'channel' ],
    'touchin':          [ 'x', 'y', 'obj_type', 'channel' ],
    'polytouchin':      [ 'x', 'y', 'obj_type', 'channel' ],
    'sysexin':          [ 'x', 'y', 'obj_type' ],
    'noteout':          [ 'x', 'y', 'obj_type', 'channel' ],
    'ctlout':           [ 'x', 'y', 'obj_type', 'controller', 'channel' ],
    'pgmout':           [ 'x', 'y', 'obj_type', 'channel' ],
    'bendout':          [ 'x', 'y', 'obj_type', 'channel' ],
    'touchout':         [ 'x', 'y', 'obj_type', 'channel' ],
    'polytouchout':     [ 'x', 'y', 'obj_type', 'channel' ],
    'serial':           [ 'x', 'y', 'obj_type', 'params' ],
    'receive':          [ 'x', 'y', 'obj_type', 'params' ],
    'bag':              [ 'x', 'y', 'obj_type' ],
    'vcf~':             [ 'x', 'y', 'obj_type', 'q' ],
    'rpole~':           [ 'x', 'y', 'obj_type', 're' ],
    'rzero~':           [ 'x', 'y', 'obj_type', 're' ],
    'rzero_rev~':       [ 'x', 'y', 'obj_type', 're' ],
    'cpole~':           [ 'x', 'y', 'obj_type', 're', 'im' ],
    'czero~':           [ 'x', 'y', 'obj_type', 're', 'im' ],
    'czero_rev~':       [ 'x', 'y', 'obj_type', 're', 'im' ],
    'import':           [ 'x', 'y', 'obj_type', 'name' ],
    'namecanvas':       [ 'x', 'y', 'name' ],
    'threshold~':       [ 'x', 'y', 'trig_val', 'deb_time',
                                    'rest_val', 'rest_time' ],
    'min~':             [ 'x', 'y', 'obj_type' ],
    'bang~':            [ 'x', 'y', 'obj_type' ],
    'netreceive':       [ 'x', 'y', 'obj_type', 'port_num', 'tcp_udp' ],
    'netsend':          [ 'x', 'y', 'obj_type', 'tcp_udp' ],
    'tabsend~':         [ 'x', 'y', 'obj_type', 'array_name' ],

    }

# Object Aliases
aliases = [ ('s', 'send'), ('s~', 'send~'),
            ('r', 'receive'), ('r~', 'receive~'),
            ('b', 'bang'), ('del', 'delay'),
            ('f', 'float'), ('i', 'int'),
            ('t', 'trigger'), ('sel', 'select'),
            ('v', 'value') ]

# add new dict keys for the aliases, pointing to existing values
OBJECT_DEFS.update([(a[0], OBJECT_DEFS[a[1]]) for a in aliases])


VANILLA_DEFS = {
    'abs~':      [ 'x', 'y', 'obj_type' ],

    'bng':       [ 'x', 'y', 'obj_type', 'size', 'hold', 'interrupt', 'init',
                   'send', 'receive', 'label', 'label_x', 'label_y', 'font',
                   'font_size', 'bg_color', 'fg_color', 'label_color' ],

    'clip~':     [ 'x', 'y', 'obj_type', 'lower', 'upper' ],

    'cnv':       [ 'x', 'y', 'obj_type', 'size', 'width', 'height', 'send',
                   'receive', 'label', 'label_x', 'label_y', 'font',
                   'font_size', 'bg_color', 'label_color', 'reserved' ],

    'dbtopow~':  [ 'x', 'y', 'obj_type' ],
    'dbtorms~':  [ 'x', 'y', 'obj_type' ],
    'exp~':      [ 'x', 'y', 'obj_type', 'log_base' ],
    'ftom~':     [ 'x', 'y', 'obj_type' ],

    'hradio':    [ 'x', 'y', 'obj_type', 'size', 'new_old', 'init', 'number',
                   'send', 'receive', 'label', 'label_x', 'label_y', 'font',
                   'font_size', 'bg_color', 'fg_color', 'label_color',
                   'default_value' ],

    'hslider':   [ 'x', 'y', 'obj_type', 'width', 'height', 'bottom', 'top',
                   'log', 'init', 'send', 'receive', 'label', 'label_x',
                   'label_y', 'font', 'font_size', 'bg_color', 'fg_color',
                   'label_color', 'default_value', 'steady_on_click' ],

    'key':       [ 'x', 'y', 'obj_type' ],
    'keyname':   [ 'x', 'y', 'obj_type' ],
    'keyup':     [ 'x', 'y', 'obj_type' ],
    'list':      [ 'x', 'y', 'obj_type', 'params' ],
    'log~':      [ 'x', 'y', 'obj_type', 'log_base' ],
    'mtof~':     [ 'x', 'y', 'obj_type' ],

    'nbx':       [ 'x', 'y', 'obj_type', 'size', 'height', 'min', 'max', 'log',
                   'init', 'send', 'receive', 'label', 'label_x', 'label_y',
                   'font', 'font_size', 'bg_color', 'fg_color', 'label_color',
                   'log_height' ],

    'openpanel': [ 'x', 'y', 'obj_type' ],
    'powtodb~':  [ 'x', 'y', 'obj_type' ],
    'pow~':      [ 'x', 'y', 'obj_type' ],
    'print':     [ 'x', 'y', 'obj_type', 'params' ],
    'print~':    [ 'x', 'y', 'obj_type' ],
    'qlist':     [ 'x', 'y', 'obj_type' ],
    'rmstodb~':  [ 'x', 'y', 'obj_type' ],
    'rsqrt~':    [ 'x', 'y', 'obj_type' ],
    'q8_rsqrt~': [ 'x', 'y', 'obj_type' ],
    'q8_sqrt~':  [ 'x', 'y', 'obj_type' ],
    'savepanel': [ 'x', 'y', 'obj_type' ],
    'sqrt~':     [ 'x', 'y', 'obj_type' ],
    'textfile':  [ 'x', 'y', 'obj_type' ],
    'toggle':    [ 'x', 'y', 'obj_type', 'size', 'init', 'send', 'receive',
                   'label', 'label_x', 'label_y', 'font', 'font_size',
                   'bg_color', 'fg_color', 'label_color', 'init_value',
                   'default_value' ],
    'vradio':    [ 'x', 'y', 'obj_type', 'size', 'new_old', 'init', 'number',
                   'send', 'receive', 'label', 'label_x', 'label_y', 'font',
                   'font_size', 'bg_color', 'fg_color', 'label_color',
                   'default_value' ],
    'vslider':   [ 'x', 'y', 'obj_type', 'width', 'height', 'bottom', 'top',
                   'log', 'init', 'send', 'receive', 'label', 'label_x',
                   'label_y', 'font', 'font_size', 'bg_color', 'fg_color',
                   'label_color', 'default_value', 'steady_on_click' ],
    'vu':        [ 'x', 'y', 'obj_type', 'width', 'height', 'receive',
                   'label', 'label_x', 'label_y', 'font', 'font_size',
                   'bg_color', 'label_color', 'scale', 'reserved' ],
    'wrap~':     [ 'x', 'y', 'obj_type' ]
        }


# Vanilla Aliases
aliases = [ ('vsl', 'vslider'), ('hsl', 'hslider'), ('tgl', 'toggle'),
             ('hdl', 'hradio'), ('vdl', 'vradio') ]

# add new dict keys for the aliases, pointing to existing values
VANILLA_DEFS.update([(a[0], VANILLA_DEFS[a[1]]) for a in aliases])

# For now add VANILLA_DEFS in OBJECT_DEFS.
OBJECT_DEFS.update(VANILLA_DEFS)

# Definition for array data
array_def = [ 'start_idx', 'values' ]


def get(name, params):
    """Return the element definition for the given arguments and a flag
       indicating whether we found an appropriate definition. If not we
       return the default minimal 'obj' definition, and False."""

    if name == 'obj':
        lenp = len(params)
        if lenp == 3 and params[2].isdigit():
            return (ELEMENT_DEFS['obj'], True)
        elif lenp >= 3:
            defn = OBJECT_DEFS.get(params[2])
            if defn:
                return (defn, True)
            else:
                # Return known if the object is just a number or dollar-arg,
                # otherwise it's an unknown abstraction.
                try:
                    sym = params[2]
                    if len(sym) > 2 and sym[:2] == '\$':
                        sym = sym[2:]
                        known = True
                    else:
                        float(sym)
                except ValueError, ex:
                    known = False
                return (ELEMENT_DEFS['obj'], known)
        else:
            return (ELEMENT_DEFS['obj'], True)
    else:
        return (ELEMENT_DEFS[name], True)
