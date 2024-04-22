import os

import boto3
import pytest
from testcontainers.localstack import LocalStackContainer

import playground

region_name = "eu-west-2"
localstack = LocalStackContainer(
    image="localstack/localstack:3.2.0", region_name=region_name
)


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    """
    Module scoped fixture to start a LocalStack container using
    Testcontainers so that it will only run once for all the tests in the module.
    :param request:
    """
    localstack.start()
    localstack.with_services("s3,sqs")
    os.environ["AWS_ENDPOINT_URL"] = localstack.get_url()
    os.environ["AWS_DEFAULT_REGION"] = region_name

    def remove_container():
        """
        Stop LocalStack using finalizers.
        """
        localstack.stop()

    request.addfinalizer(remove_container)


@pytest.fixture(scope="module", autouse=True)
def setup_data():
    """
    Function scoped ``module``, destroyed during teardown of the last test in the module (test file).
    Create a new s3 bucket and sqs ready for tests. **Note** the differences between pytest scope(s) because resources,
    may already exist during test runs.

    ``function``: the default scope, the fixture is destroyed at the end of the test. \n
    ``class``: the fixture is destroyed during teardown of the last test in the class. \n
    ``module``: the fixture is destroyed during teardown of the last test in the module. \n
    ``package``: the fixture is destroyed during teardown of the last test in the package. \n
    ``session``: the fixture is destroyed at the end of the test session. \n
    https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#fixture-scopes
    """
    s3_client = boto3.client("s3")
    sqs_client = boto3.client("sqs")
    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": region_name},
    )
    sqs_client.create_queue(QueueName="test-queue")


def test_playground_bucket():
    result = playground.upload_to_bucket(
        contents="Europe? I'm not gonna take over Europe today.",
        bucket="test-bucket",
        key="test",
    )
    assert result["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_playground_sqs():
    result = playground.send_message_to_queue(
        contents="Europe? I'm not gonna take over Europe today.",
        queue_name="test-queue",
    )
    assert result["ResponseMetadata"]["HTTPStatusCode"] == 200
