import json
import pprint

import requests

from . import log

BASE_URL = 'http://52.173.92.238/api/v1'
ARTIFACTS_RESOURCE = 'artifacts'


def insert_artifact(artifact):
    log.debug('Trying to add artifact.')
    if artifact is None:
        raise ValueError
    resp = _perform_post(_artifacts_endpoint(), artifact)
    if resp.status_code == 422:
        log.error('The artifact was not added because it failed validation.')
        log.error(pprint.pformat(artifact))
        return False
    return True


def find_artifact(image_tag):
    log.debug('Trying to find artifact with image_tag', image_tag + '.')
    if not isinstance(image_tag, str):
        raise ValueError
    resp = _perform_get(_artifact_image_tag_resource(image_tag))
    log.debug(resp.url)
    log.debug(resp.content)
    return resp


def list_artifacts():
    return _perform_get(_artifacts_endpoint())


def count_artifacts():
    raise NotImplementedError


def _perform_get(endpoint):
    return requests.get(endpoint)


def _perform_post(endpoint, data):
    headers = {'Content-Type': 'application/json'}
    return requests.post(endpoint, json.dumps(data), headers=headers)


def _endpoint(resource):
    return '/'.join([BASE_URL, resource])


def _artifacts_endpoint():
    return _endpoint(ARTIFACTS_RESOURCE)


def _artifact_image_tag_resource(image_tag):
    if not isinstance(image_tag, str):
        raise ValueError
    return '/'.join([_artifacts_endpoint(), image_tag])
