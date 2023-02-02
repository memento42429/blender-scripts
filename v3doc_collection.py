#!/usr/bin/python3

"""Sample script that shows how to list models, and various operations with them (comments,
collections...) using the V3 api and the requests library."""

import json

# import the requests library
# http://docs.python-requests.org/en/latest
# pip install requests
import requests
from requests.exceptions import RequestException

SKETCHFAB_API_URL = 'https://api.sketchfab.com/v3'
API_TOKEN = 'YOUR API_TOKEN from https://sketchfab.com/settings/password'


def _get_request_payload(*, data=None, files=None, json_payload=False):
    """Helper method that returns the authentication token and proper content type depending on
    whether or not we use JSON payload."""
    data = data or {}
    files = files or {}

    headers = {'Authorization': 'Token {}'.format(API_TOKEN)}

    if json_payload:
        headers.update({'Content-Type': 'application/json'})
        data = json.dumps(data)

    return {'data': data, 'files': files, 'headers': headers}


def list_my_models():
    my_models_endpoint = f'{SKETCHFAB_API_URL}/me/models'
    payload = _get_request_payload()

    try:
        response = requests.get(my_models_endpoint, **payload)
    except RequestException as exc:
        print(f'An API error occured: {exc}')
    else:
        data = response.json()

        if not len(data['results']) > 0:
            print('You don\'t seem to have any model :(')

        return data['results']


def get_collection():
    my_collections_endpoint = f'{SKETCHFAB_API_URL}/me/collections'
    payload = _get_request_payload()

    try:
        response = requests.get(my_collections_endpoint, **payload)
    except RequestException as exc:
        print(f'An API error occured: {exc}')
        exit(1)

    data = response.json()

    if not data['results']:
        print('You don\'t seem to have any collection, let\'s create one!')
        return
    else:
        return data['results'][0]


def create_collection(model):
    collections_endpoint = f'{SKETCHFAB_API_URL}/collections'
    data = {'name': 'A Beautiful Collection', 'models': [model['uid']]}
    payload = _get_request_payload(data=data, json_payload=True)

    try:
        response = requests.post(collections_endpoint, **payload)
    except RequestException as exc:
        print(f'An API error occured: {exc}')
    else:
        # We created our collection \o/
        # Now retrieve the data
        collection_url = response.headers['Location']
        response = requests.get(collection_url)

        return response.json()


def add_model_to_collection(model, collection):
    collection_model_endpoint = f'{SKETCHFAB_API_URL}/collections/{collection["uid"]}/models'

    payload = _get_request_payload(data={'models': [model['uid']]}, json_payload=True)
    try:
        response = requests.post(collection_model_endpoint, **payload)
    except RequestException as exc:
        print(f'An API error occured: {exc}')
    else:
        if response.status_code == requests.codes.created:
            print(f'Model successfully added to collection {collection["uid"]}!')
        else:
            print('Model already in collection')


def remove_model_from_collection(model, collection):
    collection_model_endpoint = f'{SKETCHFAB_API_URL}/collections/{collection["uid"]}/models'

    payload = _get_request_payload(data={'models': [model['uid']]}, json_payload=True)
    try:
        response = requests.delete(collection_model_endpoint, **payload)
    except RequestException as exc:
        print(f'An API error occured: {exc}')
    else:
        if response.status_code == requests.codes.no_content:
            print(f'Model successfully removed from collection {collection["uid"]}!')
        else:
            print(f'Model not in collection: {response.content}')


def comment_model(model, msg):
    comment_endpoint = f'{SKETCHFAB_API_URL}/comments'

    payload = _get_request_payload(data={'model': model['uid'], 'body': msg}, json_payload=True)
    try:
        response = requests.post(comment_endpoint, **payload)
    except RequestException as exc:
        print(f'An API error occured: {exc}')
    else:
        if response.status_code == requests.codes.created:
            print('Comment successfully posted!')
        else:
            print(f'Failed to post the comment: {response.content}')


if __name__ == '__main__':
    # This requires that your profile contains at least two models
    print('Getting models from your profile...')

    if models := list_my_models():
        try:
            model_1, model_2, *models = models
        except ValueError:
            print('You need at least two models in your profile to run this script')
            exit(1)

        # List your collections, create one if you don't have any
        collection = get_collection()

        if not collection:
            collection = create_collection(model_1)

        print(f'Now do some more stuff on model {model_2["uid"]}')

        # Obviously it's not really logical but these are just examples
        # of what you can achieve
        add_model_to_collection(model_2, collection)
        comment_model(model_2, u'Wao, this is... Wao Oo')
        remove_model_from_collection(model_2, collection)
    else:
        print('You don\'t have any models !')