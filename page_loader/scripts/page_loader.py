#!/usr/bin/env/ python3
from page_loader.cli import get_parser
from page_loader import loading


def main():
    parser = get_parser()
    args = parser.parse_args()
    path_to_downloaded = loading(args.url, args.output)
    print(path_to_downloaded)


if __name__ == '__main__':
    main()
