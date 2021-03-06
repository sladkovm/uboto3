import boto3
import os
import json


class UBoto3():
    """S3 Interface that hides away settings details
    by reading them from the environment variables"""

    region_name = os.getenv('DO_SPACES_REGION')
    endpoint_url = 'https://{}.digitaloceanspaces.com'.format(region_name)
    aws_access_key_id = os.getenv('DO_SPACES_KEY')
    aws_secret_access_key = os.getenv('DO_SPACES_SECRET')
    bucket = os.getenv('DO_BUCKET')

    def __init__(self):

        self.client = boto3.client('s3',
                                   region_name=self.region_name,
                                   endpoint_url=self.endpoint_url,
                                   aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key)

    def head_object(self, Key, **kwargs):
        """list metadata of the object"""

        if kwargs.get("Prefix"):
            Key = "{}/{}".format(kwargs.get("Prefix"), Key)
            kwargs.pop("Prefix")

        try:
            r = self.client.head_object(Bucket=self.bucket, Key=Key, **kwargs)
        except self.client.exceptions.ClientError:
            r = None

        return r

    def list_objects(self, **kwargs):
        """List of object found in the bucket

        Parameters
        ----------
        Prefix: str
            Prefix indicating the subfolder (slash is omited)
        """
        r = self.client.list_objects(Bucket=self.bucket, **kwargs)
        return r.get('Contents')

    def list_keys(self, **kwargs):
        """Return list of keys of the found objects"""
        rv = [k['Key'] for k in self.list_objects(**kwargs)]
        return rv

    def get_object(self, Key, **kwargs):
        """Get a single object from the bucket using Key"""

        r = self.client.get_object(Bucket=self.bucket, Key=Key, **kwargs)

        return json.loads(r['Body'].read().decode('utf-8'))

    def upload_json(self, f_name, **kwargs):
        """Upload json file to the S3 bucket"""
        _prefix = kwargs.get('Prefix', None)
        _key = kwargs.get('Key', os.path.basename(f_name))
        if _prefix:
            _key = _prefix + '/' + _key
        with open(f_name, 'rb') as f:
            self.client.upload_fileobj(f, Bucket=self.bucket, Key=_key)

        return _key
