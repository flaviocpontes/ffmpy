#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ffmpymedia import __author__, __version__, __copyright__, __package__
from os.path import join as joinpath

import unittest

from ffmpymedia.media import *
from tests import TEST_FILE_PATH

class TestMediaStream(unittest.TestCase):
    """
    Testes de criação dos objetos de fluxo de mídia
    """

    def test_invalid_media_stream(self):
        self.assertIsNone(MediaStream())

    def test_invalid_media_stream2(self):
        self.assertIsNone(MediaStream(**{'type': 'Invalid'}))

    def test_video_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'video'}), MediaStream)

    def test_video_stream_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'video'})), "MediaStream(**{'type': 'video'})")

    def test_video_stream_repr2(self):
        self.assertDictEqual({'sample_format': 'yuv420p', 'width': '1920', 'type': 'video', 'profile': 'Main',
                              'codec': 'mpeg2video', 'height': '1080', 'metadata': {'encoder': 'FFMPEG'}},
                             MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                            'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080',
                                            'metadata': {'encoder': 'FFMPEG'}}).__dict__)

    def test_video_stream_str(self):
        self.assertEqual(str(MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                            'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'})),
                         "video Stream: codec: mpeg2video, height: 1080, profile: Main, sample_format: yuv420p, "
                         "type: video, width: 1920")

    def test_audio_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'audio'}), MediaStream)

    def test_audio_stream_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'audio'})), "MediaStream(**{'type': 'audio'})")

    def test_image_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'image'}), MediaStream)

    def test_image_stream_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'image'})), "MediaStream(**{'type': 'image'})")

    def test_subtitle_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'subtitle'}), MediaStream)

    def test_subtitle_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'subtitle'})), "MediaStream(**{'type': 'subtitle'})")

    def test_data_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'data'}), MediaStream)

    def test_data_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'data'})), "MediaStream(**{'type': 'data'})")

    def test_attachment_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'attachment'}), MediaStream)

    def test_attachment_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'attachment'})), "MediaStream(**{'type': 'attachment'})")


class TestMediaStreamTemplate(unittest.TestCase):
    """
    Testes de criação dos objetos template de fluxo de mídia
    """

    def test_invalid_media_stream_template(self):
        self.assertIsNone(MediaStreamTemplate())

    def test_invalid_media_stream_template2(self):
        self.assertIsNone(MediaStream(**{'type': 'Invalid'}))

    def test_video_stream_template_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'video'}), MediaStreamTemplate)

    def test_video_stream_template_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'video'})), "MediaStreamTemplate(**{'type': 'video'})")

    def test_video_stream_template_repr2(self):
        self.assertDictEqual({'sample_format': 'yuv420p', 'width': '1920', 'type': 'video', 'profile': 'Main',
                              'codec': 'mpeg2video', 'height': '1080'},
                             MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                                    'profile': 'Main', 'codec': 'mpeg2video',
                                                    'height': '1080'}).__dict__)

    def test_audio_stream_template_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'audio'}), MediaStreamTemplate)

    def test_audio_stream_template_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'audio'})), "MediaStreamTemplate(**{'type': 'audio'})")

    def test_video_stream_template_str(self):
        self.assertEqual(str(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                                    'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'})),
                         "video stream template: codec: mpeg2video, height: 1080, profile: Main, sample_format: "
                         "yuv420p, type: video, width: 1920")

    def test_image_stream_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'image'}), MediaStreamTemplate)

    def test_image_stream_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'image'})), "MediaStreamTemplate(**{'type': 'image'})")

    def test_subtitle_stream_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'subtitle'}), MediaStreamTemplate)

    def test_subtitle_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'subtitle'})),
                         "MediaStreamTemplate(**{'type': 'subtitle'})")

    def test_data_stream_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'data'}), MediaStreamTemplate)

    def test_data_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'data'})), "MediaStreamTemplate(**{'type': 'data'})")

    def test_attachment_stream_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'attachment'}), MediaStreamTemplate)

    def test_attachment_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'attachment'})),
                         "MediaStreamTemplate(**{'type': 'attachment'})")


