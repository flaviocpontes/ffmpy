#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ffmpymedia import __author__, __version__, __copyright__, __package__

import unittest
from unittest.mock import patch

import ffmpymedia

class TestPackageInitializing(unittest.TestCase):

    def test_which_inexistent(self):
        self.assertIsNone(ffmpymedia.which('tttt'))

    def test_which_somewhere_else(self):
        self.assertIsNotNone(ffmpymedia.which('/mnt/ffprobe'))
