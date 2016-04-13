# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

TESTS_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(TESTS_PATH)
TEST_FILE_PATH = os.path.join(PROJECT_ROOT, 'test_files')