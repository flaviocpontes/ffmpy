#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import logging
from ffmpy.stateful_parser import ProbeContext


class FFProbeParser():

    ffprobe_path = '/opt/ffmpeg/bin/ffprobe'

    @staticmethod
    def probe_media_file(filename, path=ffprobe_path):
        """
        Chama o ffprobe e retorna o seu resultado como uma string
        """
        logging.info('Iniciando probing do arquivo {}'.format(filename))
        comando = [path, filename]
        saida = subprocess.check_output(comando, stderr=subprocess.STDOUT).decode()

        return saida

    @staticmethod
    def probe_and_parse_media_file(filename, path=ffprobe_path):
        """
        Encapsula do parser já com a saida do ffprobe como parâmetro
        """
        return FFProbeParser.parse_probe_output(FFProbeParser.probe_media_file(filename, path))

    @staticmethod
    def parse_output(input):
        """
        Passa a saida do ffprobe para o parser
        """
        ctx = ProbeContext(input)
        return ctx.process()

    @staticmethod
    def parse_probe_output(input):
        """
        Retorna os parâmetros do arquivo de entrada do ffprobe, desprezando o resto da saída
        """
        resultado = FFProbeParser.parse_output(input)
        return resultado.get('Input 0')