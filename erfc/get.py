#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Handles RFC fetching.
'''
import os

import requests


RFC_URL = 'http://tools.ietf.org/rfc/rfc'
RFC_FORMAT = 'txt'


def get_rfcs(rfc_numbers, path):
    for rfc_number in rfc_numbers:
        rfc_url = '{}{}.{}'.format(RFC_URL, rfc_number, RFC_FORMAT)
        r = requests.get(rfc_url)
        write_rfc(r.text, rfc_number, path)


def write_rfc(data, number, path):
    filename = 'rfc{}.{}'.format(number, RFC_FORMAT)
    rfc_path = os.path.join(path, filename)
    rfc_dir = os.path.dirname(rfc_path)

    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)

    with open(rfc_path, 'w') as rfc_file:
        rfc_file.write(data)
