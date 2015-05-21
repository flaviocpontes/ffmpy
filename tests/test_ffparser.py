#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __init__ import __author__, __version__, __copyright__, __package__

import os.path
import datetime
import unittest
from ffmpy.ffparser import *
import stateful_parser

test_file_path = 'test_files'

class TestParseProbeOutput(unittest.TestCase):

    def setUp(self):
        stateful_parser.Input.reset_count()
        stateful_parser.InputStreamSubContext.reset_count()
        stateful_parser.Output.reset_count()

    def tearDown(self):
        stateful_parser.Input.reset_count()
        stateful_parser.InputStreamSubContext.reset_count()
        stateful_parser.Output.reset_count()

    def test_empty(self):
        self.assertIsNone(FFProbeParser.parse_probe_output(''))

    def test_invalid_input(self):
        self.assertRaises(AttributeError, FFProbeParser.parse_probe_output, 'INVALID INPUT!!!!!')

    def test_ffprobe_outfile1(self):
        file = os.path.join(test_file_path, '1 - The Gathering.avi.ffprobe')
        self.assertEqual(FFProbeParser.parse_probe_output(open(file, 'r')),
                         {'filename': '1 - The Gathering.avi',
                          'start_time': '0.000000',
                          'format_name': 'avi',
                          'bit_rate': '1018000',
                          'duration': '5682.02',
                          'format_long_name': 'AVI (Audio Video Interleaved)',
                          'tags': {'encoder': 'VirtualDubMod 1.5.4.1 (build 2178/release)',
                                   'IAS1': 'English'},
                          'streams': [{'index': '0',
                                       'type': 'video',
                                       'codec': 'mpeg4',
                                       'codec_tag_string': 'DX50',
                                       'codec_tag': '0x30355844',
                                       'pixel_format': 'yuv420p',
                                       'width': '640',
                                       'height': '496',
                                       'sample_aspect_ratio': '1:1',
                                       'display_aspect_ratio': '40:31',
                                       'bitrate': '883',
                                       'average_frame_rate': '23.98',
                                       'container_time_base': '23.98',
                                       'reported_frame_rate': '23.98',
                                       'codec_time_base': '30k',
                                       'disposition': {'lyrics': 0, 'comment': 0, 'attached_pic': 0, 'original': 0,
                                                       'karaoke': 0, 'forced': 0, 'clean_effects': 0,
                                                       'hearing_impaired': 0, 'default': 0, 'visual_impaired': 0,
                                                       'dub': 0},
                                       },
                                      {'index': '1',
                                       'type': 'audio',
                                       'codec': 'mp3',
                                       'codec_tag_string': 'U[0][0][0]',
                                       'codec_tag': '0x0055',
                                       'sample_rate': '48000',
                                       'channel_layout': 'stereo',
                                       'channels': 2,
                                       'sample_fmt': 's16p',
                                       'bitrate': '128000',
                                       'disposition': {'lyrics': 0, 'comment': 0, 'attached_pic': 0, 'original': 0,
                                                       'karaoke': 0, 'forced': 0, 'clean_effects': 0,
                                                       'hearing_impaired': 0, 'default': 0, 'visual_impaired': 0,
                                                       'dub': 0}}],
                          })

    def test_ffprobe_outfile2(self):
        file = os.path.join(test_file_path, '[gg-BSS]_Gundam_00_S2_-_01_[44C8CD36].mkv.ffprobe')
        self.assertEqual(FFProbeParser.parse_probe_output(open(file, 'r')),
                         {'filename': '1 - The Gathering.avi',
                          'start_time': '0.000000',
                          'format_name': 'avi',
                          'bit_rate': '1018000',
                          'duration': '5682.02',
                          'format_long_name': 'AVI (Audio Video Interleaved)',
                          'tags': {'encoder': 'VirtualDubMod 1.5.4.1 (build 2178/release)',
                                   'IAS1': 'English'},
                          'streams': [{'index': '0',
                                       'type': 'video',
                                       'codec': 'mpeg4',
                                       'codec_tag_string': 'DX50',
                                       'codec_tag': '0x30355844',
                                       'pixel_format': 'yuv420p',
                                       'width': '640',
                                       'height': '496',
                                       'sample_aspect_ratio': '1:1',
                                       'display_aspect_ratio': '40:31',
                                       'bitrate': '883',
                                       'average_frame_rate': '23.98',
                                       'container_time_base': '23.98',
                                       'reported_frame_rate': '23.98',
                                       'codec_time_base': '30k',
                                       'disposition': {'lyrics': 0, 'comment': 0, 'attached_pic': 0, 'original': 0,
                                                       'karaoke': 0, 'forced': 0, 'clean_effects': 0,
                                                       'hearing_impaired': 0, 'default': 0, 'visual_impaired': 0,
                                                       'dub': 0},
                                       },
                                      {'index': '1',
                                       'type': 'audio',
                                       'codec': 'mp3',
                                       'codec_tag_string': 'U[0][0][0]',
                                       'codec_tag': '0x0055',
                                       'sample_rate': '48000',
                                       'channel_layout': 'stereo',
                                       'channels': 2,
                                       'sample_fmt': 's16p',
                                       'bitrate': '128000',
                                       'disposition': {'lyrics': 0, 'comment': 0, 'attached_pic': 0, 'original': 0,
                                                       'karaoke': 0, 'forced': 0, 'clean_effects': 0,
                                                       'hearing_impaired': 0, 'default': 0, 'visual_impaired': 0,
                                                       'dub': 0}}],
                          })
