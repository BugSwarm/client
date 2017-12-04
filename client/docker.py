import os
import subprocess
import sys

from bugswarmcommon import log
from bugswarmcommon.credentials import DOCKER_HUB_REPO

SCRIPT_DEFAULT = '/bin/bash'
HOST_SANDBOX_DEFAULT = '~/bugswarm-sandbox'
CONTAINER_SANDBOX_DEFAULT = '/bugswarm-sandbox'


# By default, this function downloads the image, enters the container, and executes '/bin/bash' in the container.
# The executed script can be changed by passing the script argument.
def docker_run(image_tag, use_sandbox=False, use_pipe_stdin=False):
    assert isinstance(image_tag, str) and not image_tag.isspace()
    assert isinstance(use_sandbox, bool)
    assert isinstance(use_pipe_stdin, bool)

    # First, try to pull the image.
    ok = docker_pull(image_tag)
    if not ok:
        return False

    # Communicate progress to the user.
    host_sandbox = _default_host_sandbox()
    container_sandbox = CONTAINER_SANDBOX_DEFAULT
    if use_sandbox:
        log.info('Binding host sandbox', host_sandbox, 'to container directory', container_sandbox)

    # Communicate progress to the user.
    if use_pipe_stdin:
        log.info('Entering the container and executing the contents of stdin inside the container.')
    else:
        log.info('Entering the container.')

    image_location = _image_location(image_tag)

    # Prepare the arguments for the docker run command.
    volume_args = ['-v', '{}:{}'.format(host_sandbox, container_sandbox)] if use_sandbox else []
    # The -t option must not be used in order to use a heredoc.
    input_args = ['-i'] if use_pipe_stdin else ['-i', '-t']
    subprocess_stdin = sys.stdin if use_pipe_stdin else None
    # If we're using a shared directory, we need to modify the start script to change the permissions of the shared
    # directory on the container side. However, this will also change the permissions on the host side.
    script_args = [SCRIPT_DEFAULT]
    if use_sandbox:
        start_command = 'sudo chmod -R 777 {} && cd {} && umask 000 && cd .. && {}'.format(
            container_sandbox, container_sandbox, SCRIPT_DEFAULT)
        # These arguments represent a command of the following form:
        # /bin/bash -c "sudo chmod 777 <container_sandbox> && cd <container_sandbox> && umask 000 && /bin/bash"
        # So bash will execute chmod and umask and then start a new bash shell. From the user's perspective, the chmod
        # and umask commands happen transparently. That is, the user only sees the final new bash shell.
        script_args = [SCRIPT_DEFAULT, '-c', start_command]

    # Try to run the image.
    # The tail arguments must be at the end of the command.
    tail_args = [image_location] + script_args
    args = ['sudo', 'docker', 'run', '--privileged'] + volume_args + input_args + tail_args
    process = subprocess.Popen(args, stdin=subprocess_stdin)
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


def _default_host_sandbox():
    return os.path.expanduser(HOST_SANDBOX_DEFAULT)
