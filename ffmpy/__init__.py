#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Flávio Cardoso Pontes <flaviopontes@acerp.org.br>'
__copyright__ = 'Copyright © 2012, 2014 Associação de Comunicação Educativa Roquette Pinto - ACERP'
__version_info__ = (0, 1, 6, 'a')
__version__ = '.'.join(map(str, __version_info__))
__package__ = 'ffmpy'

from media import MediaAnalyser, MediaStream, MediaStreamTemplate, MediaFile, MediaFileTemplate
from ffmpy.ffparser import FFprobeParser

__all__ = ['FFprobeParser', 'MediaAnalyser', 'MediaStream', 'MediaStreamTemplate', 'MediaFile', 'MediaFileTemplate']