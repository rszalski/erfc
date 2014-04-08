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
    Parses RFC numbers to a list of ints.

    :numbers:   Valid integers or ranges of thereof passed as CLI args,
                e.g., ['100', '101-103']
    :return:    A list of RFC numbers, e.g., [100, 101, 102, 103]
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


def normalize_newlines(data):
    '''
    Removes explicit linebreaks, so that text can flow freely on an eReader.

    Current approach is to define a line width threshold, above which
    linebreaks are removed (if not preceded by a full stop) together with
    following whitespace.
    '''
    # TODO Clean & Optimize.
    # TODO Find a better heuristic.
    width_threshold = 60
    data = data.splitlines(True)
    new_text = []

    for line in data:
        if len(line) > width_threshold:
            line = re.sub(r'(?<!\.)(\n|\r\n|\r)+[\t ]*', '', line)

        new_text.append(line)

    return ''.join(new_text)

def postprocess_text(data):
    '''
    Doing the postprocessing such as removing multiple spaces and so on.


    '''
    
    return ''.join(data)

def format_document(data):
    '''
    Tries to analyze type of each line and make a more aware decisions.

    This approach tries analyze each line of file and choose if removing 
    linebreaks is reasonable. 
    '''

    data = data.splitlines(True)
    new_text = []
   
    #Variable useful when deleting lines
    lines_to_del = 0

    #Variable storing the state of parser (ex. paragraph, enumeration, equation etc.)
    state = None

    #Often used regexps - compiling them should make it a bit quicker.
    re_table_of_content = re.compile(r'\.{5}?[ ]+[0-9]')
    re_page = re.compile(r'\[Page [0-9]+\]')
    re_start_of_paragraph = re.compile(r'^[ ]{3,9}[A-Z][a-z]|^[ ]{3,9}A[ ]|^[ ]{3,9}PNG')
    
    for line in data:
        if lines_to_del:
            lines_to_del-=1
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
            lines_to_del=3

        elif re_start_of_paragraph.search(line):
            state = 'paragraph'
            line = re.sub(r'\n|\r\n|\r*', '', line)
            new_text.append(line)
    
        else:
            new_text.append(line)
    
    new_test = postprocess_text(new_test)

    return ''.join(new_text)
    
def write_rfc(data, number, path):
    filename = 'rfc{}.{}'.format(number, RFC_FORMAT)
    rfc_path = os.path.join(path, filename)
    rfc_dir = os.path.dirname(rfc_path)
    #data = normalize_newlines(data)
    data = format_document(data)

    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)

    with open(rfc_path, 'w') as rfc_file:
        rfc_file.write(data)
        print('\tWritten RFC in {}.'.format(rfc_path))
