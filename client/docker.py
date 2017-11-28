import subprocess

from bugswarmcommon import log
from bugswarmcommon.credentials import DOCKER_HUB_REPO


# By default, this function downloads the image, enters the container, and executes '/bin/bash' in the container.
# The executed script can be changed by passing the script argument.
def docker_run(image_tag, script=None, shared_dir=None):
    assert isinstance(image_tag, str) and not image_tag.isspace()

    SCRIPT_DEFAULT = '/bin/bash'
    script = script or SCRIPT_DEFAULT
    using_script = script != SCRIPT_DEFAULT
    assert isinstance(script, str) and not script.isspace()

    host_dir, container_dir = None, None
    using_shared_dir = False
    if shared_dir is not None:
        assert isinstance(shared_dir, tuple)
        assert len(shared_dir) == 2
        host_dir, container_dir = shared_dir
        assert isinstance(host_dir, str) and not host_dir.isspace()
        assert isinstance(container_dir, str) and not container_dir.isspace()
        using_shared_dir = True

    # First, try to pull the image.
    ok = docker_pull(image_tag)
    if not ok:
        return False

    # Communicate what is happening next to the user.
    if using_shared_dir:
        log.info('Binding host directory', host_dir, 'to container directory', container_dir)

    if using_script:
        log.info('Entering the container and executing', script + '.')
    else:
        log.info('Entering the container.')

    # Now try to run the image.
    image_location = _image_location(image_tag)
    volume_args = ['-v', ':'.join([host_dir, container_dir])] if shared_dir else []

    # If we're using a shared directory, we need to modify the start script to change the permissions of the shared
    # directory on the container side. However, this will also change the permissions on the host side.
    script_args = [script]
    if using_shared_dir:
        script_args = [SCRIPT_DEFAULT, '-c', 'sudo chmod 777 {} && {}'.format(container_dir, script)]

    args = ['sudo', 'docker', 'run', '--privileged'] + volume_args + ['-i', '-t', image_location] + script_args
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
