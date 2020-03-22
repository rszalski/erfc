#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
eRFC downloads and formats plain-text RFCs to fit eReaders nicely.

Usage:
    erfc get <rfc_numbers>... [--save-to=<path>]

Options:
    -h, --help              Show this screen.
    -s, --save-to=<path>    Path to a folder where RFC will be stored
                            [default: rfcs].

'''
import sys

from docopt import docopt

from erfc.get import get_rfcs


def main():
    args = docopt(__doc__)
    get_rfcs(args)


if __name__ == '__main__':
    sys.exit(main())
