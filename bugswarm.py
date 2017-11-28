import logging
import pprint

import click

from bugswarmcommon import log
from bugswarmcommon import rest_api as bugswarmapi

from client import docker


@click.group()
def cli():
    # Configure logging.
    log.config_logging(getattr(logging, 'INFO', None), None)


def _validate_volume_binding(ctx, param, value):
    try:
        host_dir, container_dir = map(int, value.split(':', 1))
        return host_dir, container_dir
    except ValueError:
        raise click.BadParameter('The volume binding must be in the format <host directory>:<container directory>.')


@cli.command()
@click.option('--image-tag', required=True, type=str)
@click.option('--script', type=click.Path(file_okay=True, path_type=str))
@click.option('--volume-binding', callback=_validate_volume_binding, type=str)
def run(image_tag, script, volume_binding):
    docker.docker_run(image_tag, script, volume_binding)


@cli.command()
@click.option('--image-tag', required=True, type=str)
def show(image_tag):
    log.info('Showing metadata for artifact with image tag', image_tag + '.')
    response = bugswarmapi.find_artifact(image_tag)
    artifact = response.json()
    log.info(pprint.pformat(artifact, indent=2))
