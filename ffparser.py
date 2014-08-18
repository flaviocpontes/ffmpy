#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Flávio Pontes <flaviopontes@acerp.org.br>'
__Version__ = '0.1a'

import os
import subprocess
import logging
import re
import io

class FFprobeParser():
    #Expressões regulares utilizadas no processo de parsing
    #Input/Output
    RE_INPUT = 'Input #(\d*),\s(.*),\sfrom\s\'(.*)\':'
    RE_METADATA_INPUT = '^  Metadata:'
    RE_METADATA_STREAM = '^    Metadata:'
    RE_METADATA_STREAM_FIELD = '^      (.*): (.*)'

    #Duração
    RE_DURATION_DETECT = '^  Duration:'
    RE_DURACAO_VIDEO = '^  Duration: (.*), start: (.*), bitrate: (\\d*) kb/s'
    RE_DURACAO_IMAGEM = '^  Duration: (.*), start: (.*), bitrate: N/A'
    RE_DURACAO_AUDIO = '^  Duration: (.*), bitrate: (\\d*) kb/s'

    #Streams
    RE_STREAM_DETECT = '^    Stream '
    RE_PROFILED_VIDEO_STREAM = '^    Stream #\\d:(\\d)\\((.*)\\): Video: (.*) \\((.*)\\) \\((.* / .*)\\),' \
                               ' (.*)\\((.*), (.*)\\), (\\d*)x(\\d*) \\[.*\\],\s(\\d*) kb/s, (.*) fps,' \
                               ' (.*) tbr, (\\d*) tbn, (.*) tbc .*'
    RE_VIDEO_STREAM = '^    Stream #\\d:(\\d)\\((.*)\\): Video: (.*) \\((.* / .*)\\), (.*)\\((.*)\\),' \
                      ' (\\d*)x(\\d*) .*, (\\d*) kb/s, (.*) fps, (.*) tbr, (.*) tbn, (.*) tbc'
    RE_DEFAULT_VIDEO_STREAM = '^    Stream #\\d:(\\d)\\((.*)\\): Video: (.*) \\((.*)\\), (.*), (\\d*)x(\\d*).*,' \
                              ' (.*) fps, (.*) tbr, (.*) tbn, (.*) tbc'
    RE_VP8_VIDEO_STREAM = '^    Stream #\\d:(\\d)\\((.*)\\): Video: (.*), (.*), (\\d*)x(\\d*), .*, (.*) fps, (.*)' \
                          ' tbr, (.*) tbn, (.*) tbc'
    RE_IMAGE_STREAM = '^    Stream #\\d:(\\d): Video: (.*), (.*), (\\d*)x(\\d*).*, (.*) tbr, (.*) tbn,' \
                      ' (.*) tbc'
    RE_OUTPUT_STREAM_H264 = '^    Stream #\\d:(\\d): Video: (.*) \\((.*)\\) \\((.*/.*)\\), (.*), (\\d*)x(\\d*).*,' \
                     ' (\\d*) kb/s, '
    RE_AUDIO_STREAM = '^    Stream #\\d:(\\d)\\((.*)\\): Audio: (.*) \\((.*)\\), (\\d*) Hz, (.*), (.*),' \
                      ' (\\d*) kb/s'
    RE_AUDIO_STREAM_SIMPLE = '^    Stream #\\d:(\\d): Audio: (.*), (\\d*) Hz, (.*), (.*), (\\d*) kb/s'
    RE_AUDIO_STREAM_LANG_SIMPLE = '^    Stream #\\d:(\\d)\\((.*)\\): Audio: (.*), (\\d*) Hz, (.*), (.*), (\\d*) kb/s'
    RE_AUDIO_VORBIS_WEBM = '^    Stream #\\d:(\\d)\\((.*)\\): Audio: (.*), (\\d*) Hz, (.*), (.*) .*'
    RE_DATA_STREAM = '^    Stream #\\d:(\\d)\\((.*)\\): Data: (.*) \\((.*)\\), (\\d*) kb/s'
    RE_DATA_DEFAULT_STREAM = '^    Stream #\\d:(\\d)\\((.*)\\): Data: (.*) \\((.*)\\) \\(.*\\)'
    RE_SUBTITLE_SSA = '^    Stream #\\d:(\\d)\\((.*)\\): Subtitle: (.*) \\(.*\\)'
    RE_ATTACH = '^    Stream #\\d:(\\d): Attachment: (.*)'

    RE_CODEC_WARNING = '^Codec (.*) is not in the full list.'

    ffprobe_path = '/opt/ffmpeg/bin/ffprobe'

    @staticmethod
    def probe_media_file(filename, path=ffprobe_path):
        logging.info('Iniciando probing do arquivo {}'.format(filename))
        comando = [path, filename]
        saida = subprocess.check_output(comando, stderr=subprocess.STDOUT).decode()

        return saida

    @staticmethod
    def probe_and_parse_media_file(filename, path=ffprobe_path):
        return FFprobeParser.parse_probe_output(FFprobeParser.probe_media_file(filename, path))

    @staticmethod
    def parse_probe_output(input):

        state = [None, None, None, None]
        resultado = {}
        root = None
        meta = {}
        for line in io.StringIO(input):
            if re.search(FFprobeParser.RE_INPUT, line) or state[0] == 'input':
                if re.search(FFprobeParser.RE_INPUT, line):  # Neste caso a linha é o descritor do Input
                    fields = ['type', 'filename']
                    values = list(re.search(FFprobeParser.RE_INPUT, line).groups())
                    num = values.pop(0)
                    input = resultado['Input {}'.format(num)] = dict(zip(fields, values))
                    root = input
                    root['metadata'] = {}
                    root['streams'] = {}
                    meta_input = root['metadata']  # Inicializa o registro de metadados
                    state[0] = 'input'
                    state[1], state[2], state[3] = None, None, None
                else:  # Neste caso, estamos populando os parâmetros do input
                    if re.search(FFprobeParser.RE_DURATION_DETECT, line) or state[1] == 'duration':
                        if re.search(FFprobeParser.RE_DURATION_DETECT, line):  # Está na linha da duração
                            state[1] = 'duration'
                            state[2], state[3] = None, None
                            if re.search(FFprobeParser.RE_DURACAO_VIDEO, line):
                                fields = ['duration', 'start time', 'bitrate']
                                values = list(re.search(FFprobeParser.RE_DURACAO_VIDEO, line).groups())
                                root.update(dict(zip(fields, values)))
                            elif re.search(FFprobeParser.RE_DURACAO_IMAGEM, line):
                                fields = ['duration', 'start time']
                                values = list(re.search(FFprobeParser.RE_DURACAO_IMAGEM, line).groups())
                                root.update(dict(zip(fields, values)))
                            elif re.search(FFprobeParser.RE_DURACAO_AUDIO, line):
                                fields = ['duration', 'bitrate']
                                values = list(re.search(FFprobeParser.RE_DURACAO_AUDIO, line).groups())
                                root.update(dict(zip(fields, values)))

                        else:
                            if re.search(FFprobeParser.RE_STREAM_DETECT, line) or state[2] == 'stream':
                                if state[2] != 'stream':
                                    state[2], state[3] = 'stream', None

                                if re.search(FFprobeParser.RE_PROFILED_VIDEO_STREAM, line):
                                    print('Profiled Video Stream')
                                    fields = ['lang', 'codec', 'profile', 'codec_spec', 'sample_format', 'sample_spec', 'colorspace',
                                              'width', 'height', 'bitrate', 'fps', 'framerate', 'tb_container', 'tb_codec']
                                    values = list(re.search(FFprobeParser.RE_PROFILED_VIDEO_STREAM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Video'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_VIDEO_STREAM, line):
                                    print('Video Stream')
                                    fields = ['lang', 'codec', 'codec_spec', 'sample_format', 'sample_spec', 'width', 'height', 'bitrate',
                                              'fps', 'framerate', 'tb_container', 'tb_codec']
                                    values = list(re.search(FFprobeParser.RE_VIDEO_STREAM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Video'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_DEFAULT_VIDEO_STREAM, line):
                                    print('Default Video Stream')
                                    fields = ['lang', 'codec', 'codec_spec', 'sample_format', 'width', 'height', 'fps', 'framerate',
                                              'tb_container', 'tb_codec']
                                    values = list(re.search(FFprobeParser.RE_DEFAULT_VIDEO_STREAM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Video'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_VP8_VIDEO_STREAM, line):
                                    print('VP8 Video Stream')
                                    fields = ['lang', 'codec', 'sample_format', 'width', 'height', 'fps', 'framerate',
                                              'tb_container', 'tb_codec']
                                    values = list(re.search(FFprobeParser.RE_VP8_VIDEO_STREAM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Video'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_IMAGE_STREAM, line):
                                    print('Image Video Stream')
                                    fields = ['codec', 'sample_format', 'width', 'height', 'framerate', 'tb_container', 'tb_codec']
                                    values = list(re.search(FFprobeParser.RE_IMAGE_STREAM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Image'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_OUTPUT_STREAM_H264, line):
                                    print('h.264 Output Video Stream')
                                    fields = ['codec', 'encoder', 'encoding_specs', 'sample_format', 'width', 'height', 'bitrate']
                                    values = list(re.search(FFprobeParser.RE_OUTPUT_STREAM_H264, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Image'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']

                                #Detecção das trilhas de audio
                                elif re.search(FFprobeParser.RE_AUDIO_STREAM, line):
                                    print('Audio Stream')
                                    fields = ['lang', 'codec', 'codec spec', 'sampling_rate', 'spaciality', 'sample_format', 'bitrate']
                                    values = list(re.search(FFprobeParser.RE_AUDIO_STREAM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Audio'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_AUDIO_STREAM_SIMPLE, line):
                                    print('Audio Stream Simple')
                                    fields = ['codec', 'sampling_rate', 'spaciality', 'sample_format', 'bitrate']
                                    values = list(re.search(FFprobeParser.RE_AUDIO_STREAM_SIMPLE, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Audio'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_AUDIO_STREAM_LANG_SIMPLE, line):
                                    print('Audio Stream Lang Simple')
                                    fields = ['lang', 'codec', 'sampling_rate', 'spaciality', 'sample_format', 'bitrate']
                                    values = list(re.search(FFprobeParser.RE_AUDIO_STREAM_LANG_SIMPLE, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Audio'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_AUDIO_VORBIS_WEBM, line):
                                    print('Audio Vorbis WEBM Simple')
                                    fields = ['lang', 'codec', 'sampling_rate', 'spaciality', 'sample_format']
                                    values = list(re.search(FFprobeParser.RE_AUDIO_VORBIS_WEBM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Audio'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']

                                #Detecção das trilhas de legendas
                                elif re.search(FFprobeParser.RE_SUBTITLE_SSA, line):
                                    print('Subtitle Stream')
                                    fields = ['lang', 'codec']
                                    values = list(re.search(FFprobeParser.RE_SUBTITLE_SSA, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Subtitle'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']

                                #Detecção das trilhas de dados
                                elif re.search(FFprobeParser.RE_DATA_STREAM, line):
                                    print('Data Stream')
                                    fields = ['lang', 'codec', 'codec_spec', 'bitrate']
                                    values = list(re.search(FFprobeParser.RE_DATA_STREAM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Data'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']
                                elif re.search(FFprobeParser.RE_DATA_DEFAULT_STREAM, line):
                                    print('Data Default Stream')
                                    fields = ['lang', 'codec', 'codec_spec']
                                    values = list(re.search(FFprobeParser.RE_DATA_DEFAULT_STREAM, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Data'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']

                                #Detecção de anexos
                                elif re.search(FFprobeParser.RE_ATTACH, line):
                                    print('Attachment')
                                    fields = ['codec', ]
                                    values = list(re.search(FFprobeParser.RE_ATTACH, line).groups())
                                    num = values.pop(0)
                                    root.get('streams')['{}'.format(num)] = dict(zip(fields, values))
                                    stream = root.get('streams')['{}'.format(num)]
                                    stream['type'] = 'Attachment'
                                    stream['metadata'] = {}
                                    meta_input = stream['metadata']

                                #Avisos de Codec
                                elif re.search(FFprobeParser.RE_CODEC_WARNING, line):
                                    codec, = re.search(FFprobeParser.RE_CODEC_WARNING, line).groups()
                                    logging.warning('Codec {} not in full list'.format(codec))

                                elif re.search(FFprobeParser.RE_METADATA_STREAM, line) or state[3] == 'metadata':
                                    if re.search(FFprobeParser.RE_METADATA_STREAM, line):  # Neste caso está na linha metadata
                                        state[3] = 'metadata'
                                    elif not re.search(FFprobeParser.RE_METADATA_STREAM_FIELD, line):
                                        state[3] = None
                                    else:  # neste caso é uma linha de metadados
                                        campo = line[:line.index(':')-1].strip()
                                        valor = line[line.index(':')+1:].strip()
                                        meta_input[campo] = valor

                                else:
                                    state = [None, None, None, None]

                    elif re.search(FFprobeParser.RE_METADATA_INPUT, line) or state[1] == 'metadata':
                        if re.search(FFprobeParser.RE_METADATA_INPUT, line):  # Neste caso está na linha metadata
                            state[1] = 'metadata'
                        else:  # neste caso é uma linha de metadados
                            campo = line[:line.index(':')-1].strip()
                            valor = line[line.index(':')+1:].strip()
                            meta_input[campo] = valor

        return resultado.get('Input 0')