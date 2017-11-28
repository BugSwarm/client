import subprocess

from bugswarmcommon import log
from bugswarmcommon.credentials import DOCKER_HUB_REPO


# By default, this function downloads the image, enters the container, and executes '/bin/bash' in the container.
# The executed script can be changed by passing the script argument.
def docker_run(image_tag, script=None, volume_binding=None):
    assert isinstance(image_tag, str) and not image_tag.isspace()

    SCRIPT_DEFAULT = '/bin/bash'
    script = script or SCRIPT_DEFAULT
    assert isinstance(script, str) and not script.isspace()

    host_dir, container_dir = None, None
    if volume_binding is not None:
        assert isinstance(volume_binding, tuple)
        assert len(volume_binding) == 2
        host_dir, container_dir = volume_binding
        assert isinstance(host_dir, str) and not host_dir.isspace()
        assert isinstance(container_dir, str) and not container_dir.isspace()

    # First, try to pull the image.
    ok = docker_pull(image_tag)
    if not ok:
        return False

    # Communicate what is happening next to the user. The output depends on the passed script and volume_binding
    # parameters. If we start accepting more parameters, this logic will become unruly and will need to be refactored.
    default_script = script == SCRIPT_DEFAULT
    default_volume_binding = host_dir is None and container_dir is None
    if default_volume_binding and default_script:
        log.info('Entering container.')
    elif default_volume_binding and not default_script:
        log.info('Executing', script, 'in the container.')
    elif not default_volume_binding and default_script:
        log.info('Binding host directory', host_dir,
                 'to container directory', container_dir,
                 'and entering container.')
    elif default_volume_binding and not default_script:
        log.info('Binding host directory', host_dir,
                 'to container directory', container_dir,
                 'and executing', script, 'in the container.')

    # Now try to run the image.
    log.info('Note that Docker requires sudo.')
    image_location = _image_location(image_tag)
    volume_args = ['-v', ':'.join([host_dir, container_dir])] if volume_binding else []
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
    else:
        log.info('Downloaded the image', image_location + '.')
    return process.returncode == 0


def _image_location(image_tag):
    assert image_tag
    assert isinstance(image_tag, str)
    return DOCKER_HUB_REPO + ':' + image_tag
