# Two-stage Discourse Parser

This is a fork of the [StageDP RST parser](https://github.com/yizhongw/StageDP) parser.
I keep the orginal README in a [separate file](README_ORIGINAL.md) to avoid
confusion regarding the installation process.


## Usage

To run the parser on the file ``input_short.neuraleduseg`` from this repo,
copy it to your `/tmp` directory, mount that directory into the
Docker container and run it:

```
$ docker-compose up -d
$ cp tests/fixtures/input_short.txt /tmp/
$ docker run --net host -v /tmp:/tmp -ti stage-dp /tmp/input_short.neuraleduseg
Load action classifier from file: /opt/stage-dp/data/model/model.action.gz with 110976 features and 4 actions.
Load relation classifier from file: /opt/stage-dp/data/model/model.relation.gz with 35376 features at level 0, 17911 features at level 1, 16665 features at level 2, and 18 relations.
Load Brown clusters for creating features ...
(EDU _!Although_they_did_n't_like_it_,_they_accepted_the_offer_.!_)
$ docker-compose down
```

## Running tests

```
docker-compose -f docker-compose-test.yml up --exit-code-from stagedp
```
