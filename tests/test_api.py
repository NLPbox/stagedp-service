#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

import pytest
import requests

from stagedp.parser_wrapper import parse_text
from test_cli import (
    FIXTURES_PATH, REPO_PACKAGE_PATH, RST_PARSER, CORE_NLP,
    ANNOTATION_FUNC, BROWN_CLUSTERS)


def test_neuraleduseg_api_short_inline():
    """Segment input_short.txt into EDUs using NeuralEDUSeg via REST API."""
    input_text = FIXTURES_PATH.joinpath('input_short.txt').read_text()
    expected_output = FIXTURES_PATH.joinpath('input_short.neuraleduseg.inline').read_text()

    res = requests.post('http://localhost:9001/parse?format=inline',
                        files={'input': input_text})
    assert expected_output == res.content.decode('utf-8')

    # check that 'inline' is also the default format
    res = requests.post('http://localhost:9001/parse',
                        files={'input': input_text})
    assert expected_output == res.content.decode('utf-8')

def test_end2end_api_short():
    """Segment input_short.txt into EDUs using NeuralEDUSeg via REST API,
    then parse into RST tree using StageDP."""
    input_text = FIXTURES_PATH.joinpath('input_short.txt').read_text()
    res = requests.post('http://localhost:9001/parse',
                        files={'input': input_text})
    segmented_text = res.content.decode('utf-8')

    result = parse_text(segmented_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
    expected_output = FIXTURES_PATH.joinpath('output_short.txt').read_text()
    assert result == expected_output

def test_end2end_api_long():
    """Segment input_long.txt into EDUs using NeuralEDUSeg via REST API,
    then parse into RST tree using StageDP."""
    input_text = FIXTURES_PATH.joinpath('input_long.txt').read_text()
    res = requests.post('http://localhost:9001/parse',
                        files={'input': input_text})
    segmented_text = res.content.decode('utf-8')

    result = parse_text(segmented_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
    expected_output = FIXTURES_PATH.joinpath('output_long.txt').read_text()
    assert result == expected_output
