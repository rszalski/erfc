#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Handles RFC fetching.
'''
import os
import re

import requests


RFC_URL = 'http://tools.ietf.org/rfc/rfc'
RFC_FORMAT = 'txt'


def parse_rfc_numbers(numbers):
    '''
    Parses RFC numbers, given in arguments, to a list of ints.

    :numbers:   Valid integers or ranges thereof, passed as CLI args,
                e.g., ['100', '101-103']
    :return:    A list of RFC numbers, e.g., [100, 101, 102, 103]
    '''
    nums = []

    for arg in numbers:
        if '-' in arg:
            start, end = map(int, arg.split('-'))
            nums.extend(range(start, end + 1))
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


def postprocess_text(par):
    '''
    Changes more than 2 spaces to a single space in paragraphs.
    '''
    # TODO Change name to postprocess_paragraph or a better name
    # TODO Explain pattern
    # TODO Handle hyphens/minuses separately (1 - 2 vs. 1-2 etc.)
    pattern = re.compile(r'(\b|[.!?-])[ ]{2,}\b')

    # \g<1> preserves a terminating char (.|?|! etc.) that would otherwise be
    # changed to a single space.
    new_text = [re.sub(pattern, '\g<1> ', line) for line in par]

    return ''.join(new_text)


def format_document(data):
    '''
    Tries to analyze type of each line and make a more aware decisions.

    This approach tries analyze each line of file and choose if removing
    linebreaks is reasonable.
    '''
    data = data.splitlines(True)
    new_text = []

    # Variable useful when deleting lines
    lines_to_del = 0

    # Variable storing the state of parser (ex. paragraph, enumeration,
    # equation etc.)
    state = None

    # Often used regexps - compiling them should make it a bit quicker.
    re_table_of_content = re.compile(r'\.{5}?[ ]+[0-9]')
    re_page = re.compile(r'\[Page [0-9]+\]')
    re_start_of_paragraph = re.compile(r'^[ ]{3,9}[A-Z][a-z]|^[ ]{3,9}A[ ]|^[ ]{3,9}PNG')

    for line in data:
        if lines_to_del:
            lines_to_del -= 1
            continue
        elif line[0] == '\n':
            state = None
            new_text.append(line)
        elif state:
            if state == 'paragraph':
                line = re.sub(r'\n|\r\n|\r*', '', line)
                new_text.append(line)
        elif re_table_of_content.search(line):
            new_text.append(line)
        elif re_page.search(line):
            lines_to_del = 3
        elif re_start_of_paragraph.search(line):
            state = 'paragraph'
            line = re.sub(r'\n|\r\n|\r*', '', line)
            new_text.append(line)
        else:
            new_text.append(line)

    new_test = postprocess_text(new_text)

    return ''.join(new_test)


def write_rfc(data, number, path):
    filename = 'rfc{}.{}'.format(number, RFC_FORMAT)
    rfc_path = os.path.join(path, filename)
    rfc_dir = os.path.dirname(rfc_path)
    data = format_document(data)

    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)

    with open(rfc_path, 'w') as rfc_file:
        rfc_file.write(data)
        print('\tWritten RFC in {}.'.format(rfc_path))
