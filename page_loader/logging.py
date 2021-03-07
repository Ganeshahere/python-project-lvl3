from logging import basicConfig as bC
from logging import DEBUG
import sys


def setup():
    bC(level=DEBUG, stream=sys.stderr, format='%(levelname)s:%(message)s')
