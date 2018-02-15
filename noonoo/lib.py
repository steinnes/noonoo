import os

from functools import partial

from boto3.session import Session


class Image(object):
    def __init__(self, metadata):
        self.metadata = metadata
        self.digest = metadata['imageDigest']
        self.pushed_at = metadata['imagePushedAt']
        self.id = {'imageDigest': self.digest}
        self.tags = None
        if 'imageTags' in metadata:
            self.id['imageTag'] = metadata['imageTags'][0]
            self.tags = metadata['imageTags']

    def __repr__(self):
        return "[{}: {}]".format(
            self.pushed_at.isoformat(),
            self.id,
        )


class ECR(object):
    def __init__(self, region=None, access_key_id=None, secret_access_key=None):
        kwargs = {}
        if region is None:
            region = os.environ.get('AWS_REGION')
        if access_key_id is None:
            access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        if secret_access_key is None:
            secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        kwargs['aws_access_key_id'] = access_key_id
        kwargs['aws_secret_access_key'] = secret_access_key
        kwargs['region_name'] = region

        session = Session(**kwargs)
        self.client = session.client('ecr')

    def _list_images(self, repository):
        list_images = partial(self.client.describe_images, maxResults=100)
        while True:
            resp = list_images(repositoryName=repository)
            for image in resp['imageDetails']:
                yield Image(image)
            if 'nextToken' in resp:
                list_images = partial(list_images, nextToken=resp['nextToken'])
            else:
                break

    def get_image(self, repository, tag):
        # XXX: this is dirty, should just filter the tag..
        for image in self._list_images(repository):
            if tag in image.tags:
                return image

    def list_images(self, repository):
        return self._list_images(repository)

    def delete_images(self, repository, images):
        batch_size = 100
        while len(images) > 0:
            self.client.batch_delete_image(
                repositoryName=repository,
                imageIds=[i.id for i in images[:batch_size]]
            )
            images = images[batch_size:]
