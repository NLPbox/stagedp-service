#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import os
import gzip
import pickle
import argparse
import sys
from pathlib import Path

from nltk import Tree
from pycorenlp import StanfordCoreNLP

from stagedp.models.parser import RstParser
from stagedp.utils.token import Token
from stagedp.utils.document import Doc


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file', nargs='?', default=sys.stdout)
    return parser.parse_args()


def create_doc_from_plaintext(input_text, annotate_func):
    doc_tokens = []
    
    sentences = annotate_func(input_text)['sentences']
    for sidx, sent in enumerate(sentences):
        sent_tokens = []
        for t in sent['tokens']:
            token = Token()
            token.tidx, token.word, token.lemma, token.pos = t['index'], t['word'], t['lemma'], t['pos']

            # Our input is not annotated with paragraph/sentence/EDU boundaries,
            # so the paragraph index (pidx) is always 1 and the
            # EDU index (edudix) always equals the sentence number (sidx + 1).
            #
            # Don't ask me why sidx starts counting at 0, but pidx and eduidx start at 1.
            token.pidx = 1
            token.sidx = sidx
            token.eduidx = sidx + 1
            sent_tokens.append(token)
        for dep in sent['basicDependencies']:
            dependent_token = sent_tokens[dep['dependent']-1]
            dependent_token.hidx = dep['governor']
            dependent_token.dep_label = dep['dep']
        doc_tokens += sent_tokens

    doc = Doc()
    doc.init_from_tokens(doc_tokens)
    return doc


def parse_text(text, rst_parser, annotate_func, brown_clusters):
    """Takes an EDU-segmented text (NeuralEDUSeg format) and returns an RST tree
    (StageDP format)."""
    doc = create_doc_from_plaintext(text, annotate_func=annotate_func)

    pred_rst = rst_parser.sr_parse(doc, brown_clusters)
    tree_str = pred_rst.get_parse()
    return Tree.fromstring(tree_str).pformat(margin=150) + '\n'


def load_parser():
    rst_parser = RstParser()

    repo_root_dir = Path(__file__).parent.parent.parent
    model_dir = repo_root_dir.joinpath('data/model').absolute().as_posix()
    rst_parser.load(model_dir)
    
    brown_cluster_path = repo_root_dir.joinpath('data/resources/bc3200.pickle.gz').absolute().as_posix()
    with gzip.open(brown_cluster_path) as fin:
        print('Load Brown clusters for creating features ...')
        brown_clusters = pickle.load(fin)
    core_nlp = StanfordCoreNLP('http://localhost:9000')

    annotation_func = lambda x: core_nlp.annotate(x, properties={
        'annotators': 'tokenize,ssplit,pos,lemma,parse,depparse',
        'outputFormat': 'json'
    })
    return rst_parser, core_nlp, annotation_func, brown_clusters  


def main():
    rst_parser, core_nlp, annotation_func, brown_clusters = load_parser()
    
    args = parse_args()
    with open(args.input_file, 'r') as input_file:
        input_text = input_file.read()
    
    pprint_tree_str = parse_text(input_text, rst_parser=rst_parser, annotate_func=annotation_func, brown_clusters=brown_clusters)

    if isinstance(args.output_file, str):
        with open(args.output_file, 'w') as fout:
            fout.write(pprint_tree_str)
    else:
        sys.stdout.write(pprint_tree_str)


if __name__ == '__main__':
    main()
