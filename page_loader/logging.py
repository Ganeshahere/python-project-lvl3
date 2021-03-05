from logging import basicConfig as bC
from logging import INFO
import sys


def set_logging():
    bC(level=INFO, stream=sys.stderr, format='%(levelname)s:%(message)s')
