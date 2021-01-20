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

# ~ from neuralseg.splitter import DEFAULT_ARGS, load_models, segment_text
from stagedp.parser_wrapper import load_parser, parse_text

REPO_ROOT_PATH = Path(__file__).parent.parent # root directory of the repo
REPO_PACKAGE_PATH = REPO_ROOT_PATH.joinpath('neuralseg')
FIXTURES_PATH = REPO_ROOT_PATH.joinpath('tests/fixtures')

RST_PARSER, CORE_NLP, ANNOTATION_FUNC, BROWN_CLUSTERS = load_parser()


# ~ @pytest.fixture(scope="session", autouse=True)
# ~ def parser_models():
    # ~ print("starting parser / loading models...")
    # ~ # silence warnings
    # ~ logging.getLogger("tensorflow").setLevel(logging.ERROR)

    # ~ rst_parser, core_nlp, annotation_func, brown_clusters = load_parser()
    # ~ return rst_parser, core_nlp, annotation_func, brown_clusters
    # ~ return rst_parser, core_nlp, brown_clusters
    # ~ return load_parser()

    # ~ # We need to mess with the PATH, since the code that unpickles
    # ~ # `word.vocab` expects to be able to `import vocab`
    # ~ # (instead of `import neuralseg.vocab`.
    # ~ sys.path.append(REPO_PACKAGE_PATH.as_posix())
    
    # ~ # provide the fixture values
    # ~ rst_data, model, spacy_nlp = load_models(DEFAULT_ARGS)
    # ~ return rst_data, model, spacy_nlp


def test_rst_short():
    input_text = FIXTURES_PATH.joinpath('input_short.neuraleduseg').read_text()
    expected_output = FIXTURES_PATH.joinpath('output_short.txt').read_text()
    result = parse_text(input_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
    assert result == expected_output

def test_rst_long():
    input_text = FIXTURES_PATH.joinpath('input_long.neuraleduseg').read_text()
    expected_output = FIXTURES_PATH.joinpath('output_long.txt').read_text()
    result = parse_text(input_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
    assert result == expected_output

def test_rst_eurostar():
    input_text = FIXTURES_PATH.joinpath('input_eurostar.neuraleduseg').read_text()
    expected_output = FIXTURES_PATH.joinpath('output_eurostar.txt').read_text()
    result = parse_text(input_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
    assert result == expected_output

# ~ def test_segmentation_short(parser_models):
    # ~ """NeuralEDUSeg produces the expected segmentation output."""
    # ~ rst_data, model, spacy_nlp = parser_models
    
    # ~ input_text = FIXTURES_PATH.joinpath('input_short.txt').read_text()

    # ~ expected_output_json = FIXTURES_PATH.joinpath('output_short.json').read_text()
    # ~ json_result = segment_text(input_text, rst_data, model, spacy_nlp, output_format='json')
    # ~ assert json_result == expected_output_json

    # ~ expected_output_json_debug = FIXTURES_PATH.joinpath('output_short.debug.json').read_text()
    # ~ json_result = segment_text(input_text, rst_data, model, spacy_nlp, output_format='json', debug=True)
    # ~ assert json_result == expected_output_json_debug

    # ~ expected_output_tokenized = FIXTURES_PATH.joinpath('output_short.tokenized').read_text()
    # ~ json_result = segment_text(input_text, rst_data, model, spacy_nlp, output_format='tokenized')
    # ~ assert json_result == expected_output_tokenized

    # ~ expected_output_inline = FIXTURES_PATH.joinpath('output_short.inline').read_text()
    # ~ json_result = segment_text(input_text, rst_data, model, spacy_nlp, output_format='inline')
    # ~ assert json_result == expected_output_inline


# ~ def test_segmentation_long(parser_models):
    # ~ """NeuralEDUSeg produces the expected segmentation output."""
    # ~ rst_data, model, spacy_nlp = parser_models
    
    # ~ input_text = FIXTURES_PATH.joinpath('input_long.txt').read_text()

    # ~ expected_output_json = FIXTURES_PATH.joinpath('output_long.json').read_text()
    # ~ json_result = segment_text(input_text, rst_data, model, spacy_nlp, output_format='json', debug=False)
    # ~ assert json_result == expected_output_json

    # ~ expected_output_json_debug = FIXTURES_PATH.joinpath('output_long.debug.json').read_text()
    # ~ json_result = segment_text(input_text, rst_data, model, spacy_nlp, output_format='json', debug=True)
    # ~ assert json_result == expected_output_json_debug

    # ~ expected_output_tokenized = FIXTURES_PATH.joinpath('output_long.tokenized').read_text()
    # ~ json_result = segment_text(input_text, rst_data, model, spacy_nlp, output_format='tokenized', debug=False)
    # ~ assert json_result == expected_output_tokenized

    # ~ expected_output_inline = FIXTURES_PATH.joinpath('output_long.inline').read_text()
    # ~ json_result = segment_text(input_text, rst_data, model, spacy_nlp, output_format='inline', debug=False)
    # ~ assert json_result == expected_output_inline
