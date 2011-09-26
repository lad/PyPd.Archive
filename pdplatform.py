
import platform
import os

# TODO What does the mac return?

home = os.environ['HOME']

(UNIX, WIN, MAC, UNKNOWN) = range(4)
home_dirs = { UNIX: os.path.join(home, '.pypd'),
              WIN:  os.path.join(home, 'AppData', 'Local', 'PyPD'),
              MAC:  os.path.join(home, 'Library', 'Preferences', 'PyPD') }

# Platform values don't change so we setup some global constants on import
#     gPlatform, gPrefDir, gPrefFile

_plat = platform.system().lower()
# would be nice to have a dict that looks up keys with .startswith
# instead of this.
if _plat.startswith('linux') or _plat.startswith('cygwin'):
    platform = UNIX
elif _plat.startswith('windows'):
    platform = WIN
elif _plat.startswith('mac'):
    platform = MAC
else:
    platform = UNKNOWN

pref_dir = home_dirs[platform]
pref_file = os.path.join(pref_dir, 'prefs')
