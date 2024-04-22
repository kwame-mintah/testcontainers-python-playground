import io
import json

import boto3


def upload_to_bucket(
    contents: str,
    bucket: str,
    key: str,
) -> dict:
    """
    Create file object with provided contents to s3 bucket.

    :param contents: string message
    :param bucket: The name of the bucket to upload to
    :param key: The name of the key to upload to
    :return: AWS response
    """
    client = boto3.client("s3", region_name="eu-west-2")
    example = {"Johnny": contents}
    file_obj = io.BytesIO()
    file_obj.write(json.dumps(example).encode("utf-8"))
    file_obj.seek(0)
    return client.put_object(Body=file_obj, Bucket=bucket, Key=key)


def send_message_to_queue(
    contents: str,
    queue_name: str,
) -> dict:
    """
    Send message to simple queue service specified.

    :param contents: The contents of the message onto the queue
    :param queue_name: The URL of the Amazon SQS queue to which a message is sent.
    """
    client = boto3.client("sqs", region_name="eu-west-2")
    queue_url = client.get_queue_url(QueueName=queue_name)["QueueUrl"]
    message_body = {
        "message": contents,
    }
    return client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))
