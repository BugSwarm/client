import pprint
import subprocess

import click

from client import bugswarm_api_wrapper as bugswarmapi
from client import log

DOCKER_HUB_ARTIFACT_USER = 'yclliu'
DOCKER_HUB_ARTIFACT_REPO = 'artifacts'


@click.group()
def cli():
    pass


# @cli.command()
# @click.option('--artifact-id', required=True)
# def run(artifact_id):
#     click.echo('run called and passed artifact_id = ' + artifact_id)
#     click.echo('Downloading and entering the image with artifact_id ' + artifact_id)
#     # image_tag = _get_artifact_image_tag(artifact_id)
#     image_tag = ''
#     _docker_run(image_tag)


@cli.command()
@click.option('--image-tag', required=True, type=str)
def run(image_tag):
    click.echo('Downloading and entering image with tag ' + image_tag + '.')
    _docker_run(image_tag)


def _docker_run(image_tag):
    image_location = DOCKER_HUB_ARTIFACT_USER + '/' + DOCKER_HUB_ARTIFACT_REPO + ':' + image_tag
    args = ['docker', 'run', '--privileged', '-i', '-t', image_location, '/bin/bash']
    # Try the docker command without sudo.
    command = ' '.join(args)
    process = subprocess.Popen(command, shell=True)
    if process.returncode != 0:
        # The non-sudo command failed, so try again with sudo.
        sudo_command = ' '.join(['sudo'] + args)
        sudo_process = subprocess.Popen(sudo_command, shell=True)
        # sudo_process.wait()
        if sudo_process.wait() != 0:
            # Something went wrong. Return failure.
            return False
    return True


# def _get_artifact_image_tag(artifact_id):
#     client = MongoClient('mongodb://127.0.0.1:3001/meteor')
#     db = client.meteor
#     coll = db['artifacts']
#     cursor = coll.find({'aid': artifact_id})
#     pprint.pprint(cursor)
#     return cursor
