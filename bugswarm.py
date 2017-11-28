import logging
import os
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


def _validate_shared_dir(ctx, param, value):
    if value is None:
        return value

    host_dir, container_dir = value.split(':', 1)

    # Since we do not know the the filesystem of the container, we cannot validate container_dir. We cannot even check
    # if it is an absolute path because that would require that the container is the same platform as the host, which is
    # too strong of an assumption. Instead, we pass validation responsibility to docker; it will complain if necessary.
    #
    # However, we can check that host_dir is an absolute path to an existing directory on the host machine.
    if not host_dir or not os.path.isdir(host_dir) or not container_dir:
        raise click.BadParameter('The volume binding must be a colon-separated pair of absolute paths to a directory '
                                 'on the host and the container, respectively. '
                                 '(e.g. /home/username/bugswarm-sandbox:/home)')
    return host_dir, container_dir


@cli.command()
@click.option('--image-tag', required=True, type=str)
@click.option('--script', type=click.Path(file_okay=True, path_type=str))
@click.option('--shared-dir', callback=_validate_shared_dir, default=None, type=str)
def run(image_tag, script, shared_dir):
    docker.docker_run(image_tag, script, shared_dir)


@cli.command()
@click.option('--image-tag', required=True, type=str)
def show(image_tag):
    log.info('Showing metadata for artifact with image tag', image_tag + '.')
    response = bugswarmapi.find_artifact(image_tag)
    artifact = response.json()
    log.info(pprint.pformat(artifact, indent=2))
