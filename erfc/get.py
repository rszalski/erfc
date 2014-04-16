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


def postprocess_paragraph(par):
    '''
    Changes more than 2 spaces to a single space in paragraphs.

    :par:   A paragraph of text as a single string.
    '''
    # In case of whitespace before hyphen, we preserve that for symmetry.
    hyphen_pattern = re.compile('''
    ([ ]*)  # Match 0 or more space before hyphen, store in subgroup 1.
    (-)     # Match hyphen, store in subgroup 2.
    [ ]+    # Match redundant spaces after hyphen.
    ''', re.VERBOSE)
    par = re.sub(hyphen_pattern, '\g<1>\g<2>\g<1>', par)

    pattern = re.compile('''
    (\\b|[,.!?])    # Match either a word boundary or a sentence-terminating
                    # character, store in a subgroup 1.
    [ ]{2,}         # Match 2 or more spaces.
    \\b             # Word boundary.
    ''', re.VERBOSE)
    # \g<1> preserves a terminating char (.|?|! etc.) that would otherwise be
    # changed to a single space.
    return re.sub(pattern, '\g<1> ', par)


def format_document(data):
    '''
    Decides whether removing linebreaks at a given line is reasonable.
    '''
    data = data.splitlines(True)
    new_text = []

    lines_to_del = 0

    # Variable storing the state of parser (e.g., paragraph, enumeration,
    # equation etc.)
    state = None

    re_toc = re.compile(r'\.{5}?[ ]+[0-9]')
    re_page = re.compile(r'\[Page [0-9]+\]')
    re_start_of_paragraph = re.compile(r'''
        ^[ ]{3,9}[A-Z][a-z]|^[ ]{3,9}A[ ]|^[ ]{3,9}PNG
    ''')

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
        elif re_toc.search(line):
            new_text.append(line)
        elif re_page.search(line):
            lines_to_del = 3
        elif re_start_of_paragraph.search(line):
            state = 'paragraph'
            line = re.sub(r'\n|\r\n|\r*', '', line)
            new_text.append(line)
        else:
            new_text.append(line)

    # Postprocess acts on a whole string
    return postprocess_paragraph(''.join(new_text))


def write_rfc(data, number, path):
    filename = 'rfc{}.{}'.format(number, RFC_FORMAT)
    rfc_path = os.path.join(path, filename)
    rfc_dir = os.path.dirname(rfc_path)
    data = format_document(data)

    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)

    with open(rfc_path, 'w') as rfc_file:
        rfc_file.write(data)
        print('\tSaved RFC in {}.'.format(rfc_path))
