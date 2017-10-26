import click
import pprint
import subprocess

from pymongo import MongoClient

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
    command = ' '.join(['docker', 'run', '--privileged', '-i', '-t', image_location, '/bin/bash'])
    process = subprocess.Popen(command, shell=True)
    stdout = process.communicate()[0]
    result = stdout.decode('utf-8').strip() if stdout else None
    returncode = process.returncode
    return result, returncode


def _get_artifact_image_tag(artifact_id):
    client = MongoClient('mongodb://127.0.0.1:3001/meteor')
    db = client.meteor
    coll = db['artifacts']
    cursor = coll.find({'aid': artifact_id})
    pprint.pprint(cursor)
    return cursor
