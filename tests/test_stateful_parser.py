#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __init__ import __author__, __version__, __copyright__, __package__

import os.path
import datetime
import unittest
from stateful_parser import *


class TestDecodeDateString(unittest.TestCase):

    def test_empty_string(self):
        self.assertRaises(ValueError, decodedatetime, '')

    def test_invalid_date(self):
        self.assertRaises(ValueError, decodedatetime, 'aAFsakhjhhkashkj')

    def test_valid_timestamp(self):
        self.assertEqual(decodedatetime('2014-01-01 00:00:00'),
                         datetime.datetime(2014, 1, 1, 00, 00, 00))

    def test_valid_timestamp2(self):
        self.assertEqual(decodedatetime('1989-04-16 23:18:59'),
                         datetime.datetime(1989, 4, 16, 23, 18, 59))

    def test_invalid_timestamp(self):
        self.assertRaises(ValueError, decodedatetime, '1950-01-59 26:63:49')

    def test_invalid_timestamp2(self):
        self.assertRaises(ValueError, decodedatetime, '1100-13-18 14:18:49')

    def test_valid_date_string(self):
        self.assertEqual(decodedatetime('May 15 2014 15:42:07'),
                         datetime.datetime(2014, 5, 15, 15, 42, 7))

    def test_valid_date_string2(self):
        self.assertEqual(decodedatetime('Oct 18 1979 09:14:16'),
                         datetime.datetime(1979, 10, 18, 9, 14, 16))

    def test_invalid_date_string(self):
        self.assertRaises(ValueError, decodedatetime, 'Nov 32 2853 15:25:02')

    def test_invalid_date_string2(self):
        self.assertRaises(ValueError, decodedatetime, 'Jul 87 1977 9:10:15')


class TesteProbeContext(unittest.TestCase):
    def test_invalid_object(self):
        self.assertRaises(ValueError, ProbeContext, {})

    def test_empty_string(self):
        parser = ProbeContext('')
        self.assertEqual({'header': {}}, parser.process())

    def test_invalid_input(self):
        self.assertRaises(ValueError, ProbeContext, True)

    def test_br_eleitor(self):
        self.maxDiff = None
        file = open('test_files/ACDM001 ESTRANHO COMILAO.mov.ffprobe', 'r')
        resultado_esperado = {'header': {'libavcodec': '56.26.100',
                                         'libavdevice': '56.4.100',
                                         'libavfilter': '5.11.102',
                                         'libavformat': '56.25.101',
                                         'libavutil': '54.20.100',
                                         'libpostproc': '53.3.100',
                                         'libswresample': '1.1.100',
                                         'libswscale': '3.1.101',
                                         'util': 'ffprobe',
                                         'version': 'n2.6.1'},
                              'Input 0': {'filename': 'ACDM001 ESTRANHO COMILAO.mov',
                                          'duration': '00:26:21.25',
                                          'format_name': 'mov,mp4,m4a,3gp,3g2,mj2',
                                          'format_long_name': 'QuickTime / MOV',
                                          'metadata': {'creation_time': datetime.datetime(2014, 12, 10, 21, 51, 18),
                                                       'handler_name': 'Apple Alias Data Handler',
                                                       'timecode': '01:00:00;00'},
                                          'streams': {'0': {'average_frame_rate': '29.97',
                                                            'bitrate': '34539',
                                                            'codec': 'mpeg2video',
                                                            'codec_tag': '0x62766478',
                                                            'codec_tag_string': 'xdvb',
                                                            'codec_time_base': '59.94',
                                                            'color_range': 'tv',
                                                            'color_space': 'bt709',
                                                            'container_time_base': '2997',
                                                            'display_aspect_ratio': '16:9',
                                                            'height': '1080',
                                                            'language': 'eng',
                                                            'pixel_format': 'yuv420p',
                                                            'profile': 'Main',
                                                            'reported_frame_rate': '29.97',
                                                            'sample_aspect_ratio': '1:1',
                                                            'type': 'Video',
                                                            'width': '1920'},
                                                      '1': {'bitrate': '1536',
                                                            'codec': 'pcm_s16le',
                                                            'codec_tag': '0x74776F73',
                                                            'codec_tag_string': 'sowt',
                                                            'language': 'eng',
                                                            'sample_format': 's16',
                                                            'sampling_rate': '48000',
                                                            'spaciality': '2 channels',
                                                            'type': 'Audio'},
                                                      '2': {'codec': 'none',
                                                            'codec_tag': '0x64636D74',
                                                            'codec_tag_string': 'tmcd',
                                                            'language': 'eng',
                                                            'type': 'Data'}}}}
        self.assertEqual(resultado_esperado, ProbeContext(file).process())

