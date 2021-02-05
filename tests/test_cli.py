#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

import argparse
import json
import logging
from pathlib import Path
import sys

import pytest
import requests

from stagedp.parser_wrapper import load_parser, parse_text

REPO_ROOT_PATH = Path(__file__).parent.parent # root directory of the repo
REPO_PACKAGE_PATH = REPO_ROOT_PATH.joinpath('src/stagedp')
FIXTURES_PATH = REPO_ROOT_PATH.joinpath('tests/fixtures')

RST_PARSER, CORE_NLP, ANNOTATION_FUNC, BROWN_CLUSTERS = load_parser()


def test_rst_short():
    input_text = FIXTURES_PATH.joinpath('input_short.neuraleduseg.inline').read_text()
    expected_output = FIXTURES_PATH.joinpath('output_short.txt').read_text()
    result = parse_text(input_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
    assert result == expected_output

def test_rst_long():
    input_text = FIXTURES_PATH.joinpath('input_long.neuraleduseg.inline').read_text()
    expected_output = FIXTURES_PATH.joinpath('output_long.txt').read_text()
    result = parse_text(input_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
    assert result == expected_output

def test_rst_eurostar():
    input_text = FIXTURES_PATH.joinpath('input_eurostar.neuraleduseg.inline').read_text()
    expected_output = FIXTURES_PATH.joinpath('output_eurostar.txt').read_text()
    result = parse_text(input_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
    assert result == expected_output
