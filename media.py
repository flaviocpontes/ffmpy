#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Flávio Pontes <flaviopontes@acerp.org.br>'
__Version__ = '0.1a'

import os
import ffparser as p
from pprint import pprint

def sorted_list(lista):
    lista = list(lista)
    lista.sort()
    return lista


class MediaAnalyser:

    @staticmethod
    def validate_media_file(media_file, media_template):
        pass


class MediaStream():
    """
    Representa um fluxo de mídia
    """

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self):
        result = self.__dict__.get('type') + ' Stream: {}'.format(self.__dict__)
        return result

    def __repr__(self):
        return str(self.__dict__)


#Classes representando os gabaritos dos fluxos de midia
class MediaStreamTemplate():
    """
    Representa o gabarito de um fluxo de mídia
    """

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self):
        return '{} Stream Template: {}'.format(self.__dict__.get('type'), self.__dict__)

    def __repr__(self):
        return 'StreamTemplate(**'+str(self.__dict__)+')'

    def __eq__(self, other):
        for key in self.__dict__.keys():
            if key != 'metadata':
                if key in other.__dict__.keys():
                    if self.__dict__[key] != other.__dict__[key]:
                        return False
                else:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def difference(self, other):
        """
        Retorna as diferenças entre o template do fluxo e o fluxo. Cada campo é retornado com uma dupla
        {campo: (valor encontrado, valor esperado)}
        :param other: VideoStream
        :return: dict
        """
        difference = {}
        for key in self.__dict__.keys():
            if key != 'metadata':
                if key in other.__dict__.keys():
                    if self.__dict__[key] != other.__dict__[key]:
                        difference[key] = (other.__dict__[key], self.__dict__[key])
        return difference


class MediaFile:
    """
    Representa um arquivo de mídia, composto por vários fluxos de tipos diferentes
    """

    def __new__(cls, *args, **kwargs):
        """
        Verifica se o arquivo é válido e não cria uma instância se não for.
        :param cls:
        :return: MediaFile
        """
        try:
            if len(args) > 0:
                assert os.access(kwargs.get('filename'), os.R_OK)
            return super(MediaFile, cls).__new__(cls)
        except AssertionError as e:
            print('Não foi possível acessar o arquivo {}. Erro {}'.format(args[0], e))
            return None

    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.duration = kwargs.get('duration')
        self.start_time = kwargs.get('start time')
        self.bitrate = kwargs.get('bitrate')
        self.metadata = kwargs.get('metadata')
        self.type = kwargs.get('type')
        self.streams = []
        for stream in sorted_list(kwargs.get('streams').keys()):
            self.streams.append(MediaStream(**kwargs.get('streams').get(stream)))

    def __str__(self):
        return 'Arquivo {}'.format(self.filename)

    def __repr__(self):
        output = {}
        output['filename'] = self.filename
        output['duration'] = self.duration
        output['start time'] = self.start_time
        output['bitrate'] = self.bitrate
        output['metadata'] = self.metadata
        output['streams'] = {}
        for stream in self.streams:
            output['streams'][str(self.streams.index(stream))] = stream.__dict__

        return str('MediaFile(**'+str(output)+')')

    def get_streams_by_type(self, type):
        result = []
        for stream in self.streams:
            if stream.type == type:
                result.append(stream)
        return result

    def get_video_streams(self):
        return self.get_streams_by_type('Video')

    def get_image_streams(self):
        return self.get_streams_by_type('Image')

    def get_audio_streams(self):
        return self.get_streams_by_type('Audio')

    def get_subtitle_streams(self):
        return self.get_streams_by_type('Subtitle')

    def get_data_streams(self):
        return self.get_streams_by_type('Data')

    def get_attachments(self):
        return self.get_streams_by_type('Attachment')


class MediaFileTemplate():
    """
    Representa os parametros de um arquivo de mídia.
    É usado como base de comparação e como base para gerar parâmetros para os comandos de conversão do FFMPEG.
    """

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')

        if kwargs.get('duration'):
            self.duration = kwargs.get('duration')
        if kwargs.get('start time'):
            self.start_time = kwargs.get('start time')
        if kwargs.get('bitrate'):
            self.bitrate = kwargs.get('bitrate')
        if kwargs.get('metadata'):
            self.metadata = kwargs.get('metadata')
        self.streams = []
        for stream in kwargs.get('streams'):
            self.streams.append(MediaStreamTemplate(**stream))

    def __str__(self):
        return '{} File Template: {}'.format(self.type, self.__dict__)

    def __repr__(self):
        return 'MediaFileTemplate(**'+str(self.__dict__)+')'

    def __eq__(self, other):
        for key in self.__dict__.keys():
            if key != 'metadata':
                if key == 'streams':
                    for stream in self.streams:
                        if stream != other.streams[self.streams.index(stream)]:
                            return False
                elif self.__dict__[key] != other.__dict__[key]:
                    return False
        return True

    def difference(self, other):
        """
        Retorna as diferenças entre o template do fluxo e o fluxo. Cada campo é retornado com uma dupla
        {campo: (valor encontrado, valor esperado)}
        :param other: VideoStream
        :return: dict
        """
        difference = {}
        for key in self.__dict__.keys():
            if key != 'metadata':
                if key == 'streams':
                    for stream in self.streams:
                        if stream != other.streams[self.streams.index(stream)]:
                            if not difference.get('streams'):
                                difference['streams'] = []
                            difference['streams'].append(stream.difference(other.streams[self.streams.index(stream)]))
                elif key in other.__dict__.keys():
                    if self.__dict__[key] != other.__dict__[key]:
                        difference[key] = (other.__dict__[key], self.__dict__[key])
        return difference


if __name__ == '__main__':
    #Para fins de teste
    descriptor = p.FFprobeParser.parse_ffprobe('/home/Compartilhado/teste parser/ATIV001 ATLETISMO 1.mov')
    pprint(descriptor.get('Input 0'))
    teste = MediaFile(**descriptor.get('Input 0'))
    print(teste.__dict__)
    teste_template = MediaFileTemplate(**{'type': 'mov,mp4,m4a,3gp,3g2,mj2',
                                          'start_time': '0.000000',
                                          'streams': [{'sample_format': 'yuv420p',
                                                       'width': '1920',
                                                       'type': 'Video',
                                                       'profile': 'Main',
                                                       'codec': 'mpeg2video',
                                                       'height': '1080'},
                                                      {'sampling_rate': '48000',
                                                       'type': 'Audio',
                                                       'codec': 'pcm_s16le'},
                                                      ]})
    print(teste_template == teste)
    print(teste_template.difference(teste))
