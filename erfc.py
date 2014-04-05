#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
eRFC

Usage:
    erfc get <rfc_numbers>... [--save-to=<path>]

Options:
    -h, --help          Show this screen.
    --save-to=<path>    Path to a folder where RFC will be stored
                        [default: rfcs].

'''
import sys

from docopt import docopt

from erfc.get import get_rfcs


def main(args):
    get_rfcs(args['<rfc_numbers>'], args['--save-to'])

if __name__ == '__main__':
    args = docopt(__doc__)
    sys.exit(main(args))
