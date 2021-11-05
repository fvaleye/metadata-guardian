import sys

from loguru import logger

from .data_rules import *
from .report import *
from .scanner import *
from .source import *

logger.remove()
logger.add(sys.stderr, level="INFO")
