# Two-stage Discourse Parser

This is a fork of the [StageDP RST parser](https://github.com/yizhongw/StageDP) parser.
I keep the orginal README in a [separate file](README_ORIGINAL.md) to avoid
confusion regarding the installation process.


## Installation

```
docker build -t stage-dp .
docker-compose up
```

## Usage

To test if parser works, just run ``docker run --net host stage-dp``.

To run the parser on the file ``input_short.txt`` from this repo,
copy it to your `/tmp` directory, mount that directory into the
Docker container and run it:

```
cp input_short.txt /tmp/
docker run --net host -v /tmp:/tmp -ti stage-dp /tmp/input_short.txt
```

## Running tests

```
docker-compose -f docker-compose-test.yml up --exit-code-from stagedp
```
