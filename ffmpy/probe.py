#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import logging
from ffmpy.parser import ProbeContext
from ffmpy import ffprobe_path

class MediaProbe:
    """
    Classe estática
    """

    @staticmethod
    def _probe_media_file(filename, path=ffprobe_path):
        """Chama o ffprobe e retorna o seu resultado como uma string"""
        logging.info('Iniciando probing do arquivo {}'.format(filename))
        comando = [path, filename]
        saida = subprocess.check_output(comando, stderr=subprocess.STDOUT).decode()

        return saida

    @staticmethod
    def get_media_file_input_params(filename, path=ffprobe_path):
        """Encapsula do parser já com a saida do ffprobe como parâmetro"""
        return MediaProbe.get_input_media_params(MediaProbe._probe_media_file(filename, path))

    @staticmethod
    def parse_ffprobe_output(input):
        """
        Passa a saida do ffprobe para o parser
        """
        ctx = ProbeContext(input)
        return ctx.process()

    @staticmethod
    def get_input_media_params(input):
        """
        Retorna os parâmetros do arquivo de entrada do ffprobe, desprezando o resto da saída
        """
        resultado = MediaProbe.parse_ffprobe_output(input)
        return resultado.get('Input 0')