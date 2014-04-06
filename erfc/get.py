#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Handles RFC fetching.
'''
import os

import requests


RFC_URL = 'http://tools.ietf.org/rfc/rfc'
RFC_FORMAT = 'txt'


def parse_rfc_numbers(numbers):
    '''
    '''
    nums = []

    for arg in numbers:
        if '-' in arg:
            (start, end) = arg.split('-')
            nums.extend(range(int(start), int(end) + 1))
        else:
            nums.append(int(arg))

    return nums


def get_rfcs(args):
    rfc_numbers = parse_rfc_numbers(args['<rfc_numbers>'])
    print('Requested RFCs: {}\n'.format(rfc_numbers))

    for rfc_number in rfc_numbers:
        print('Getting RFC{}...'.format(rfc_number))
        rfc_url = '{}{}.{}'.format(RFC_URL, rfc_number, RFC_FORMAT)
        r = requests.get(rfc_url)
        print('\tDone.')
        write_rfc(r.text, rfc_number, args['--save-to'])


def write_rfc(data, number, path):
    filename = 'rfc{}.{}'.format(number, RFC_FORMAT)
    rfc_path = os.path.join(path, filename)
    rfc_dir = os.path.dirname(rfc_path)

    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)

    with open(rfc_path, 'w') as rfc_file:
        rfc_file.write(data)
        print('\tWritten RFC in {}.'.format(rfc_path))
