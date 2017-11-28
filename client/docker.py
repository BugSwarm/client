import subprocess

from bugswarmcommon import log
from bugswarmcommon.credentials import DOCKER_HUB_REPO


# By default, this function downloads the image, enters the container, and executes '/bin/bash' in the container.
# The executed script can be changed by passing the script argument.
def docker_run(image_tag, script=None, shared_dir=None):
    assert isinstance(image_tag, str) and not image_tag.isspace()

    SCRIPT_DEFAULT = '/bin/bash'
    script = script or SCRIPT_DEFAULT
    assert isinstance(script, str) and not script.isspace()

    host_dir, container_dir = None, None
    if shared_dir is not None:
        assert isinstance(shared_dir, tuple)
        assert len(shared_dir) == 2
        host_dir, container_dir = shared_dir
        assert isinstance(host_dir, str) and not host_dir.isspace()
        assert isinstance(container_dir, str) and not container_dir.isspace()

    # First, try to pull the image.
    ok = docker_pull(image_tag)
    if not ok:
        return False

    # Communicate what is happening next to the user. The output depends on the passed script and shared_dir parameters.
    default_shared_dir = host_dir is None and container_dir is None
    if not default_shared_dir:
        log.info('Binding host directory', host_dir, 'to container directory', container_dir)

    default_script = script == SCRIPT_DEFAULT
    if not default_script:
        log.info('Entering the container and executing', script + '.')
    else:
        log.info('Entering the container.')

    # Now try to run the image.
    image_location = _image_location(image_tag)
    volume_args = ['-v', ':'.join([host_dir, container_dir])] if shared_dir else []
    args = ['sudo', 'docker', 'run', '--privileged'] + volume_args + ['-i', '-t', image_location, script]
    process = subprocess.Popen(args)
    _ = process.communicate()
    return process.returncode == 0


def docker_pull(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)

    image_location = _image_location(image_tag)
    args = ['sudo', 'docker', 'pull', image_location]
    process = subprocess.Popen(args)
    _ = process.communicate()
    if process.returncode != 0:
        log.error('Could not download the image', image_location, 'from Docker Hub.')
    else:
        log.info('Downloaded the image', image_location + '.')
    return process.returncode == 0


def _image_location(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)
    return DOCKER_HUB_REPO + ':' + image_tag
