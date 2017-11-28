import logging
import pprint
import subprocess

import click

from bugswarmcommon import log
from bugswarmcommon import rest_api as bugswarmapi
from bugswarmcommon.credentials import DOCKER_HUB_REPO


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
def _docker_run(image_tag, script='/bin/bash'):
    assert image_tag
    assert isinstance(image_tag, str)
    print('script[' + script + ']')
    exit()
    assert script
    assert isinstance(script, str)

    # First, try to pull the image.
    ok = _docker_pull(image_tag)
    if not ok:
        return False

    # Now try to run the image.
    log.info('Note that Docker requires sudo.')
    image_location = _image_location(image_tag)
    args = ['sudo', 'docker', 'run', '--privileged', '-i', '-t', image_location, script]
    process = subprocess.Popen(args)
    _ = process.communicate()
    if process.returncode != 0:
        log.error('Could not run the image', image_location + '.')
        return False
    return process.returncode == 0


def _docker_pull(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)

    image_location = _image_location(image_tag)
    args = ['docker', 'pull', image_location]
    process = subprocess.Popen(args)
    _ = process.communicate()
    if process.returncode != 0:
        log.error('Could not download the image', image_location, 'from Docker Hub.')
    return process.returncode == 0


def _image_location(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)
    return DOCKER_HUB_REPO + ':' + image_tag
