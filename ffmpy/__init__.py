#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path

__author__ = 'Flávio Cardoso Pontes <flaviopontes@acerp.org.br>'
__copyright__ = 'Copyright © 2012, 2014 Associação de Comunicação Educativa Roquette Pinto - ACERP'
__version_info__ = (0, 2, 2, 0)
__version__ = '.'.join(map(str, __version_info__))
__package__ = 'ffmpy'


def which(program):
    """Finds the executable binary of a program

    Args:
        program (str): the programs supposed executable filename

    Returns:
        str: The programs real executable filename or None if not found
    """

    def is_exec(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if is_exec(program):
        return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, fname)
            if is_exec(exe_file):
                return exe_file
    return None


ffprobe_path = which('/opt/ffmpeg/bin/ffprobe')
if not ffprobe_path:
    FileNotFoundError('Não foi possível possível encontrar o executável do ffprobe')

ffmpeg_path = which('/opt/ffmpeg/bin/ffmpeg')
if not ffmpeg_path:
    FileNotFoundError('Não foi possível possível encontrar o executável do ffmpeg')

ffserver_path = which('/opt/ffmpeg/bin/ffserver')
if not ffserver_path:
    FileNotFoundError('Não foi possível possível encontrar o executável do ffserver')

from ffmpy.media import MediaAnalyser, MediaStream, MediaStreamTemplate, MediaFile, MediaFileTemplate
from ffmpy.probe import MediaProbe

__all__ = ['MediaAnalyser', 'MediaStream', 'MediaStreamTemplate', 'MediaFile', 'MediaFileTemplate', 'MediaProbe']