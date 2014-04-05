#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
eRFC

Usage:
    erfc get <rfc_number>...

Options:
    -h, --help      Show this screen.

'''
import sys

from docopt import docopt


def main():
    pass

if __name__ == '__main__':
    args = docopt(__doc__)
    sys.exit(main())
