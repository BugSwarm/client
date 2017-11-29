import subprocess
import sys

import click

from bugswarmcommon import log
from bugswarmcommon.credentials import DOCKER_HUB_REPO

SCRIPT_DEFAULT = '/bin/bash'
CONTAINER_SANDBOX_DEFAULT = '/bugswarm-sandbox'


# By default, this function downloads the image, enters the container, and executes '/bin/bash' in the container.
# The executed script can be changed by passing the script argument.
def docker_run(image_tag, script=None, sandbox=None, input_stream=None):
    assert isinstance(image_tag, str) and not image_tag.isspace()

    script = script or SCRIPT_DEFAULT
    using_script = script != SCRIPT_DEFAULT
    assert isinstance(script, str) and not script.isspace()

    using_sandbox = False
    if sandbox is not None:
        assert isinstance(sandbox, str) and not sandbox.isspace()
        using_sandbox = True

    # First, try to pull the image.
    ok = docker_pull(image_tag)
    if not ok:
        return False

    # if using_sandbox:
        # Confirm that the user wants to use the passed sandbox.
        # if not click.confirm('\n'
        #                      'Due to a limitation of Docker, your sandbox directory ({}) and everything it contains '
        #                      'will become readable, writable, and executable by everyone.\n'
        #                      'Are you sure you want to continue?'.format(sandbox)):
        #     return False

    # Communicate progress to the user.
    container_sandbox = CONTAINER_SANDBOX_DEFAULT
    if using_sandbox:
        log.info('Binding host sandbox', sandbox, 'to container directory', container_sandbox)

    # Communicate progress to the user.
    if using_script:
        log.info('Entering the container and executing', script + '.')
    else:
        log.info('Entering the container.')

    # Prepare the arguments for the docker run command.
    image_location = _image_location(image_tag)
    volume_args = ['-v', '{}:{}'.format(sandbox, container_sandbox)] if using_sandbox else []
    input_args = [] if True else ['-i', '-t']
    subprocess_stdin = sys.stdin if True else None
    # If we're using a shared directory, we need to modify the start script to change the permissions of the shared
    # directory on the container side. However, this will also change the permissions on the host side.
    script_args = [script]
    if using_sandbox:
        start_command = 'sudo chmod -R 777 {} && cd {} && umask 000 && cd .. && {}'.format(
            container_sandbox, container_sandbox, script)
        # These arguments represent a command of the following form:
        # /bin/bash -c "sudo chmod 777 <container_sandbox> && cd <container_sandbox> && umask 000 && /bin/bash"
        # So bash will execute chmod and umask and then start a new bash shell. From the user's perspective, the chmod
        # and umask commands happen transparently. That is, the user only sees the final new bash shell.
        script_args = [SCRIPT_DEFAULT, '-c', start_command]

    # Try to run the image.
    args = ['sudo', 'docker', 'run', '--privileged'] + volume_args + input_args + [image_location] + script_args
    process = subprocess.Popen(args, shell=True, stdin=subprocess_stdin)
    _ = process.communicate()
    return process.returncode == 0


def docker_pull(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)

    # Exit early if the image already exists locally.
    if _image_exists_locally(image_tag):
        return True

    image_location = _image_location(image_tag)
    args = ['sudo', 'docker', 'pull', image_location]
    process = subprocess.Popen(args)
    _ = process.communicate()
    if process.returncode != 0:
        log.error('Could not download the image', image_location, 'from Docker Hub.')
    else:
        log.info('Downloaded the image', image_location + '.')
    return process.returncode == 0


# Returns True if the image already exists locally.
def _docker_image_inspect(image_tag):
    image_location = _image_location(image_tag)
    args = ['sudo', 'docker', 'image', 'inspect', image_location]
    process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _ = process.communicate()
    # For a non-existent image, docker image inspect has a non-zero exit status.
    if process.returncode == 0:
        log.info('The image', image_location, 'already exists locally and is up to date.')
    return process.returncode == 0


# Returns True if the image already exists locally.
def _image_exists_locally(image_tag):
    return _docker_image_inspect(image_tag)


def _image_location(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)
    return DOCKER_HUB_REPO + ':' + image_tag
