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

    def test_empty(self):
        self.assertIsNone(FFprobeParser.parse_probe_output(''))

    def test_invalid_input(self):
        self.assertRaises(AttributeError, FFprobeParser.parse_probe_output, 'INVALID INPUT!!!!!')

    def test_ffprobe_outfile1(self):
        file = os.path.join(test_file_path, 'AULA PROFISSOES.ffprobe')
        self.assertEqual(FFprobeParser.parse_probe_output(open(file, 'r')),
                         {'duration': '00:15:46.41',
                          'filename': 'AULA PROFISSOES.mov',
                          'streams': {'0': {'display_aspect_ratio': '16:9', 'color_range': 'tv',
                                            'sample_aspect_ratio': '1:1',
                                            'color_space': 'bt709', 'container_time_base': '2997', 'width': '1920',
                                            'height': '1080', 'pixel_format': 'yuv420p', 'reported_frame_rate': '29.97',
                                            'codec_time_base': '59.94', 'average_frame_rate': '29.97',
                                            'profile': 'Main',
                                            'codec': 'mpeg2video', 'codec_tag': '0x62766478',
                                            'codec_tag_string': 'xdvb',
                                            'bitrate': '33386', 'language': 'eng', 'type': 'Video'},
                                      '1': {'spaciality': '1 channels', 'sampling_rate': '48000', 'bitrate': '768',
                                            'codec': 'pcm_s16le', 'codec_tag': '0x74776F73', 'codec_tag_string': 'sowt',
                                            'sample_format': 's16', 'language': 'eng', 'type': 'Audio'},
                                      '2': {'spaciality': '1 channels', 'sampling_rate': '48000', 'bitrate': '768',
                                            'codec': 'pcm_s16le', 'codec_tag': '0x74776F73', 'codec_tag_string': 'sowt',
                                            'sample_format': 's16', 'language': 'eng', 'type': 'Audio'},
                                      '3': {'codec': 'none', 'codec_tag': '0x64636D74', 'codec_tag_string': 'tmcd',
                                            'language': 'eng', 'type': 'Data'},
                                      },
                          'metadata': {'timecode': '01:00:00;00', 'handler_name': 'Apple Alias Data Handler',
                                       'creation_time': datetime.datetime(2014, 4, 3, 18, 19, 14)},
                          'type': 'mov,mp4,m4a,3gp,3g2,mj2'})

    def test_ffprobe_outfile2(self):
        file = os.path.join(test_file_path, 'AULA PROFISSOES_alta.ffprobe')
        self.assertEqual(FFprobeParser.parse_probe_output(open(file, 'r')),
                         {'filename': 'AULA PROFISSOES_alta.mp4',
                          'duration': '00:15:46.46',
                          'streams': {'0': {'container_time_base': '11988', 'average_frame_rate': '29.97',
                                            'type': 'Video', 'language': 'und', 'pixel_format': 'yuv420p',
                                            'bitrate': '1940', 'height': '720', 'codec': 'h264', 'width': '1280',
                                            'codec_time_base': '59.94', 'codec_tag': '0x31637661',
                                            'sample_aspect_ratio': '1:1', 'profile': 'High',
                                            'codec_tag_string': 'avc1', 'reported_frame_rate': '29.97',
                                            'display_aspect_ratio': '16:9'},
                                      '1': {'codec': 'aac', 'sampling_rate': '48000', 'sample_format': 'fltp',
                                            'codec_tag': '0x6134706D', 'type': 'Audio', 'language': 'eng',
                                            'spaciality': 'mono', 'profile': 'LC', 'codec_tag_string': 'mp4a',
                                            'bitrate': '96'}},
                          'type': 'mov,mp4,m4a,3gp,3g2,mj2',
                          'metadata': {'handler_name': 'SoundHandler'}})

    def test_ffprobe_outfile3(self):
        file = os.path.join(test_file_path, 'AULA PROFISSOES_media.mp4.ffprobe')
        self.assertEqual(FFprobeParser.parse_probe_output(open(file, 'r')),
                         {'type': 'mov,mp4,m4a,3gp,3g2,mj2',
                          'duration': '00:15:46.46',
                          'streams': {'0': {'language': 'und', 'codec': 'h264', 'bitrate': '618',
                                            'pixel_format': 'yuv420p', 'height': '480', 'type': 'Video',
                                            'display_aspect_ratio': '16:9', 'profile': 'Main', 'width': '852',
                                            'codec_time_base': '59.94', 'codec_tag': '0x31637661',
                                            'container_time_base': '11988', 'sample_aspect_ratio': '640:639',
                                            'codec_tag_string': 'avc1', 'reported_frame_rate': '29.97',
                                            'average_frame_rate': '29.97'},
                                      '1': {'language': 'eng', 'codec': 'aac', 'codec_tag': '0x6134706D',
                                            'profile': 'LC', 'bitrate': '72', 'type': 'Audio', 'sample_format': 'fltp',
                                            'spaciality': 'mono', 'codec_tag_string': 'mp4a', 'sampling_rate': '48000'},
                                      },
                          'filename': 'AULA PROFISSOES_media.mp4',
                          'metadata': {'handler_name': 'SoundHandler'}})

    def test_ffprobe_outfile4(self):
        file = os.path.join(test_file_path, 'AULA PROFISSOES_media.webm.ffprobe')
        self.assertEqual(FFprobeParser.parse_probe_output(open(file, 'r')),
                         {'type': 'mov,mp4,m4a,3gp,3g2,mj2',
                          'duration': '00:15:46.46',
                          'streams': {'0': {'language': 'und', 'codec': 'h264', 'bitrate': '618',
                                            'pixel_format': 'yuv420p', 'height': '480', 'type': 'Video',
                                            'display_aspect_ratio': '16:9', 'profile': 'Main', 'width': '852',
                                            'codec_time_base': '59.94', 'codec_tag': '0x31637661',
                                            'container_time_base': '11988', 'sample_aspect_ratio': '640:639',
                                            'codec_tag_string': 'avc1', 'reported_frame_rate': '29.97',
                                            'average_frame_rate': '29.97'},
                                      '1': {'language': 'eng', 'codec': 'aac', 'codec_tag': '0x6134706D',
                                            'profile': 'LC', 'bitrate': '72', 'type': 'Audio', 'sample_format': 'fltp',
                                            'spaciality': 'mono', 'codec_tag_string': 'mp4a', 'sampling_rate': '48000'},
                                      },
                          'filename': 'AULA PROFISSOES_media.mp4',
                          'metadata': {'handler_name': 'SoundHandler'}})