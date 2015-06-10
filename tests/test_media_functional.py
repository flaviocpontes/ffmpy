#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __init__ import __author__, __version__, __copyright__, __package__

import unittest
import ffmpy

class TestMediaUse(unittest.TestCase):

    def test_compare_two_files(self):
        # User1 wants to compare two media files to see if their stream layouts are the same.
        # First he passes the same file to the API to see if they compare as the same
        filename1 = filename2 = 'test_files/SIN001 Sinuca.mp4'
        self.assertEqual(ffmpy.MediaFile.parse_file(filename1), ffmpy.MediaFile.parse_file(filename2))

        # Then he wants to be sure and see th

