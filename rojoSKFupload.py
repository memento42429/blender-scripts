#!/usr/bin/python3

"""Sample script for uploading to Sketchfab using the V3 API and the requests library."""

import os
import json
from pathlib import Path
from time import sleep
from unicodedata import category

# import the requests library
# http://docs.python-requests.org/en/latest
# pip install requests
import requests
from requests.exceptions import RequestException

##
# Uploading a model to Sketchfab is a two step process
#
# 1. Upload a model. If the upload is successful, the API will return
#    the model's uid in the `Location` header, and the model will be placed in the processing queue
#
# 2. Poll for the processing status
#    You can use your model id (see 1.) to poll the model processing status
#    The processing status can be one of the following:
#    - PENDING: the model is in the processing queue
#    - PROCESSING: the model is being processed
#    - SUCCESSED: the model has being sucessfully processed and can be view on sketchfab.com
#    - FAILED: the processing has failed. An error message detailing the reason for the failure
#              will be returned with the response
#
# HINTS
# - limit the rate at which you poll for the status (once every few seconds is more than enough)
##

SKETCHFAB_API_URL = 'https://api.sketchfab.com/v3'
# API_TOKEN = 'b22a1408a460494aa718098700afc054' # rojohaku API token
API_TOKEN = '05263c13aabb4cf79ed9372611a6ccd2' # GMNH API token
MAX_RETRIES = 50
MAX_ERRORS = 10
RETRY_TIMEOUT = 5  # seconds

dirpath = str(r"I:\20220923_Gunma_Kimura_WhaleDataBase\periotic_tympanic_bulla_for_upload\test")

def _get_request_payload(*, data=None, files=None, json_payload=False):
    """Helper method that returns the authentication token and proper content type depending on
    whether or not we use JSON payload."""
    data = data or {}
    files = files or {}
    headers = {'Authorization': f'Token {API_TOKEN}'}

    if json_payload:
        headers.update({'Content-Type': 'application/json'})
        data = json.dumps(data)

    return {'data': data, 'files': files, 'headers': headers}


def upload(path, # this function return 'model_url'
            name = 'test model テストモデル', #'This is a bob model I made with love and passion'
            description = 'This is test description. \n\n 日本語も可能です。\n\n改行は2行必要。',
            tags = ['test', 'rojohaku', 'skulls', 'mammals'], #['bob', 'character', 'video-games'], Array of tags
            categ = [''], # ['people'], Array of categories slugs
            license = 'by-nc', #'by', License slug
            private = 1, # 1, requires a pro account
            password = 'my-password', # requires a pro account
            isPublished = False, # Model will be on draft instead of published
            isInspectable = True): # Allow 2D view in model inspector
    """
    POST a model to sketchfab.
    This endpoint only accepts formData as we upload a file.
    """
    model_endpoint = f'{SKETCHFAB_API_URL}/models'

    # Mandatory parameters
    model_file = path # path to your model ex) './data/pikachu.zip'

    # Optional parameters
    data = {'name': name,
            'description': description,
            'tags': tags,
            'categories': categ,
            'license': license,
            'private': private,
            'password': password,
            'isPublished': isPublished,
            'isInspectable': isInspectable
    }

    print('Uploading...')

    with open(model_file, 'rb') as file_:
        files = {'modelFile': file_}
        payload = _get_request_payload(data=data, files=files)

        try:
            response = requests.post(model_endpoint, **payload)
        except RequestException as exc:
            print(f'An error occured: {exc}')
            return

    if response.status_code != requests.codes.created:
        print(f'Upload failed with error: {response.json()}')
        return

    # Should be https://api.sketchfab.com/v3/models/XXXX
    model_url = response.headers['Location']
    print('Upload successful. Your model is being processed.')
    print(f'Once the processing is done, the model will be available at: {model_url}')

    return model_url


def poll_processing_status(model_url):
    """GET the model endpoint to check the processing status."""
    errors = 0
    retry = 0

    print('Start polling processing status for model')

    while (retry < MAX_RETRIES) and (errors < MAX_ERRORS):
        print(f'Try polling processing status (attempt #{retry})...')

        payload = _get_request_payload()

        try:
            response = requests.get(model_url, **payload)
        except RequestException as exc:
            print(f'Try failed with error {exc}')
            errors += 1
            retry += 1
            continue

        result = response.json()

        if response.status_code != requests.codes.ok:
            print(f'Upload failed with error: {result["error"]}')
            errors += 1
            retry += 1
            continue

        processing_status = result['status']['processing']

        if processing_status == 'PENDING':
            print(f'Your model is in the processing queue. Will retry in {RETRY_TIMEOUT} seconds')
            retry += 1
            sleep(RETRY_TIMEOUT)
            continue
        elif processing_status == 'PROCESSING':
            print(f'Your model is still being processed. Will retry in {RETRY_TIMEOUT} seconds')
            retry += 1
            sleep(RETRY_TIMEOUT)
            continue
        elif processing_status == 'FAILED':
            print(f'Processing failed: {result["error"]}')
            return False
        elif processing_status == 'SUCCEEDED':
            print(f'Processing successful. Check your model here: {model_url}')
            return True

        retry += 1

    print('Stopped polling after too many retries or too many errors')
    return False


def patch_model(model_url):
    """
    PATCH the model endpoint to update its name, description...
    Important: The call uses a JSON payload.
    """

    payload = _get_request_payload(data={}, json_payload=True)

    try:
        response = requests.patch(model_url, **payload)
    except RequestException as exc:
        print(f'An error occured: {exc}')
    else:
        if response.status_code == requests.codes.no_content:
            print('PATCH model successful.')
        else:
            print(f'PATCH model failed with error: {response.content}')


def patch_model_options(model_url):
    """PATCH the model options endpoint to update the model background, shading, orienration."""
    data = {
        'shading': 'lit',
        'background': '{"color": "#555555"}',
        # For axis/angle rotation:
        'orientation': '{"axis": [1, 1, 0], "angle": 34}',
        # Or for 4x4 matrix rotation:
        # 'orientation': '{"matrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]}'
    }
    payload = _get_request_payload(data=data, json_payload=True)
    try:
        response = requests.patch(f'{model_url}/options', **payload)
    except RequestException as exc:
        print(f'An error occured: {exc}')
    else:
        if response.status_code == requests.codes.no_content:
            print('PATCH options successful.')
        else:
            print(f'PATCH options failed with error: {response.content}')


# get whole file names with .blend
def search_models(path,list_models):
    """
    output list of dir of stl under the folder.
    """
    p = Path(path)
    i = 0
    for file in p.iterdir():
        if file.is_dir():
            search_models(file,list_models)
        elif file.is_file():
            base, ext = os.path.splitext(file) #make taple
            if ext == ".blend":
                # resolve()を使って絶対パスを表示する
                list_models.append(file.resolve())
    return list_models

###################################
# Uploads, polls and patch a model
###################################

if __name__ == '__main__':
    list_models = search_models(dirpath,[])
    for model in list_models:
        path = model
        filename = str(model).split("\\")
        basename = filename[-1].split(".")[0] # like a "Ziphius_cavirostris_USNM530291_tyb"
        if model_url := upload(path, name = basename):
            if poll_processing_status(model_url):
                patch_model(model_url)
                patch_model_options(model_url)
