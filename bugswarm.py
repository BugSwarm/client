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


@cli.command()
@click.option('--image-tag', required=True,
              type=str,
              help='The artifact image tag.')
@click.option('--use-sandbox/--no-use-sandbox', default=False,
              help='Whether to set up a directory that is shared by the host and container.')
@click.option('--pipe-stdin/--no-pipe-stdin', default=False,
              help='If enabled, the contents of stdin are executed in the container. '
                   'This option supports heredocs in shells that support them. '
                   'Disabled by default.')
def run(image_tag, use_sandbox, pipe_stdin):
    """Start an artifact container."""
    log.info('Note that Docker requires sudo.')
    docker.docker_run(image_tag, use_sandbox, pipe_stdin)


@cli.command()
@click.option('--image-tag', required=False,
              type=str,
              help='The artifact image tag.')
@click.option('--all', is_flag=True)
def show(image_tag, all):
    """Display artifact metadata."""
    if all:
        log.info('Gathering metadata for all artifacts. This might take a minute.')
        results = bugswarmapi.list_artifacts()
        log.info(pprint.pformat(results, indent=2))
    elif image_tag:
        log.info('Showing metadata for artifact with image tag', image_tag + '.')
        response = bugswarmapi.find_artifact(image_tag)
        artifact = response.json()
        log.info(pprint.pformat(artifact, indent=2))
