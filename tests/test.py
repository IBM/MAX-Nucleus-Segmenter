#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests
import pytest


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Nucleus Segmenter'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == "max-nucleus-segmenter"
    assert metadata['name'] == "MAX Nucleus Segmenter"
    assert metadata['description'] == "Nucleus image segmentation model trained with Keras on 2018 Data Science Bowl dataset"
    assert metadata['license'] == 'Apache License 2.0'


def test_predict():

    model_endpoint = 'http://localhost:5000/model/predict'

    # Test by the image with multiple nuclei
    img_png = 'assets/example.png'
    img_jpg = 'tests/example.jpg'
    img_tiff = 'tests/example.tiff'

    for img_file in [img_png, img_jpg, img_tiff]:
        with open(img_file, 'rb') as file:
            file_form = {'image': (img_file, file, 'image/jpeg')}
            r = requests.post(url=model_endpoint, files=file_form)

        assert r.status_code == 200
        response = r.json()

        assert response['status'] == 'ok'
        assert 60 <= len(response['predictions']) <= 61
        assert len(response['predictions'][0]['mask']) > 0
        assert response['predictions'][0]['probability'] > 0.95

    # Test by the image without nuclei
    non_nucleus_img = 'assets/non-nucleus.png'
    with open(non_nucleus_img, 'rb') as file:
        file_form = {'image': (non_nucleus_img, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'
    assert len(response['predictions']) == 0

    # Test by the text data
    img3_path = 'README.md'

    with open(img3_path, 'rb') as file:
        file_form = {'image': (img3_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__])
