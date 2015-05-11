#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Flávio Cardoso Pontes <flaviopontes@acerp.org.br>'
__copyright__ = 'Copyright © 2012, 2014 Associação de Comunicação Educativa Roquette Pinto - ACERP'
__version_info__ = (0, 2, 0, 'dev')
__version__ = '.'.join(map(str, __version_info__))
__package__ = 'ffmpy'

from ffmpy.media import MediaAnalyser, MediaStream, MediaStreamTemplate, MediaFile, MediaFileTemplate
from ffmpy.ffparser import FFProbeParser

__all__ = ['MediaAnalyser', 'MediaStream', 'MediaStreamTemplate', 'MediaFile', 'MediaFileTemplate', 'FFProbeParser']