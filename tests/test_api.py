#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

import pexpect
import pytest
import requests

from stagedp.parser_wrapper import parse_text
from stagedp.parser_api import NEURALSEG_ENDPOINT
from test_cli import (
    FIXTURES_PATH, REPO_PACKAGE_PATH, RST_PARSER, CORE_NLP,
    ANNOTATION_FUNC, BROWN_CLUSTERS)


@pytest.fixture(scope="session", autouse=True)
def start_api():
    print("starting  StageDP API...")
    api_path = REPO_PACKAGE_PATH.joinpath('parser_api.py')                                                                                                                                                                                             
    child = pexpect.spawn('hug -f {}'.format(api_path))
    # provide the fixture value (we don't need it, but it marks the
    # point when the 'setup' part of this fixture ends).
    yield child.expect('(?i)Serving on :8000')
    print("stopping StageDP API...")
    child.close()
    
def test_neuraleduseg_api_short_inline():
    """Segment input_short.txt into EDUs using NeuralEDUSeg via REST API."""
    input_text = FIXTURES_PATH.joinpath('input_short.txt').read_text()
    expected_output = FIXTURES_PATH.joinpath('input_short.neuraleduseg.inline').read_text()

    res = requests.post('{}/parse?format=inline'.format(NEURALSEG_ENDPOINT),
                        files={'input': input_text})
    assert expected_output == res.content.decode('utf-8')

    # check that 'inline' is also the default format
    res = requests.post('{}/parse'.format(NEURALSEG_ENDPOINT),
                        files={'input': input_text})
    assert expected_output == res.content.decode('utf-8')

def test_end2end_api_short():
    """Produce an RST tree for plaintext input_short.txt using StageDP's REST API."""
    input_text = FIXTURES_PATH.joinpath('input_short.txt').read_text()
    res = requests.post('{}/parse'.format('http://localhost:8000'),
                        files={'input': input_text})
    parsed_text = res.content.decode('utf-8')
    expected_output = FIXTURES_PATH.joinpath('output_short.txt').read_text()
    assert parsed_text == expected_output

def test_end2end_api_long():
    """Produce an RST tree for plaintext input_long.txt using StageDP's REST API."""
    input_text = FIXTURES_PATH.joinpath('input_long.txt').read_text()
    res = requests.post('{}/parse'.format('http://localhost:8000'),
                        files={'input': input_text})
    parsed_text = res.content.decode('utf-8')
    expected_output = FIXTURES_PATH.joinpath('output_long.txt').read_text()
    assert parsed_text == expected_output

def test_api_status_page():
    """Status page is reachable when REST API is running."""
    res = requests.get('http://localhost:8000/status')
    assert res.ok == True
