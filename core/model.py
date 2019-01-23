import io
import logging

import skimage.color
import skimage.io
import skimage.transform
from keras.backend import clear_session
from maxfw.model import MAXModelWrapper

from config import DEFAULT_MODEL_PATH, MODEL_NAME
from core.mask_rcnn.mrcnn import model as model_lib
from core.mask_rcnn.nucleus.nucleus import NucleusInferenceConfig, mask_to_rle

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):

    MODEL_META_DATA = {
        'id': '{}-keras-model'.format(MODEL_NAME.lower()),
        'name': '{} Keras Model'.format(MODEL_NAME),
        'description':
            '{} Keras model trained on 2018 Data Science Bowl'.format(MODEL_NAME),
        'type': 'Image Segmentation',
        'license': 'Apache License 2.0',
        'source': 'https://developer.ibm.com/exchanges/models/all/max-nucleus-segmenter/'
    }

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        clear_session()
        config = NucleusInferenceConfig()
        config.display()

        self.model = model_lib.MaskRCNN(mode="inference", config=config, model_dir="")
        self.model.load_weights(path, by_name=True)
        # this seems to be required to make Keras models play nicely with threads
        self.model.keras_model._make_predict_function()
        logger.info('Loaded model: {}'.format(self.model.keras_model.name))

    def _read_image(self, image_data):
        image = skimage.io.imread(io.BytesIO(image_data), plugin='imageio')
        return image

    def _pre_process(self, image):
        # If grayscale. Convert to RGB for consistency.
        if image.ndim != 3:
            image = skimage.color.gray2rgb(image)
        # If has an alpha channel, remove it for consistency
        if image.shape[-1] == 4:
            image = image[..., :3]
        return image

    def _post_process(self, preds):
        rle = mask_to_rle(preds["masks"], preds["scores"])
        return rle

    def _predict(self, x):
        preds = self.model.detect([x], verbose=0)[0]
        return preds
