FROM python:3.5

RUN apt update
RUN apt install -y python-pip


ADD requirements.txt /opt/stage-dp/

WORKDIR /opt/stage-dp
RUN pip install -r requirements.txt

RUN pip install pudb ipython # TODO: remove
RUN pip install pytest # TODO: remove

COPY data /opt/stage-dp/data
COPY src /opt/stage-dp/src
COPY tests /opt/stage-dp/tests
COPY setup.py README.md /opt/stage-dp/

RUN cp -r data /usr/local/lib/python3.5/site-packages/

RUN python setup.py install
 

WORKDIR /opt/stage-dp/src/stagedp

ENTRYPOINT ["./parser_wrapper.py"]
CMD ["../../tests/fixtures/input_long.txt"]

