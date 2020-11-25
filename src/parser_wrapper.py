#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import os
import gzip
import pickle
import argparse
import sys

from pycorenlp import StanfordCoreNLP

from models.parser import RstParser
from utils.token import Token
from utils.document import Doc
from nltk import Tree


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file', nargs='?', default=sys.stdout)
    return parser.parse_args()


def create_doc_from_edu_file(edu_file, annotate_func):
    with open(edu_file, 'r') as fin:
        doc_tokens = []
        paragraphs = [p.strip() for p in fin.read().split('<P>') if p.strip()]
        previous_edu_num = 0
        for pidx, para in enumerate(paragraphs):
            sentences = [s.strip() for s in para.split('<S>') if s.strip()]
            for sidx, sent in enumerate(sentences):
                edus = [e.strip() + ' ' for e in sent.split('\n') if e.strip()]
                sent_text = ''.join(edus)
                annot_re = annotate_func(sent_text)['sentences'][0]
                sent_tokens = []
                for t in annot_re['tokens']:
                    token = Token()
                    token.tidx, token.word, token.lemma, token.pos = t['index'], t['word'], t['lemma'], t['pos']
                    token.pidx, token.sidx = pidx + 1, sidx
                    edu_text_length = 0
                    for eidx, edu_text in enumerate(edus):
                        edu_text_length += len(edu_text)
                        if edu_text_length > t['characterOffsetEnd']:
                            token.eduidx = previous_edu_num + eidx + 1
                            break
                    sent_tokens.append(token)
                for dep in annot_re['basicDependencies']:
                    dependent_token = sent_tokens[dep['dependent']-1]
                    dependent_token.hidx = dep['governor']
                    dependent_token.dep_label = dep['dep']
                doc_tokens += sent_tokens
                previous_edu_num += len(edus)
    doc = Doc()
    doc.init_from_tokens(doc_tokens)
    return doc


def main():
    args = parse_args()
    parser = RstParser()
    parser.load('../data/model')
    with gzip.open('../data/resources/bc3200.pickle.gz') as fin:
        print('Load Brown clusters for creating features ...')
        brown_clusters = pickle.load(fin)
    core_nlp = StanfordCoreNLP('http://localhost:9000')
    annotate = lambda x: core_nlp.annotate(x, properties={
        'annotators': 'tokenize,ssplit,pos,lemma,parse,depparse',
        'outputFormat': 'json',
        'ssplit.isOneSentence': True
    })

    print('Parsing {}...'.format(args.input_file))
    doc = create_doc_from_edu_file(args.input_file, annotate_func=annotate)
    pred_rst = parser.sr_parse(doc, brown_clusters)
    tree_str = pred_rst.get_parse()
    pprint_tree_str = Tree.fromstring(tree_str).pformat(margin=150) + '\n'
    
    # ~ import pudb; pudb.set_trace()
    if isinstance(args.output_file, str):
        with open(args.output_file, 'w') as fout:
            fout.write(pprint_tree_str)
    else:
        sys.stdout.write(pprint_tree_str)

# args.output_file deafults to:                                                                                            
#   <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>


if __name__ == '__main__':
    main()
