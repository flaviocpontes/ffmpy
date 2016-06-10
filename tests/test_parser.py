#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ffmpymedia import __author__, __version__, __copyright__, __package__

import os.path
import datetime
import unittest
import ffmpymedia.parser as parser


class TestDecodeDateString(unittest.TestCase):

    def test_empty_string(self):
        self.assertRaises(ValueError, parser.decodedatetime, '')

    def test_invalid_date(self):
        self.assertRaises(ValueError, parser.decodedatetime, 'aAFsakhjhhkashkj')

    def test_valid_timestamp(self):
        self.assertEqual(parser.decodedatetime('2014-01-01 00:00:00'),
                         datetime.datetime(2014, 1, 1, 00, 00, 00))

    def test_valid_timestamp2(self):
        self.assertEqual(parser.decodedatetime('1989-04-16 23:18:59'),
                         datetime.datetime(1989, 4, 16, 23, 18, 59))

    def test_invalid_timestamp(self):
        self.assertRaises(ValueError, parser.decodedatetime, '1950-01-59 26:63:49')

    def test_invalid_timestamp2(self):
        self.assertRaises(ValueError, parser.decodedatetime, '1100-13-18 14:18:49')

    def test_valid_date_string(self):
        self.assertEqual(parser.decodedatetime('May 15 2014 15:42:07'),
                         datetime.datetime(2014, 5, 15, 15, 42, 7))

    def test_valid_date_string2(self):
        self.assertEqual(parser.decodedatetime('Oct 18 1979 09:14:16'),
                         datetime.datetime(1979, 10, 18, 9, 14, 16))

    def test_invalid_date_string(self):
        self.assertRaises(ValueError, parser.decodedatetime, 'Nov 32 2853 15:25:02')

    def test_invalid_date_string2(self):
        self.assertRaises(ValueError, parser.decodedatetime, 'Jul 87 1977 9:10:15')


class TesteProbeContext(unittest.TestCase):
    def test_invalid_object(self):
        self.assertRaises(ValueError, parser.ProbeContext, {})

    def test_empty_string(self):
        p = parser.ProbeContext('')
        self.assertEqual({'header': {}}, p.process())

    def test_invalid_input(self):
        self.assertRaises(ValueError, parser.ProbeContext, True)

