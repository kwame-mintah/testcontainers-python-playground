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


@pytest.fixture(scope="function", autouse=True)
def setup_data():
    """
    A function scoped fixture, which will be executed before running every test.
    Create a new s3 bucket ready to be used.
    """
    client = boto3.client("s3")
    client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": region_name},
    )


def test_playground():
    result = playground.upload_to_bucket(
        contents="Europe? I'm not gonna take over Europe today.",
        bucket="test-bucket",
        key="test",
    )
    assert result["ResponseMetadata"]["HTTPStatusCode"] == 200
