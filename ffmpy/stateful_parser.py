#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import re
import datetime


def decodedatetime(datestring):
    """
    Faz a decodificação das representações de datas da saída do ffmpeg para o objeto nativo datetime.
    """
    if re.match('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', datestring):
        return datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    elif re.match('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}', datestring):
        return datetime.datetime.strptime(datestring, '%b %d %Y %H:%M:%S')
    else:
        raise ValueError('date string "{}" does not match any supported date format.'.format(datestring))


def reset_class_counters():
    Input.reset_count()
    InputStreamSubContext.reset_count()
    Output.reset_count()


#############################
# Abstract Class Definition #
#############################
class Context:
    """
    Classe abstrata que define a assinatura do contexto.
    """
    def __init__(self, parse_string):
        if isinstance(parse_string, io.TextIOBase):
            self.parse_string = parse_string
        elif isinstance(parse_string, str):
            self.parse_string = io.StringIO(parse_string)
        else:
            raise ValueError('parse_string must be a str or a io.TextIOBase child.')

        self.result = {}
        self.subcontext = None
        self.current_line = None

    def next_line(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError


class Parser:
    """
    Classe abstrata ancestral dos Parsers
    """

    def __init__(self, context):
        self.context = context
        self.root = None
        self.state = None

    def process(self):
        raise NotImplementedError


class State:
    """
    Classe abstrata que define a assinatura dos estados
    """
    def process(self, parser):
        raise NotImplementedError


class SubContext:
    """
    Classe abstrata que define a assinatura dos SubContextos
    """
    count = 0

    @classmethod
    def reset_count(cls):
        cls.count = 0

    def __init__(self):
        self.root = {}
        self.state = None
        self.remaining = None

    def process(self, parser):
        raise NotImplementedError


##############################
# Context Classes Definition #
##############################
class ProbeContext(Context):
    """
    Objeto de contexto utilizado para a análise de mídia através da interpretação da saída do ffprobe.
    Contém o resultado do processamento e armazena o estado da máquina.
    """
    def __init__(self, parse_string):
        super().__init__(parse_string)
        self.subcontext = Header(self)

    def next_line(self):
        self.current_line = self.parse_string.readline()
        return self.current_line

    def process(self):
        while self.next_line():
            self.subcontext.process()
        return self.result


#################################
# SubContext Classes Definition #
#################################
class InputStreamSubContext(SubContext):
    """
    Faz a interpretação da linha de descrição dos Fluxos.
    """
    def __init__(self):
        super().__init__()
        self.state = StreamIndex()

    def process(self, parser):
        if parser.context.current_line.startswith('    Stream '):
            self.remaining = parser.context.current_line
            while self.remaining:
                self.state.process(self)
            if not parser.root.get('streams'):
                parser.root['streams'] = {}
            parser.root['streams']['{}'.format(InputStreamSubContext.count)] = self.root
            InputStreamSubContext.count += 1
        elif parser.context.current_line.startswith('    Metadata:'):
            parser.state = StreamMetadata()
            parser.state.process(parser)


#############################
# Parser Classes Definition #
#############################
class Header(Parser):
    """
    Parser para o bloco de cabeçalho do ffprobe.
    """

    def __init__(self, context):
        super().__init__(context)
        self.root = context.result['header'] = {}

        self.state = Version()

    def process(self):
        self.state.process(self)


class Input(Parser):
    """
    Parser para o bloco de arquivo de entrada do ffprobe/ffmpeg.
    """
    count = 0

    @classmethod
    def reset_count(cls):
        cls.count = 0

    def __init__(self, context):
        super().__init__(context)
        self.root = context.result['Input {}'.format(Input.count)] = {}
        Input.count += 1

        self.state = InputLine()

    def process(self):
        self.state.process(self)


class CodecMessages(Parser):

    def __init__(self, context):
        super().__init__(context)
        self.root = {}

        self.state = CodecLine()

    def process(self):
        self.state.process(self)


class Output(Parser):
    """
    Parser para o bloco de arquivo de entrada do ffprobe/ffmpeg.
    """
    count = 0

    @classmethod
    def reset_count(cls):
        cls.count = 0

    def __init__(self, context):
        super().__init__(context)
        self.root = context.result['Input {}'.format(Input.count)] = {}
        Input.count += 1

        self.state = InputLine()

    def process(self):
        self.state.process(self)


########################
# Parser State Classes #
########################
class Version(State):
    """
    Utilitário e versão
    """
    def process(self, parser):
        values = re.match('(ffmpeg|ffprobe) version (.*) Copyright.*\n', parser.context.current_line)
        parser.root.update(dict(zip(['util', 'version'], values.groups())))
        parser.state = Build()


class Build(State):
    """
    Data e compilador usado na compilação do FFMPEG.
    """
    def process(self, parser):
        if re.match('^  built on (.*) with (.*)', parser.context.current_line):
            values = re.match('^  built on (.*) with (.*)', parser.context.current_line)
            parser.root.update(dict(zip(['build_date'], [decodedatetime(values.groups()[0])])))
        parser.state = Configuration()


class Configuration(State):
    """
    Lerá a linha de configuração.
    """
    def process(self, parser):
        parser.state = LibVersions()


class LibVersions(State):
    """
    Estados que buscam as versões das bibliotecas.
    """
    def process(self, parser):
        if re.match('^  (\S*)\s*(\S*)\s*(\S*) /', parser.context.current_line):
            values = re.match('^  (\S*)\s*(\S*)\s*(\S*) /', parser.context.current_line)
            parser.root.update(dict(zip([values.groups()[0]], [values.groups()[1]+values.groups()[2]])))
        elif re.match('^Guessed', parser.context.current_line):
            parser.context.subcontext = Input(parser.context)
        else:
            parser.context.subcontext = Input(parser.context)
            parser.context.subcontext.process()


class InputLine(State):
    """
    Tipo e nome do arquivo.
    """
    def process(self, parser):
        values = re.match('Input #\d*,\s(.*),\sfrom\s\'(.*)\':', parser.context.current_line)
        parser.root.update(dict(zip(['type', 'filename'], list(values.groups()))))
        InputStreamSubContext.reset_count()
        parser.state = InputMetadata()


class InputMetadata(State):
    """
    Metadados do bloco de entrada.
    """
    def __init__(self):
        self.root = {}

    def process(self, parser):
        if re.match('^  Duration:', parser.context.current_line):
            parser.state = InputDuration()
            parser.state.process(parser)
        elif re.match('^  Metadata:', parser.context.current_line):
            self.root = parser.root['metadata'] = {}
        elif re.match('^    \S*\s*: \S*', parser.context.current_line):
            values = re.match('^    (\S*)\s*: (.*?)\s*$', parser.context.current_line).groups()
            if values[0] == 'creation_time':
                self.root.update({values[0]: decodedatetime(values[1])})
            else:
                self.root.update({values[0]: values[1]})


class InputDuration(State):
    """
    Faz a interpretação das linhas de descrição dos Fluxos
    """
    def process(self, parser):
        if re.match('^  Duration: ([0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2})', parser.context.current_line):
            values = re.match('^  Duration: ([0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2})', parser.context.current_line)
            parser.root.update({'duration': values.groups()[0]})
        parser.state = InputStreamSubContext()


class StreamIndex(State):
    """
    Índice do fluxo.
    """
    def process(self, parser):
        values = re.match('^    Stream #\d:(\d)', parser.remaining)
        # parser.root.update({'index': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        if parser.remaining.startswith('('):
            parser.state = StreamLanguage()
        else:
            parser.state = StreamType()


class StreamLanguage(State):
    """
    Linguagem do fluxo.
    """
    def process(self, parser):
        values = re.match('\((\S*)\)', parser.remaining)
        parser.root.update({'language': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        parser.state = StreamType()


class StreamType(State):
    """
    Tipo do fluxo.
    """
    def process(self, parser):
        values = re.match(':\s(\S*):\s', parser.remaining)
        parser.root.update({'type': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        parser.state = StreamCodec()


class StreamCodec(State):
    """
    Codec do fluxo.
    """
    def process(self, parser):
        if re.match('\S*,\s', parser.remaining):
            values = re.match('(\S*),\s', parser.remaining)
        elif re.match('\S*\s', parser.remaining):
            values = re.match('(\S*)\s', parser.remaining)
        parser.root.update({'codec': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        if re.match('\(\S*\)\s\(\S*\s/\s\S*\),', parser.remaining):
            parser.state = StreamCodecProfile()
        elif re.match('\(\S*\s/\s\S*\),', parser.remaining):
            parser.state = StreamCodecSpec()
        elif re.match('\(\S*\s/\s\S*\) \(', parser.remaining):
            parser.state = DataStreamCodecSpec()
        else:
            parser.state = VideoStreamPixelFormat()


class StreamCodecProfile(State):
    """
    Perfil do codec.
    """
    def process(self, parser):
        values = re.match('\((\S*?)\)\s', parser.remaining)
        parser.root.update({'profile': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        parser.state = StreamCodecSpec()


class StreamCodecSpec(State):
    """
    Etiquetas do codec.
    """
    def process(self, parser):
        values = re.match('\((\S*)\s/\s(\S*)\), ', parser.remaining)
        parser.root.update({'codec_tag_string': values.groups()[0],
                            'codec_tag': values.groups()[1]})
        parser.remaining = parser.remaining[values.end():]
        if parser.remaining == '(default)\n':
            parser.remaining = ''
        elif re.match('(\S*?)\(\S*?,\s\S*\),', parser.remaining) or re.match('(\S*?),', parser.remaining):
            parser.state = VideoStreamPixelFormat()
        elif re.match('\S* Hz,', parser.remaining):
            parser.state = AudioStreamSamplingRate()


class DataStreamCodecSpec(State):
    """
    Etiquetas do codec.
    """
    def process(self, parser):
        values = re.match('\((\S*)\s/\s(\S*?)\) ', parser.remaining)
        parser.root.update({'codec_tag_string': values.groups()[0],
                            'codec_tag': values.groups()[1]})
        parser.remaining = parser.remaining[values.end():]
        if parser.remaining == '(default)\n':
            parser.remaining = ''


class AudioStreamSamplingRate(State):
    """
    Taxa de amostragem do audio
    """
    def process(self, parser):
        values = re.match('(\S*) Hz, ', parser.remaining)
        parser.root.update({'sampling_rate': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        parser.state = AudioStreamSpaciality()


class AudioStreamSpaciality(State):
    """
    Taxa de amostragem do audio
    """
    def process(self, parser):
        values = re.match('(.*?), ', parser.remaining)
        parser.root.update({'spaciality': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        parser.state = AudioStreamSampleFormat()


class AudioStreamSampleFormat(State):
    """
    Taxa de amostragem do audio
    """
    def process(self, parser):
        values = re.match('(\S*?), ', parser.remaining)
        parser.root.update({'sample_format': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        parser.state = StreamBitrate()


class VideoStreamPixelFormat(State):
    """
    Tipo de amostragem, intervalo de cor e espaço de cor.
    """
    def process(self, parser):
        if re.match('(\S*?)\(\S*?,\s\S*\),', parser.remaining):
            values = re.match('(\S*?)\(', parser.remaining)
            parser.state = VideoStreamColorSpec()
        elif re.match('\S*,\s', parser.remaining):
            values = re.match('(\S*),\s.', parser.remaining)
            parser.state = VideoStreamResolution()
        parser.root.update({'pixel_format': values.groups()[0]})
        parser.remaining = parser.remaining[values.end()-1:]


class VideoStreamColorSpec(State):
    """
    Intervalo e espaço de cor.
    """
    def process(self, parser):
        values = re.match('\((\S*?),\s(\S*)\), ', parser.remaining)
        parser.root.update({'color_range': values.groups()[0],
                            'color_space': values.groups()[1]})
        parser.remaining = parser.remaining[values.end():]
        parser.state = VideoStreamResolution()


class VideoStreamResolution(State):
    """
    Largura, altura, e razões de aspecto.
    """
    def process(self, parser):
        values = re.match('(\d*)x(\d*)\s\[SAR\s(\d*:\d*)\sDAR\s(\d*:\d*)\], ', parser.remaining)
        parser.root.update({'width': values.groups()[0],
                            'height': values.groups()[1],
                            'sample_aspect_ratio': values.groups()[2],
                            'display_aspect_ratio': values.groups()[3]})
        parser.remaining = parser.remaining[values.end():]
        if re.match('(\d*) tbr, (\d*) tbn, (\d*) tbc', parser.remaining):
            parser.state = PNGStreamTimeBase()
        else:
            parser.state = StreamBitrate()


class StreamBitrate(State):
    """
    Bitrate.
    """
    def process(self, parser):
        values = re.match('(\d*) kb/s', parser.remaining)
        parser.root.update({'bitrate': values.groups()[0]})
        parser.remaining = parser.remaining[values.end():]
        if parser.remaining == ' (default)\n':
            parser.remaining = ''
        elif parser.remaining.startswith(', '):
            parser.remaining = parser.remaining[2:]
            parser.state = StreamTimeBase()


class StreamTimeBase(State):
    """
    fps, tbr, tbn, tbc.
    """
    def process(self, parser):
        values = re.match('(\d*.\d*) fps, (\d*.\d*) tbr, (\d*) tbn, (\d*.\d*) tbc ', parser.remaining)
        parser.root.update({'reported_frame_rate': values.groups()[0],
                            'average_frame_rate': values.groups()[1],
                            'container_time_base': values.groups()[2],
                            'codec_time_base': values.groups()[3]})
        parser.remaining = parser.remaining[values.end():]
        if parser.remaining == '(default)\n':
            parser.remaining = ''


class PNGStreamTimeBase(State):
    """
    tbr, tbn, tbc.
    """
    def process(self, parser):
        values = re.match('(\d*.?\d*) tbr, (\d*.?\d*) tbn, (\d*.?\d*) tbc', parser.remaining)
        parser.root.update({'average_frame_rate': values.groups()[0],
                            'container_time_base': values.groups()[1],
                            'codec_time_base': values.groups()[2]})
        parser.remaining = parser.remaining[values.end():]
        if parser.remaining == '\n':
            parser.remaining = ''


class StreamMetadata(State):
    """
    Metadados do bloco de entrada.
    """
    def __init__(self):
        self.root = {}

    def process(self, parser):
        if re.match('^    Stream ', parser.context.current_line):
            parser.state = InputStreamSubContext()
            parser.state.process(parser)
        elif re.match('^    Metadata:', parser.context.current_line):
            self.root = parser.root['metadata'] = {}
        elif re.match('^      \S*\s*: \S*', parser.context.current_line):
            values = re.match('^      (\S*)\s*: (.*?)\s*$', parser.context.current_line).groups()
            if values[0] == 'creation_time':
                self.root.update({values[0]: decodedatetime(values[1])})
            else:
                self.root.update({values[0]: values[1]})
        elif re.match('^Input', parser.context.current_line):
            parser.context.subcontext = Input(parser.context)
            parser.context.subcontext.process()


class CodecLine(State):
    def process(self, parser):
        if re.match('^Output', parser.context.current_line):
            parser.context.subcontext = Output(parser.context)
            parser.context.subcontext.process()

