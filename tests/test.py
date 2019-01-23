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
    assert metadata['id'] == "mask_rcnn_nucleus_detection-keras-model"
    assert metadata['name'] == "mask_rcnn_nucleus_detection Keras Model"
    assert metadata['description'] == "mask_rcnn_nucleus_detection Keras model trained on 2018 Data Science Bowl"
    assert metadata['license'] == 'Apache License 2.0'


def test_predict():

    model_endpoint = 'http://localhost:5000/model/predict'

    # Test by the image with multiple nucleis
    img1_path = 'assets/example.png'

    with open(img1_path, 'rb') as file:
        file_form = {'image': (img1_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'
    assert len(response['predictions']) == 61
    assert len(response['predictions'][0]['mask']) > 0
    assert response['predictions'][0]['score'] > 0.95

    # Test by the text data
    img3_path = 'README.md'

    with open(img3_path, 'rb') as file:
        file_form = {'image': (img3_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__])
