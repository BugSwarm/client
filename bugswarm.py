import logging
import pprint
import subprocess

import click

from bugswarmcommon import log
from bugswarmcommon import rest_api as bugswarmapi

DOCKER_HUB_ARTIFACT_USER = 'yclliu'
DOCKER_HUB_ARTIFACT_REPO = 'artifacts'


@click.group()
def cli():
    # Configure logging.
    log.config_logging(getattr(logging, 'INFO', None), None)


@cli.command()
@click.option('--image-tag', required=True, type=str)
@click.option('--script', type=click.Path(file_okay=True, path_type=str))
def run(image_tag, script):
    if script:
        log.info('Downloading image with tag', image_tag, 'and executing', script, 'in the container.')
    else:
        log.info('Downloading image with tag', image_tag, 'and entering container.')
    _docker_run(image_tag, script)


@cli.command()
@click.option('--image-tag', required=True, type=str)
def show(image_tag):
    log.info('Showing metadata for artifact with image tag', image_tag + '.')
    response = bugswarmapi.find_artifact(image_tag)
    artifact = response.json()
    log.info(pprint.pformat(artifact, indent=2))


# By default, this function downloads the image, enters the container, and executes '/bin/bash' in the container.
# The executed script can be changed by passing the script argument.
def _docker_run(image_tag, script):
    if script is None:
        script = '/bin/bash'
    log.info('Note that Docker requires sudo.')
    image_location = DOCKER_HUB_ARTIFACT_USER + '/' + DOCKER_HUB_ARTIFACT_REPO + ':' + image_tag
    args = ['sudo', 'docker', 'run', '--privileged', '-i', '-t', image_location, script]
    process = subprocess.Popen(args)
    _ = process.communicate()
    return process.returncode == 0
