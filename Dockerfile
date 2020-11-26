FROM python:3.5

RUN apt update
RUN apt install -y python-pip


ADD requirements.txt /opt/stage-dp/

WORKDIR /opt/stage-dp
RUN pip install -r requirements.txt

COPY . /opt/stage-dp/

WORKDIR /opt/stage-dp/src
ENTRYPOINT ["./parser_wrapper.py"]
CMD ["../input_long.txt"]

