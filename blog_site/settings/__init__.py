# settings/__init__.py

from .settings import *

try:
    from .settings_dev import *
except:
    pass
