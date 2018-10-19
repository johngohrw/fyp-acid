import io
import numpy as np
import cv2
import random
from sklearn.externals import joblib
from flask import *

# Path to your python modules
import sys
sys.path.append("./lbp/");
sys.path.append("./shapes/");
sys.path.append("./ocr/");

from modules.lbp import LocalBinaryPatterns
from lbp2 import getLBPHistogram
from Method2 import Shapes
from ocr import OCR


global ocrEngine, lbpEngine, shapesEngine, models
app = Flask(__name__);
app.config["ALLOWED_EXTENSIONS"] = set(['png', 'jpg', 'jpeg']);


def main():
    # All things global should be defined here
    global ocrEngine, lbpEngine, shapesEngine, models
    lbpEngine = LocalBinaryPatterns(8, 24, "uniform");
    shapesEngine = Shapes();
    ocrEngine = OCR();
    # Load the pre-trained classification models
    models = {};
    models["linear"] = joblib.load("ml/linear_svm.model");
    models["rbf"] = joblib.load("ml/rbf_kernel_svm.model");
    models["knn"] = joblib.load("ml/knn.model");


@app.route("/")
def hello_world():
    return "Nothing to see here... :D";


def valid_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"];

@app.route("/api/v0/classify", methods=["POST"])
def classify_endpoint():
    img = handle_file_upload(request);
    if img.shape[0] == 0:
        return "400 BAD REQUEST", 400;

    lbpFeatures = getLBPHistogram(lbpEngine, img);
    shapeFeatures = shapesEngine.boxFeatures(img);
    _, ocrFeatures = ocrEngine.recognize(img);

    features = np.append(lbpFeatures, np.append(shapeFeatures, ocrFeatures));
    # For some reason it became a numpy array of strings
    features = np.asarray(features, dtype=float);

    # Round to five decimal places
    features = np.around(features, decimals=5);
    # Needs to be in a 2d array, even though its single class prediction
    features = [features.tolist()];

    # Multiple models may be chosen for prediction
    param = request.args.get("model");
    results = [];
    for modelName in param.split(","):
        model = models[modelName];
        pred = model.predict(features)[0];
        results.append({"model": modelName, "prediction": str(pred)});

    response = jsonify(results);
    response.headers.add('Access-Control-Allow-Origin', '*');
    return response, 201;


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404;

@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


def handle_file_upload(request):
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return np.array([]);
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('No selected file')
        return np.array([]);

    if file and valid_file(file.filename):
        return decode_img(file);


def decode_img(file):
    in_memory_img = io.BytesIO();
    file.save(in_memory_img);
    imgbuf = np.fromstring(in_memory_img.getvalue(), np.uint8);
    img = cv2.imdecode(imgbuf, cv2.IMREAD_UNCHANGED);
    return img;


if __name__ == "__main__":
    main();
    app.run();

