from core.model import ModelWrapper
from flask_restplus import fields, abort
from werkzeug.datastructures import FileStorage
from maxfw.core import MAX_API, PredictAPI

# Set up parser for input data (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files',
                          required=True,
                          help="An image file (RGB/HWC, 64 * 64, 128 * 128, 256 * 256)")


label_prediction = MAX_API.model('NucleusPrediction', {
    'mask': fields.List(fields.Integer(
        required=True, description='Segmented masks of each nucleus. The mask '
                                   'is compressed by Run-length encoding.')),
    'score': fields.Float(
        required=True, description='Predicted probability for the class label')
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
