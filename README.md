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
To run the parser on the file ``/tmp/input.txt`` on your
local machine, run:

```
docker run --net host -v /tmp:/tmp -ti stage-dp /tmp/input.txt
```
