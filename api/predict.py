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

from core.model import ModelWrapper
from flask_restplus import fields, abort
from werkzeug.datastructures import FileStorage
from maxfw.core import MAX_API, PredictAPI

# Set up parser for input data (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files',
                          required=True,
                          help="An image file (JPG/PNG/TIFF). Valid input size: 64 * 64, 128 * 128, 256 * 256")


label_prediction = MAX_API.model('NucleusPrediction', {
    'mask': fields.List(fields.Integer(
        required=True, description='Segmented masks of each nucleus. The mask '
                                   'is compressed by Run-length encoding.')),
    'probability': fields.Float(
        required=True, description='Predicted probability for presence of the nucleus')
})


predict_response = MAX_API.model('ModelPredictResponse', {
    'status': fields.String(required=True,
                            description='Response status message'),
    'predictions': fields.List(fields.Nested(label_prediction))
})


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    @MAX_API.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()
        try:
            input_data = args['image'].read()
            image = self.model_wrapper._read_image(input_data)
        except ValueError:
            abort(400,
                  "Please submit a valid image in PNG, Tiff or JPEG format")

        preds = self.model_wrapper.predict(image)
        result['predictions'] = preds
        result['status'] = 'ok'

        return result
