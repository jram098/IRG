__version__ = '1.0'

print('using IR Mark I v{} ...'.format(__version__))

import sys

if sys.version_info.major < 3:
    msg = 'IR Mark I Requires Python 3.4 or greater. You are using {}'.format(sys.version)
    raise ValueError(msg)

from . import parts
from .vehicle import Vehicle
from .memory import Memory
from . import utils
from . import config
from . import contrib
from .config import load_config
