import logging
import pprint

import click

from bugswarmcommon import log
from bugswarmcommon import rest_api as bugswarmapi

from client import docker


@click.group()
@click.version_option(message='BugSwarm Client, version %(version)s')
def cli():
    """A command line interface for the BugSwarm dataset."""
    # Configure logging.
    log.config_logging(getattr(logging, 'INFO', None), None)
    log.info('Note that Docker requires sudo.')


@cli.command()
@click.option('--image-tag', required=True,
              type=str,
              help='The artifact image tag.')
@click.option('--use-sandbox/--no-use-sandbox', default=False,
              help='Whether to set up a directory that is shared by the host and container.')
@click.option('--pipe-stdin/--no-pipe-stdin', default=False,
              help='If enabled, the contents of stdin are executed inside the container. '
                   'This option supports heredocs in shells that support them. '
                   'Disabled by default.')
@click.option('--rm/--no-rm', default=True,
              help='If enabled, artifact containers will be cleaned up automatically after use.'
                   'Enabled by default.')
def run(image_tag, use_sandbox, pipe_stdin, rm):
    """Start an artifact container."""
    docker.docker_run(image_tag, use_sandbox, pipe_stdin, rm)


@cli.command()
@click.option('--image-tag', required=True,
              type=str,
              help='The artifact image tag.')
def show(image_tag):
    """Display artifact metadata."""
    log.info('Showing metadata for artifact with image tag', image_tag + '.')
    response = bugswarmapi.find_artifact(image_tag)
    artifact = response.json()
    log.info(pprint.pformat(artifact, indent=2))
