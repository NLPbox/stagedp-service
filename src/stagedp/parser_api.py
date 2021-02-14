import os
import logging
import sys

from falcon import HTTP_200
import hug
import requests

from stagedp.parser_wrapper import load_parser, parse_text

"""REST API for the StageDP RST parser (calling the REST API of the
NeuralEDUSeg discourse segmenter in order to create an end-to-end system).

Examples:

    hug -f parser_api.py # run the StageDP server

    curl -X POST -F "input=@/tmp/input.txt" http://localhost:8000/parse
"""

OUTPUT_FILEPATH = '/tmp/output.txt'
RST_PARSER, CORE_NLP, ANNOTATION_FUNC, BROWN_CLUSTERS = load_parser()

# NEURALSEG_ENDPOINT env is defined in docker-compose, but we provide a fallback as well.
NEURALSEG_ENDPOINT = os.environ.get('NEURALSEG_ENDPOINT', 'http://localhost:9001')


@hug.response_middleware()
def process_data(request, response, resource):
    """This is a middleware function that gets called for every request a hug API processes.
    It will allow Javascript clients on other hosts / ports to access the API (CORS request).
    """
    response.set_header('Access-Control-Allow-Origin', '*')

@hug.post('/parse', output=hug.output_format.file)
def call_parser(body):
    if 'input' in body:
        input_file_content = body['input']
        input_text = input_file_content.decode('utf-8')

        # segment input_text with NeuralEDUSeg REST API
        res = requests.post('{}/parse'.format(NEURALSEG_ENDPOINT),
                            files={'input': input_text})
        segmented_text = res.content.decode('utf-8')

        output_text = parse_text(segmented_text, rst_parser=RST_PARSER, annotate_func=ANNOTATION_FUNC, brown_clusters=BROWN_CLUSTERS)
        with open(OUTPUT_FILEPATH, 'w') as output_file:
            output_file.write(output_text)

        return OUTPUT_FILEPATH
    else:
        return {'body': body}

@hug.get('/status')
def get_status():
    return HTTP_200
