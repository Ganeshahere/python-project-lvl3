import logging as log


def set_logging():
    log.basicConfig(level=log.info, format='%(levelname)s: %(message)s')
