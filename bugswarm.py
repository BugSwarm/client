import logging
import pprint

import click

from bugswarmcommon import log
from bugswarmcommon import rest_api as bugswarmapi

from client import docker


@click.group()
@click.version_option(message='BugSwarm Client, version %(version)s')
def cli():
    # Configure logging.
    log.config_logging(getattr(logging, 'INFO', None), None)
    log.info('Note that Docker requires sudo.')


@cli.command()
@click.option('--image-tag', required=True, type=str)
@click.option('--script', type=click.Path(exists=False, file_okay=True, dir_okay=False, path_type=str))
@click.option('--sandbox',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True, path_type=str))
def run(image_tag, script, sandbox):
    docker.docker_run(image_tag, script, sandbox)


@cli.command()
@click.option('--image-tag', required=True, type=str)
def show(image_tag):
    log.info('Showing metadata for artifact with image tag', image_tag + '.')
    response = bugswarmapi.find_artifact(image_tag)
    artifact = response.json()
    log.info(pprint.pformat(artifact, indent=2))
