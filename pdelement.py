
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
    'connect':          [ 'srcId', 'srcOut', 'tgtId', 'tgtOut' ],
    # special case for canvas on the first line
    'canvas0':          [ 'x', 'y', 'width', 'height', 'fontSize' ],
    'canvas':           [ 'x', 'y', 'width', 'height', 'name', 'openOnLoad' ],
    'array':            [ 'name', 'size', 'saveFlag' ],
    'coords':           [ 'x1', 'y2', 'x2', 'y1', 'width', 'heigth', 'gop' ],
    'floatatom':        [ 'x', 'y', 'width', 'lower', 'upper', 'labelPos',
                          'label', 'receive', 'send' ],
    'symbolatom':       [ 'x', 'y', 'width', 'lower', 'upper', 'labelPos',
                          'label', 'receive', 'send' ],
    'msg':              [ 'x', 'y', 'text' ],
    'obj':              [ 'x', 'y', 'objType', 'params' ],
    'restore':          [ 'x', 'y', 'graphFlag', 'name' ],
    'text':             [ 'x', 'y', 'text' ],
    'declare':          [ 'params' ]
    }

OBJECT_DEFS = {
    'inlet':            [ 'x', 'y', 'objType' ],
    'outlet':           [ 'x', 'y', 'objType' ],
    'send':             [ 'objType', 'dest', ],
    'send~':            [ 'objType', 'dest', ],
    'receive':          [ 'objType', 'src', ],
    'receive~':         [ 'objType', 'src', ],
    'pack':             [ 'x', 'y', 'objType' ],
    '!=':               [ 'x', 'y', 'objType', 'rhs' ],
    '%':                [ 'x', 'y', 'objType', 'rhs' ],
    '&':                [ 'x', 'y', 'objType', 'rhs' ],
    '&&':               [ 'x', 'y', 'objType', 'rhs' ],
    '*':                [ 'x', 'y', 'objType', 'rhs' ],
    '*~':               [ 'x', 'y', 'objType', 'rhs' ],
    '+':                [ 'x', 'y', 'objType', 'rhs' ],
    '+~':               [ 'x', 'y', 'objType', 'rhs' ],
    '-':                [ 'x', 'y', 'objType', 'rhs' ],
    '-~':               [ 'x', 'y', 'objType', 'rhs' ],
    '/':                [ 'x', 'y', 'objType', 'rhs' ],
    '/~':               [ 'x', 'y', 'objType', 'rhs' ],
    '<':                [ 'x', 'y', 'objType', 'rhs' ],
    '<=':               [ 'x', 'y', 'objType', 'rhs' ],
    '<~':               [ 'x', 'y', 'objType', 'rhs' ],
    '==':               [ 'x', 'y', 'objType', 'rhs' ],
    '>':                [ 'x', 'y', 'objType', 'rhs' ],
    '>=':               [ 'x', 'y', 'objType', 'rhs' ],
    '>>':               [ 'x', 'y', 'objType', 'rhs' ],
    '<<':               [ 'x', 'y', 'objType', 'rhs' ],
    '||':               [ 'x', 'y', 'objType', 'rhs' ],
    'abs':              [ 'x', 'y', 'objType' ],
    'adc~':             [ 'x', 'y', 'objType', 'inputs' ],
    'append':           [ 'x', 'y', 'objType', 'templateName', 'fields' ],
    'sublist':          [ 'x', 'y', 'objType', 'templateName', 'field' ],
    'arraysize':        [ 'x', 'y', 'objType', 'arrayName' ],
    'atan':             [ 'x', 'y', 'objType' ],
    'bang':             [ 'x', 'y', 'objType' ],
    'biquad~':          [ 'x', 'y', 'objType', 'params' ],
    'block~':           [ 'x', 'y', 'objType', 'size', 'overlap',
                          'resampling' ],
    'bp~':              [ 'x', 'y', 'objType', 'freq', 'q' ],
    'catch~':           [ 'x', 'y', 'objType', 'bus_name' ],
    'change':           [ 'x', 'y', 'objType', 'init' ],
    'clip':             [ 'x', 'y', 'objType', 'lower', 'upper' ],
    'cos':              [ 'x', 'y', 'objType' ],
    'cos~':             [ 'x', 'y', 'objType' ],
    'dac~':             [ 'x', 'y', 'objType', 'outputs' ],
    'rmstodb':          [ 'x', 'y', 'objType' ],
    'dbtopow':          [ 'x', 'y', 'objType' ],
    'dbtorms':          [ 'x', 'y', 'objType' ],
    'powtodb':          [ 'x', 'y', 'objType' ],
    'declare':          [ 'x', 'y', 'params' ],
    'delay':            [ 'x', 'y', 'objType', 'ms' ],
    'delwrite~':        [ 'x', 'y', 'objType', 'buf', 'ms'],
    'delread~':         [ 'x', 'y', 'objType', 'buf', 'ms'],
    'vd~':              [ 'x', 'y', 'objType', 'params' ],
    'div':              [ 'x', 'y', 'objType', 'rhs' ],
    'drawcurve':        [ 'x', 'y', 'objType', 'params' ],
    'drawnumber':       [ 'x', 'y', 'objType', 'params' ],
    'drawpolygon':      [ 'x', 'y', 'objType', 'params' ],
    'drawsymbol':       [ 'x', 'y', 'objType', 'params' ],
    'drunk':            [ 'x', 'y', 'objType', 'upper', 'step' ],
    'element':          [ 'x', 'y', 'objType', 'params' ],
    'env~':             [ 'x', 'y', 'objType', 'window', 'period' ],
    'exp':              [ 'x', 'y', 'objType', 'params' ],
    'expr':             [ 'x', 'y', 'objType', 'params' ],
    'expr~':            [ 'x', 'y', 'objType', 'params' ],
    'filledcurve':      [ 'x', 'y', 'objType', 'params' ],
    'filledpolygon':    [ 'x', 'y', 'objType', 'params' ],
    'float':            [ 'x', 'y', 'objType', 'params' ],
    'get':              [ 'x', 'y', 'objType', 'params' ],
    'getsize':          [ 'x', 'y', 'objType', 'params' ],
    'hip~':             [ 'x', 'y', 'objType', 'freq' ],
    'image':            [ 'x', 'y', 'objType', 'params' ],
    'inlet':            [ 'x', 'y', 'objType', 'params' ],
    'inlet~':           [ 'x', 'y', 'objType', 'params' ],
    'int':              [ 'x', 'y', 'objType', 'params' ],
    'line':             [ 'x', 'y', 'objType', 'params' ],
    'line~':            [ 'x', 'y', 'objType', 'params' ],
    'loadbang':         [ 'x', 'y', 'objType' ],
    'log':              [ 'x', 'y', 'objType' 'params' ],
    'lop~':             [ 'x', 'y', 'objType', 'freq' ],
    'makefilename':     [ 'x', 'y', 'objType', 'params' ],
    'makenote':         [ 'x', 'y', 'objType', 'params' ],
    'stripnote':        [ 'x', 'y', 'objType' ],
    'makesymbol':       [ 'x', 'y', 'objType', 'params' ],
    'max':              [ 'x', 'y', 'objType', 'params' ],
    'max~':             [ 'x', 'y', 'objType' ],
    'metro':            [ 'x', 'y', 'objType', 'params' ],
    'min':              [ 'x', 'y', 'objType', 'params' ],
    'mod':              [ 'x', 'y', 'objType', 'params' ],
    'moses':            [ 'x', 'y', 'objType', 'value' ],
    'mtof':             [ 'x', 'y', 'objType' ],
    'ftom':             [ 'x', 'y', 'objType' ],
    'noise~':           [ 'x', 'y', 'objType' ],
    'outlet':           [ 'x', 'y', 'objType', 'params' ],
    'outlet~':          [ 'x', 'y', 'objType', 'params' ],
    'pack':             [ 'x', 'y', 'objType', 'params' ],
    'phasor~':          [ 'x', 'y', 'objType', 'freq' ],
    'pink~':            [ 'x', 'y', 'objType' ],
    'pipe':             [ 'x', 'y', 'objType', 'params' ],
    'pointer':          [ 'x', 'y', 'objType', 'params' ],
    'poly':             [ 'x', 'y', 'objType', 'params' ],
    'pow':              [ 'x', 'y', 'objType', 'params' ],
    'random':           [ 'x', 'y', 'objType', 'params' ],
    'readsf~':          [ 'x', 'y', 'objType', 'params' ],
    'dmstodb':          [ 'x', 'y', 'objType' ],
    'route':            [ 'x', 'y', 'objType', 'params' ],
    'fft~':             [ 'x', 'y', 'objType', 'params' ],
    'ifft~':            [ 'x', 'y', 'objType', 'params' ],
    'rfft~':            [ 'x', 'y', 'objType', 'params' ],
    'rifft~':           [ 'x', 'y', 'objType', 'params' ],
    'framp~':           [ 'x', 'y', 'objType' ],
    'samphold~':        [ 'x', 'y', 'objType' ],
    'samplerate~':      [ 'x', 'y', 'objType' ],
    'select':           [ 'x', 'y', 'objType', 'params' ],
    'set':              [ 'x', 'y', 'objType', 'params' ],
    'setsize':          [ 'x', 'y', 'objType', 'params' ],
    'sig~':             [ 'x', 'y', 'objType', 'params' ],
    'sin':              [ 'x', 'y', 'objType', 'params' ],
    'snapshot~':        [ 'x', 'y', 'objType', 'params' ],
    'vsnapshot~':       [ 'x', 'y', 'objType', 'params' ],
    'spigot':           [ 'x', 'y', 'objType', 'params' ],
    'sqrt':             [ 'x', 'y', 'objType', 'params' ],
    'struct':           [ 'x', 'y', 'objType', 'params' ],
    'swap':             [ 'x', 'y', 'objType', 'params' ],
    'switch~':          [ 'x', 'y', 'objType', 'params' ],
    'symbol':           [ 'x', 'y', 'objType', 'params' ],
    'symbolarray':      [ 'x', 'y', 'objType', 'params' ],
    'table':            [ 'x', 'y', 'objType', 'params' ],
    'tabosc4~':         [ 'x', 'y', 'objType', 'params' ],
    'tabread':          [ 'x', 'y', 'objType', 'params' ],
    'tabread~':         [ 'x', 'y', 'objType', 'params' ],
    'tabread4~':        [ 'x', 'y', 'objType', 'params' ],
    'tabreceive~':      [ 'x', 'y', 'objType', 'params' ],
    'tabwrite':         [ 'x', 'y', 'objType', 'params' ],
    'tabwrite~':        [ 'x', 'y', 'objType', 'params' ],
    'tabplay~':         [ 'x', 'y', 'objType', 'params' ],
    'throw~':           [ 'x', 'y', 'objType', 'params' ],
    'timer':            [ 'x', 'y', 'objType', 'params' ],
    'trigger':          [ 'x', 'y', 'objType', 'params' ],
    'union':            [ 'x', 'y', 'objType', 'params' ],
    'unique':           [ 'x', 'y', 'objType', 'params' ],
    'unpack':           [ 'x', 'y', 'objType', 'params' ],
    'until':            [ 'x', 'y', 'objType', 'params' ],
    'value':            [ 'x', 'y', 'objType', 'params' ],
    'vline~':           [ 'x', 'y', 'objType', 'params' ],
    'writesf~':         [ 'x', 'y', 'objType', 'params' ],
    'osc~':             [ 'x', 'y', 'objType', 'params' ],
    'plot':             [ 'x', 'y', 'objType', 'params' ],
    'soundfiler':       [ 'x', 'y', 'objType' ],
    'realtime':         [ 'x', 'y', 'objType', 'params' ],
    'cputime':          [ 'x', 'y', 'objType' ],
    'notein':           [ 'x', 'y', 'objType', 'channel' ],
    'ctlin':            [ 'x', 'y', 'objType', 'controller', 'channel' ],
    'pgmin':            [ 'x', 'y', 'objType', 'channel' ],
    'bendin':           [ 'x', 'y', 'objType', 'channel' ],
    'touchin':          [ 'x', 'y', 'objType', 'channel' ],
    'polytouchin':      [ 'x', 'y', 'objType', 'channel' ],
    'sysexin':          [ 'x', 'y', 'objType' ],
    'noteout':          [ 'x', 'y', 'objType', 'channel' ],
    'ctlout':           [ 'x', 'y', 'objType', 'controller', 'channel' ],
    'pgmout':           [ 'x', 'y', 'objType', 'channel' ],
    'bendout':          [ 'x', 'y', 'objType', 'channel' ],
    'touchout':         [ 'x', 'y', 'objType', 'channel' ],
    'polytouchout':     [ 'x', 'y', 'objType', 'channel' ],
    'serial':           [ 'x', 'y', 'objType', 'params' ],
    'receive':          [ 'x', 'y', 'objType', 'params' ],
    'bag':              [ 'x', 'y', 'objType' ],
    'vcf~':             [ 'x', 'y', 'objType', 'q' ],
    'rpole~':           [ 'x', 'y', 'objType', 're' ],
    'rzero~':           [ 'x', 'y', 'objType', 're' ],
    'rzero_rev~':       [ 'x', 'y', 'objType', 're' ],
    'cpole~':           [ 'x', 'y', 'objType', 're', 'im' ],
    'czero~':           [ 'x', 'y', 'objType', 're', 'im' ],
    'czero_rev~':       [ 'x', 'y', 'objType', 're', 'im' ],
    'import':           [ 'x', 'y', 'objType', 'name' ],
    'namecanvas':       [ 'x', 'y', 'name' ],
    'threshold~':       [ 'x', 'y', 'trig_val', 'deb_time',
                                    'rest_val', 'rest_time' ],
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
    'abs~':      [ 'x', 'y', 'objType' ],

    'bng':       [ 'x', 'y', 'objType', 'size', 'hold', 'interrupt', 'init',
                   'send', 'receive', 'label', 'labelX', 'labelY', 'font',
                   'fontSize', 'bgColor', 'fgColor', 'labelColor' ],

    'clip~':     [ 'x', 'y', 'objType', 'lower', 'upper' ],

    'cnv':       [ 'x', 'y', 'objType', 'size', 'width', 'height', 'send',
                   'receive', 'label', 'labelX', 'labelY', 'font', 'fontSize',
                   'bgColor', 'labelColor', 'reserved' ],

    'dbtopow~':  [ 'x', 'y', 'objType' ],
    'dbtorms~':  [ 'x', 'y', 'objType' ],
    'exp~':      [ 'x', 'y', 'objType', 'logBase' ],
    'ftom~':     [ 'x', 'y', 'objType' ],

    'hradio':    [ 'x', 'y', 'objType', 'size', 'newOld', 'init', 'number',
                   'send', 'receive', 'label', 'labelX', 'labelY', 'font',
                   'fontSize', 'bgColor', 'fgColor', 'labelColor',
                   'defaultValue' ],

    'hslider':   [ 'x', 'y', 'objType', 'width', 'height', 'bottom', 'top',
                   'log', 'init', 'send', 'receive', 'label', 'labelX',
                   'labelY', 'font', 'fontSize', 'bgColor', 'fgColor',
                   'labelColor', 'defaultValue', 'steadyOnClick' ],

    'key':       [ 'x', 'y', 'objType' ],
    'keyname':   [ 'x', 'y', 'objType' ],
    'keyup':     [ 'x', 'y', 'objType' ],
    'list':      [ 'x', 'y', 'objType', 'params' ],
    'log~':      [ 'x', 'y', 'objType', 'logBase' ],
    'mtof~':     [ 'x', 'y', 'objType' ],

    'nbx':       [ 'x', 'y', 'objType', 'size', 'height', 'min', 'max', 'log',
                   'init', 'send', 'receive', 'label', 'labelX', 'labelY',
                   'font', 'fontSize', 'bgColor', 'fgColor', 'labelColor',
                   'logHeight' ],

    'openpanel': [ 'x', 'y', 'objType' ],
    'powtodb~':  [ 'x', 'y', 'objType' ],
    'pow~':      [ 'x', 'y', 'objType' ],
    'print':     [ 'x', 'y', 'objType', 'params' ],
    'print~':    [ 'x', 'y', 'objType' ],
    'qlist':     [ 'x', 'y', 'objType' ],
    'rmstodb~':  [ 'x', 'y', 'objType' ],
    'rsqrt~':    [ 'x', 'y', 'objType' ],
    'q8_rsqrt~': [ 'x', 'y', 'objType' ],
    'q8_sqrt~':  [ 'x', 'y', 'objType' ],
    'savepanel': [ 'x', 'y', 'objType' ],
    'sqrt~':     [ 'x', 'y', 'objType' ],
    'textfile':  [ 'x', 'y', 'objType' ],

    'toggle':    [ 'x', 'y', 'objType', 'size', 'init', 'send', 'receive',
                   'label', 'labelX', 'labelY', 'font', 'fontSize', 'bgColor',
                   'fgColor', 'labelColor', 'initValue', 'defaultValue' ],

    'vradio':    [ 'x', 'y', 'objType', 'size', 'newOld', 'init', 'number',
                   'send', 'receive', 'label', 'labelX', 'labelY', 'font',
                   'fontSize', 'bgColor', 'fgColor', 'labelColor',
                   'defaultValue' ],

    'vslider':   [ 'x', 'y', 'objType', 'width', 'height', 'bottom', 'top',
                   'log', 'init', 'send', 'receive', 'label', 'labelX',
                   'labelY', 'font', 'fontSize', 'bgColor', 'fgColor',
                   'labelColor', 'defaultValue', 'steadyOnClick' ],
    'vu':        [ 'x', 'y', 'objType', 'width', 'height', 'receive',
                   'label', 'labelX', 'labelY', 'font', 'fontSize',
                   'bgColor', 'labelColor', 'scale', 'reserved' ],
    'wrap~':     [ 'x', 'y', 'objType' ]
        }


# Vanilla Aliases
aliases = [ ('vsl', 'vslider'), ('hsl', 'hslider'), ('tgl', 'toggle'),
             ('hdl', 'hradio'), ('vdl', 'vradio') ]

# add new dict keys for the aliases, pointing to existing values
VANILLA_DEFS.update([(a[0], VANILLA_DEFS[a[1]]) for a in aliases])

array_def = [ 'start_idx', 'values' ]


# For now add VANILLA_DEFS in OBJECT_DEFS.
OBJECT_DEFS.update(VANILLA_DEFS)

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
                # Return known if the object is just a number, otherwise it's
                # an unknown abstraction.
                try:
                    sym = params[2]
                    if len(sym) > 2 and sym[:2] == '\$':
                        sym = sym[2:]
                    float(sym)
                    known = True
                except ValueError, ex:
                    known = False
                return (ELEMENT_DEFS['obj'], known)
        else:
            return (ELEMENT_DEFS['obj'], True)
    else:
        return (ELEMENT_DEFS[name], True)

def t(x):
    import ConfigParser
    c=ConfigParser.RawConfigParser()

    c.read('pdelement.cfg')
    line = c.get('objects',x)
    attrs = [a.strip() for a in line.split(',')]
    return attrs
