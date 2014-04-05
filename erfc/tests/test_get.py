#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import pytest

from erfc.get import parse_rfc_numbers


class TestParseRfcNumbers():
    def test_empty_numbers(self):
        assert [] == parse_rfc_numbers([])

    def test_various_ranges(self):
        arg_numbers = ['100', '101', '102-104', '105', '110-112']
        rfc_numbers = [100, 101, 102, 103, 104, 105, 110, 111, 112]

        assert rfc_numbers == parse_rfc_numbers(arg_numbers)
