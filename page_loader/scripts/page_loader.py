#!/usr/bin/env/ python3
import sys
from page_loader.cli import get_parser
from page_loader import loading
import logging
from page_loader.logging import set_logging


def main():
    try:
        set_logging()
        logging.info('Start downloading...')
        parser = get_parser()
        args = parser.parse_args()
        path_to_downloaded = loading(args.url, args.output)
    except Exception as er:
        logging.error(f"{er}")
        sys.exit(1)
    else:
        print(f"Successfully! Page is downloaded into '{path_to_downloaded}'")
        logging.info('Download finished.')


if __name__ == '__main__':
    main()
