#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Flávio Cardoso Pontes <flaviopontes@acerp.org.br>'
__copyright__ = 'Copyright © 2012, 2014 Associação de Comunicação Educativa Roquette Pinto - ACERP'
__version__ = '0.1.5'
__package__ = 'ffmpy'

from ffparser import FFprobeParser
from media import MediaAnalyser, MediaStream, MediaStreamTemplate, MediaFile, MediaFileTemplate

__all__ = ['FFprobeParser', 'MediaAnalyser', 'MediaStream', 'MediaStreamTemplate', 'MediaFile', 'MediaFileTemplate']