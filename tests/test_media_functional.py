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
        print(file1.__repr__())
        print(file2.__repr__())
        print(file3.__repr__())

    def test_media_analyser(self):
        # Developer1 whises to test the MediaAnalyser API funcionality.
        # With that in mind, he decides to try out all 4 API calls from this helper class.
        filename1 = filename2 = joinpath(TEST_FILE_PATH, 'SIN001 Sinuca.mp4')
        filename3 = joinpath(TEST_FILE_PATH, 'COLB001 Color Bar.mp4')

        template1 = ffmpy.MediaFileTemplate(**{'format_name': 'mov,mp4,m4a,3gp,3g2,mj2', 'duration': '12.0', 'metadata': None, 'start_time': '0.000000', 'streams': [{'type': 'video', 'height': '1080', 'bitrate': '2574', 'metadata': {'handler_name': 'VideoHandler'}, 'codec': 'h264', 'index': '0', 'disposition': {'lyrics': 0, 'default': 1, 'clean_effects': 0, 'karaoke': 0, 'hearing_impaired': 0, 'visual_impaired': 0, 'forced': 0, 'comment': 0, 'dub': 0, 'original': 0, 'attached_pic': 0}, 'codec_tag': '0x31637661', 'codec_tag_string': 'avc1', 'width': '1920', 'sample_aspect_ratio': '1:1', 'pixel_format': 'yuv420p', 'reported_frame_rate': '25', 'display_aspect_ratio': '16:9', 'container_time_base': '12800', 'average_frame_rate': '25', 'codec_time_base': '50', 'language': 'und', 'profile': 'High', 'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10'}], 'filename': '/home/flaviopontes/PycharmProjects/FFMPY/test_files/SIN001 Sinuca.mp4', 'bit_rate': '2577000'})
        template3 = ffmpy.MediaFileTemplate(**{'format_name': 'mov,mp4,m4a,3gp,3g2,mj2', 'duration': '12.0', 'metadata': None, 'start_time': '0.000000', 'streams': [{'type': 'video', 'height': '1080', 'bitrate': '2574', 'metadata': {'handler_name': 'VideoHandler'}, 'codec': 'h264', 'index': '0', 'disposition': {'lyrics': 0, 'default': 1, 'clean_effects': 0, 'karaoke': 0, 'hearing_impaired': 0, 'visual_impaired': 0, 'forced': 0, 'comment': 0, 'dub': 0, 'original': 0, 'attached_pic': 0}, 'codec_tag': '0x31637661', 'codec_tag_string': 'avc1', 'width': '1920', 'sample_aspect_ratio': '1:1', 'pixel_format': 'yuv420p', 'reported_frame_rate': '25', 'display_aspect_ratio': '16:9', 'container_time_base': '12800', 'average_frame_rate': '25', 'codec_time_base': '50', 'language': 'und', 'profile': 'High', 'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10'}], 'filename': '/home/flaviopontes/PycharmProjects/FFMPY/test_files/SIN001 Sinuca.mp4', 'bit_rate': '2577000'})

        self.assertFalse(ffmpy.MediaAnalyser.compare_media_file_with_template(filename1, template1))

