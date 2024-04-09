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
