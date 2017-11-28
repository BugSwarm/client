import subprocess

from bugswarmcommon import log
from bugswarmcommon.credentials import DOCKER_HUB_REPO


# By default, this function downloads the image, enters the container, and executes '/bin/bash' in the container.
# The executed script can be changed by passing the script argument.
def docker_run(image_tag, script=None, volume_binding=None):
    assert image_tag
    assert isinstance(image_tag, str)

    script = script or '/bin/bash'
    assert script
    assert isinstance(script, str)

    if volume_binding is not None:
        assert isinstance(volume_binding, str)

    if script:
        log.info('Downloading image with tag', image_tag, 'and executing', script, 'in the container.')
    else:
        log.info('Downloading image with tag', image_tag, 'and entering container.')

    # First, try to pull the image.
    ok = docker_pull(image_tag)
    if not ok:
        return False

    # Now try to run the image.
    log.info('Note that Docker requires sudo.')
    image_location = _image_location(image_tag)
    volume_args = ['-v', volume_binding] if volume_binding else []
    args = ['sudo', 'docker', 'run', '--privileged'] + volume_args + ['-i', '-t', image_location, script]
    process = subprocess.Popen(args)
    _ = process.communicate()
    if process.returncode != 0:
        log.error('Could not run the image', image_location + '.')
        return False
    return process.returncode == 0


def docker_pull(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)

    image_location = _image_location(image_tag)
    args = ['docker', 'pull', image_location]
    process = subprocess.Popen(args)
    _ = process.communicate()
    if process.returncode != 0:
        log.error('Could not download the image', image_location, 'from Docker Hub.')
    return process.returncode == 0


def _image_location(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)
    return DOCKER_HUB_REPO + ':' + image_tag