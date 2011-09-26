#!/usr/bin/env python

import pdconfig
import pdplatform

cfg = pdconfig.PdConfigParser(pdplatform.pref_file)
print cfg.get('pd_root')
print cfg.get_startswith('include')
