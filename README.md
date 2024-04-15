# 🛝 Testcontainers Python Playground

As the name of the repository suggests, it's just a [_playground_](https://dictionary.cambridge.org/dictionary/english/playground).
Will be used to start various test containers supported by [Testcontainers](https://testcontainers.com/) in preparation for usage on
various projects.

## Prerequisites

1. [Docker for desktop](https://docs.docker.com/desktop/)

> [!NOTE]
> You may need to enable "[x] Allow the default Docker socket to be used (requires password)" within your docker for desktop
> for containers to run successfully.

## Usage

Install the necessary python packages in `requirements.txt`:

```shell
pip install requirements.txt
```

And then run any of the tests within the project:

```shell
pytest tests
```

## Running Docker in Docker (DinD)

Tests can also be run within an integration environment (e.g. Jenkins, GitHub, Azure Pipelines etc.)
two things have to be [provided](https://testcontainers-python.readthedocs.io/en/latest/#docker-in-docker-dind):

1. The container has to provide a docker client installation. Either use an image that has docker pre-installed
   (e.g. the official docker images) or install the client from within the Dockerfile specification.

2. The container has to have access to the docker daemon which can be achieved by mounting `/var/run/docker.sock`
   or setting the `DOCKER_HOST` environment variable as part of your docker run command.

| Environment Variable                  | Example                                                                        | Description                          |
|---------------------------------------|--------------------------------------------------------------------------------|--------------------------------------|
| TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE | /var/run/docker.sock                                                           | Path to Docker’s socket used by ryuk |
| TESTCONTAINERS_RYUK_PRIVILEGED        | false                                                                          | Run ryuk as a privileged container   |
| TESTCONTAINERS_RYUK_DISABLED          | false                                                                          | Disable ryuk                         |
| RYUK_CONTAINER_IMAGE                  | [testcontainers/ryuk:0.7.0](https://hub.docker.com/r/testcontainers/ryuk/tags) | Custom image for ryuk                |

Build the docker image using the `Dockerfile` provided and then run the container:

```shell
docker build -t testcontainers-python:example .
```

```shell
docker run -i -e TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock  \
  -e TESTCONTAINERS_RYUK_PRIVILEGED=false \
  -e TESTCONTAINERS_RYUK_DISABLED=false \
  -e RYUK_CONTAINER_IMAGE=testcontainers/ryuk:0.7.0 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name testcontainers-example testcontainers-python:example
```
