#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ffmpy import __author__, __version__, __copyright__, __package__

import unittest
from unittest.mock import patch

import ffmpy

class TestPackageInitializing(unittest.TestCase):

    def test_which_inexistent(self):
        self.assertIsNone(ffmpy.which('tttt'))

    def test_which_somewhere_else(self):
        self.assertIsNotNone(ffmpy.which('/mnt/ffprobe'))
