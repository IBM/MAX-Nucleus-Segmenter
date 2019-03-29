# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# API Metadata
API_TITLE = 'MAX Nucleus Segmenter'
API_DESC = 'Identify nuclei in a microscopy image, additionally assigning each pixel of the image to a particular nucleus'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'mask_rcnn_nucleus_detection'
DEFAULT_MODEL_PATH = 'assets/{}.h5'.format(MODEL_NAME)
MODEL_LICENSE = 'Apache License 2.0'
