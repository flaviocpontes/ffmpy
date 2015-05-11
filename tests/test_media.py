#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __init__ import __author__, __version__, __copyright__, __package__

import unittest

from ffmpy.media import *


class TestMediaStreamCreation(unittest.TestCase):
    """
    Testes de criação dos objetos de fluxo de mídia
    """

    def test_invalid_media_stream(self):
        self.assertIsNone(MediaStream())

    def test_invalid_media_stream2(self):
        self.assertIsNone(MediaStream(**{'type': 'Invalid'}))

    def test_video_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'Video'}), MediaStream)

    def test_video_stream_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'Video'})), "MediaStream(**{'type': 'Video'})")

    def test_video_stream_repr2(self):
        self.assertDictEqual({'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video', 'profile': 'Main',
                              'codec': 'mpeg2video', 'height': '1080', 'metadata': {'encoder': 'FFMPEG'}},
                             MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                            'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080',
                                            'metadata': {'encoder': 'FFMPEG'}}).__dict__)

    def test_video_stream_str(self):
        self.assertEqual(str(MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                            'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'})),
                         "Video Stream: codec: mpeg2video, height: 1080, profile: Main, sample_format: yuv420p, "
                         "type: Video, width: 1920")

    def test_audio_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'Audio'}), MediaStream)

    def test_audio_stream_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'Audio'})), "MediaStream(**{'type': 'Audio'})")

    def test_image_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'Image'}), MediaStream)

    def test_image_stream_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'Image'})), "MediaStream(**{'type': 'Image'})")

    def test_subtitle_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'Subtitle'}), MediaStream)

    def test_subtitle_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'Subtitle'})), "MediaStream(**{'type': 'Subtitle'})")

    def test_data_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'Data'}), MediaStream)

    def test_data_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'Data'})), "MediaStream(**{'type': 'Data'})")

    def test_attachment_stream_creation(self):
        self.assertIsInstance(MediaStream(**{'type': 'Attachment'}), MediaStream)

    def test_attachment_type_repr(self):
        self.assertEqual(repr(MediaStream(**{'type': 'Attachment'})), "MediaStream(**{'type': 'Attachment'})")


class TestMediaStreamTemplateCreation(unittest.TestCase):
    """
    Testes de criação dos objetos template de fluxo de mídia
    """

    def test_invalid_media_stream_template(self):
        self.assertIsNone(MediaStreamTemplate())

    def test_invalid_media_stream_template2(self):
        self.assertIsNone(MediaStream(**{'type': 'Invalid'}))

    def test_video_stream_template_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'Video'}), MediaStreamTemplate)

    def test_video_stream_template_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'Video'})), "MediaStreamTemplate(**{'type': 'Video'})")

    def test_video_stream_template_repr2(self):
        self.assertDictEqual({'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video', 'profile': 'Main',
                              'codec': 'mpeg2video', 'height': '1080'},
                             MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                                    'profile': 'Main', 'codec': 'mpeg2video',
                                                    'height': '1080'}).__dict__)

    def test_audio_stream_template_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'Audio'}), MediaStreamTemplate)

    def test_audio_stream_template_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'Audio'})), "MediaStreamTemplate(**{'type': 'Audio'})")

    def test_video_stream_template_str(self):
        self.assertEqual(str(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                                    'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'})),
                         "Video Stream Template: codec: mpeg2video, height: 1080, profile: Main, sample_format: "
                         "yuv420p, type: Video, width: 1920")


    def test_image_stream_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'Image'}), MediaStreamTemplate)

    def test_image_stream_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'Image'})), "MediaStreamTemplate(**{'type': 'Image'})")

    def test_subtitle_stream_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'Subtitle'}), MediaStreamTemplate)

    def test_subtitle_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'Subtitle'})),
                         "MediaStreamTemplate(**{'type': 'Subtitle'})")

    def test_data_stream_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'Data'}), MediaStreamTemplate)

    def test_data_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'Data'})), "MediaStreamTemplate(**{'type': 'Data'})")

    def test_attachment_stream_creation(self):
        self.assertIsInstance(MediaStreamTemplate(**{'type': 'Attachment'}), MediaStreamTemplate)

    def test_attachment_type_repr(self):
        self.assertEqual(repr(MediaStreamTemplate(**{'type': 'Attachment'})),
                         "MediaStreamTemplate(**{'type': 'Attachment'})")


class TestMediaStreamTemplateAnalysis(unittest.TestCase):
    """
    Testes das funcionalidades de análise dos templates de fluxos de mídia
    """

    def test_empty_template_equal1(self):
        """
        Deve retornar verdadeiro sempre pois o template não faz nenhuma exigência
        """
        self.assertTrue(MediaStreamTemplate(**{'type': 'Video'}) == MediaStream(**{'type': 'Video',
                                            'sample_format': 'yuv420p', 'width': '66718', 'height': '643816hsa',
                                            'blablabla': 'sakjhfashkjf'}))

    def test_empty_template_equal2(self):
        self.assertTrue(MediaStreamTemplate(**{'type': 'Video'}).difference(MediaStream(**{'type': 'Video',
                            'sample_format': 'yuv420p', 'width': '66718', 'height': '643816hsa',
                            'blablabla': 'sakjhfashkjf'})) == {})

    def test_full_template_equal1(self):
        """
        Testa um Template com todas as informações
        """
        self.assertTrue(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                               'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'}).
            difference(MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video', 'profile': 'Main',
                                      'codec': 'mpeg2video', 'height': '1080'})) == {})

    def test_full_template_equal2(self):
        self.assertTrue(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                               'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'}) ==\
            MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video', 'profile': 'Main',
                           'codec': 'mpeg2video', 'height': '1080'}))

    def test_full_template_equal3(self):
        """
        Testa Um media stream sem uma chave que esta no Template
        """
        self.assertFalse(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                               'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'}) ==\
            MediaStream(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                           'codec': 'mpeg2video', 'height': '1080'}))

    def test_stream_difference1(self):
        self.assertFalse(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                               'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'}) ==\
            MediaStream(**{'sample_format': 'yuv420p', 'width': '1280', 'type': 'Video', 'profile': 'Main',
                           'codec': 'mpeg2video', 'height': '720'}))

    def test_stream_difference2(self):
        """
        Testa um MediaFile diferente
        """
        self.assertTrue(MediaStreamTemplate(**{'sample_format': 'yuv420p', 'width': '1920', 'type': 'Video',
                                               'profile': 'Main', 'codec': 'mpeg2video', 'height': '1080'}).
                        difference(MediaStream(**{'sample_format': 'yuv420p', 'width': '1280', 'type': 'Video',
                                                  'profile': 'Main', 'codec': 'mpeg2video', 'height': '720'})))


class TestMediaFileCreation(unittest.TestCase):
    """
    Testes das funcionalidades da classe MediaFile
    """
    def setUp(self):
        self.TEST_FILE = '/home/Compartilhado/Arquivos de testes/Fork/AULA PROFISSOES.mov'

    def test_nonexistente_file(self):
        self.assertIsNone(MediaFile(**{'filename': 'NAOEXISTE'}))

    def test_insufficient_parameters(self):
        file_params = p.FFProbeParser.probe_and_parse_media_file(self.TEST_FILE)
        file_params.__delitem__('duration')
        self.assertIsNone(MediaFile(**file_params))

