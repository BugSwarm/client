import json
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
    log.config_logging(getattr(logging, 'INFO', None))


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
              help='If enabled, artifact containers will be cleaned up automatically after use. '
                   'Disable this behavior if you want to inspect the container filesystem after use. '
                   'Enabled by default.')
def run(image_tag, use_sandbox, pipe_stdin, rm):
    """Start an artifact container."""
    log.info('Note that Docker requires sudo privileges.')
    docker.docker_run(image_tag, use_sandbox, pipe_stdin, rm)


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
        # Print without the INFO prefix so the output is easier to parse.
        print(json.dumps(results, sort_keys=True, indent=4))
    elif image_tag:
        response = bugswarmapi.find_artifact(image_tag)
        artifact = response.json()
        # Print without the INFO prefix so the output is easier to parse.
        print(json.dumps(artifact, sort_keys=True, indent=4))
