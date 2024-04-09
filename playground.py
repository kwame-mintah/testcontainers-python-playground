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
    client = boto3.client("s3")
    example = {"Johnny": contents}
    file_obj = io.BytesIO()
    file_obj.write(json.dumps(example).encode("utf-8"))
    file_obj.seek(0)
    return client.put_object(Body=file_obj, Bucket=bucket, Key=key)
