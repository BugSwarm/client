import logging
import pprint
import subprocess

import click

from client import bugswarm_api_wrapper as bugswarmapi
from client import log

DOCKER_HUB_ARTIFACT_USER = 'yclliu'
DOCKER_HUB_ARTIFACT_REPO = 'artifacts'


@click.group()
def cli():
    # Configure logging.
    log.config_logging(getattr(logging, 'INFO', None), None)


@cli.command()
@click.option('--image-tag', required=True, type=str)
def run(image_tag):
    log.info('Downloading and entering image with tag', image_tag + '.')
    _docker_run(image_tag)


@cli.command()
@click.option('--image-tag', required=True, type=str)
def show(image_tag):
    log.info('Showing metadata for artifact with image tag', image_tag + '.')
    response = bugswarmapi.find_artifact(image_tag)
    artifact = response.json()
    log.info(pprint.pformat(artifact, indent=2))


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
