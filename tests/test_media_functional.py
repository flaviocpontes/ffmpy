#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from os.path import join as joinpath

import ffmpy

from tests import TEST_FILE_PATH

class TestMediaUse(unittest.TestCase):

    def test_compare_two_files(self):
        # User1 wants to compare two media files to see if their stream layouts are the same.
        # First he passes the same file to the API to see if they compare as the same
        filename1 = filename2 = joinpath(TEST_FILE_PATH, 'SIN001 Sinuca.mp4')
        file1 = ffmpy.MediaFile.parse_file(filename1)
        file2 = ffmpy.MediaFile.parse_file(filename2)
        self.assertTrue(file1 == file2)

        # Then he wants to be sure and see the that difference between the two files is {}
        self.assertEqual(ffmpy.MediaFile.parse_file(filename1).difference(ffmpy.MediaFile.parse_file(filename2)), {})

        # Then he decides to try two different files to be sure different files are treated differenty
        filename3 = joinpath(TEST_FILE_PATH, 'COLB001 Color Bar.mp4')
        file3 = ffmpy.MediaFile.parse_file(filename3)
        self.assertFalse(file1 == file3)

        # As he is very curious, he then wants to see the difference between the files
        self.assertNotEqual(ffmpy.MediaFile.parse_file(filename1).difference(ffmpy.MediaFile.parse_file(filename3)), {})

        # After all these comparisons, he decided to take a look at the streams of each file.
        print(file1.get_video_streams())
        print(file2.get_video_streams())
        print(file3.get_video_streams())

