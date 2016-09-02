# -*- coding: utf-8 -*-

from __future__ import print_function
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
    if not os.path.isfile(file_path):
        raiseError(file_path, u"does not exist")

    filetime = datetime.fromtimestamp(os.path.getctime(file_path))
    cachetime = datetime.fromtimestamp(os.path.getctime(cache_path))
    return filetime < cachetime

def check_path(path):
    path = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(path):
        raiseError(u"file:'%s' not found" % path)
    return path

def raiseError(*args):
    plug_error = u"Citation.vim error:"
    print(plug_error, *args)
    raise RuntimeError(plug_error, args)