class TestMediaStreamTemplateAnalysis(unittest.TestCase):
    """
    Testes das funcionalidades de análise dos templates de fluxos de mídia
    """

    def test_empty_template_equal1(self):
        """
        Deve retornar verdadeiro sempre pois o template não faz nenhuma exigência
        """
        self.assertTrue(MediaStreamTemplate(**{'type': 'video'}) == MediaStream(**{'type': 'video',
                                            'sample_format': 'yuv420p', 'width': '66718', 'height': '643816hsa',
                                            'blablabla': 'sakjhfashkjf'}))

    def test_minimal_template_equality(self):
        self.assertTrue(MediaStreamTemplate(**{'type': 'video'}) == MediaStream(**{'type': 'video',
                            'sample_format': 'yuv420p', 'width': '66718', 'height': '643816hsa',
                            'blablabla': 'sakjhfashkjf'}))

    def test_template_equality(self):
        """
        Testa um Template com todas as informações
        """
        self.assertTrue(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                               'profile': 'Main', 'codec': 'mpeg2video',
                                                'height': '1080'}) ==
        MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video', 'profile': 'Main',
                       'codec': 'mpeg2video', 'height': '1080'}))

    def test_full_template_equal2(self):
        self.assertTrue(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                               'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'}) ==\
            MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video', 'profile': 'Main',
                           'codec': 'mpeg2video', 'height': '1080'}))

    def test_full_template_equal3(self):
        """
        Testa Um media stream sem uma chave que esta no Template
        """
        self.assertFalse(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                               'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'}) ==\
            MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                           'codec': 'mpeg2video', 'height': '1080'}))

    def test_stream_difference_with_different_height(self):
        """
        Testa um MediaFile diferente
        """
        self.assertTrue(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                               'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'}).
                        difference(MediaStream(**{'sample_format': 'yuv420p', 'width': '1280', 'type': 'video',
                                                  'profile': 'Main', 'codec': 'mpeg2video', 'height': '720'})))

    def test_stream_difference_with_equal_streams(self):
        """
        Testa a diferença
        """
        self.assertFalse(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                                'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080',
                                                'metadata': {'title': 'Test with Metadata'},
                                                'disposition': {"default": 1, "dub": 0, "original": 0, "comment": 0,
                                                                "lyrics": 0, "karaoke": 0, "forced": 1,
                                                                "hearing_impaired": 0, "visual_impaired": 0,
                                                                "clean_effects": 0, "attached_pic": 0}}).
                         difference(MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                                   'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080',
                                                   'metadata': {'title': 'Test with Metadata'},
                                                   'disposition': {"default": 1, "dub": 0, "original": 0, "comment": 0,
                                                                   "lyrics": 0, "karaoke": 0, "forced": 1,
                                                                   "hearing_impaired": 0, "visual_impaired": 0,
                                                                   "clean_effects": 0, "attached_pic": 0}})))

    def test_stream_difference_with_different_metadata(self):
        """
        Testa um MediaFile diferente
        """
        self.assertEqual(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                                'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080',
                                                'metadata': {'title': 'Test with Metadata'},
                                                'disposition': {"default": 1, "dub": 0, "original": 0, "comment": 0,
                                                                "lyrics": 0, "karaoke": 0, "forced": 1,
                                                                "hearing_impaired": 0, "visual_impaired": 0,
                                                                "clean_effects": 0, "attached_pic": 0}}).
                         difference(MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                                   'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080',
                                                   'metadata': {'title': 'Different Metadata!'},
                                                   'disposition': {"default": 1, "dub": 0, "original": 0, "comment": 0,
                                                                   "lyrics": 0, "karaoke": 0, "forced": 1,
                                                                   "hearing_impaired": 0, "visual_impaired": 0,
                                                                   "clean_effects": 0, "attached_pic": 0}}),
                                    include_metadata=True),
                         {'metadata': {'title': ('Different Metadata!', 'Test with Metadata')}})

    def test_stream_difference_with_different_dispositions(self):
        """
        Testa a diferença
        """
        self.assertEqual(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                                'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080',
                                                'metadata': {'title': 'Test with Metadata'},
                                                'disposition': {"default": 1, "dub": 0, "original": 0, "comment": 0,
                                                                "lyrics": 0, "karaoke": 0, "forced": 1,
                                                                "hearing_impaired": 0, "visual_impaired": 0,
                                                                "clean_effects": 0, "attached_pic": 0}}).
                         difference(MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'video',
                                                   'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080',
                                                   'metadata': {'title': 'Test with Metadata'},
                                                   'disposition': {"default": 0, "dub": 0, "original": 0, "comment": 0,
                                                                   "lyrics": 0, "karaoke": 0, "forced": 1,
                                                                   "hearing_impaired": 0, "visual_impaired": 0,
                                                                   "clean_effects": 0, "attached_pic": 0}})),
                         {'disposition': {'default': (0, 1)}})


class TestMediaFileCreation(unittest.TestCase):
    """
    Testes das funcionalidades da classe MediaFile
    """
    def setUp(self):
        self.TEST_FILE = os.path.join(TEST_FILE_PATH, 'SIN001 Sinuca.mp4')

    def test_nonexistente_file(self):
        self.assertIsNone(MediaFile(**{'filename': 'NAOEXISTE'}))

    def test_insufficient_parameters(self):
        file_params = probe.MediaProbe.get_media_file_input_params(self.TEST_FILE)
        file_params.__delitem__('duration')
        self.assertIsNone(MediaFile(**file_params))