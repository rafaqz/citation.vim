# -*- coding: utf-8 -*-

import sys
import os.path
from datetime import datetime, timedelta

def compat_str(string):
    if sys.version_info[0] == 2:
        return unicode(string)
    elif sys.version_info[0] == 3:
        return str(string)

def is_current(file_path, cache_path):
    if not os.path.isfile(cache_path):
        return False
    filetime = datetime.fromtimestamp(os.path.getctime(file_path))
    cachetime = datetime.fromtimestamp(os.path.getctime(cache_path))
    return filetime < cachetime

