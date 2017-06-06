#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import pytest

from erfc.get import parse_rfc_numbers, postprocess_paragraph


class TestParseRfcNumbers():
    def test_corner_cases(self):
        assert [] == parse_rfc_numbers([])
        assert [402] == parse_rfc_numbers(['402'])
        assert [200, 201, 202] == parse_rfc_numbers(['200-202'])
        assert [200, 201, 202, 203] == parse_rfc_numbers(['200-202', '203'])

    def test_various_ranges(self):
        arg_numbers = ['100', '101', '102-104', '105', '110-112']
        rfc_numbers = [100, 101, 102, 103, 104, 105, 110, 111, 112]

        assert rfc_numbers == parse_rfc_numbers(arg_numbers)


class TestPostprocessText():
    def test_spaces(self):
        '''
        Given a string with redundant whitespace, removes it while preserving
        sentence terminating symbols (?!.).
        '''
        pre = ('This document!    describes PNG (Portable Network Graphics),  '
               'an   extensible file format.  for the  storage?  of raster'
               'images.')
        post = ('This document! describes PNG (Portable Network Graphics), '
                'an extensible file format. for the storage? of raster'
                'images.')

        assert postprocess_paragraph(pre) == post

    def test_hyphens(self):
        '''
        Given a string with redundant whitespace after hyphens, removes it
        to match space before hyphen (if any).
        '''
        pre = 'some text -    some other text'
        post = 'some text - some other text'
        pre_range = '1-    2'
        post_range = '1-2'

        assert postprocess_paragraph(pre) == post
        assert postprocess_paragraph(pre_range) == post_range
