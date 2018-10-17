import io
import numpy as np
import cv2
import random
#from skimage import data, io, filters
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


global ocrEngine, lbpEngine, shapesEngine;
app = Flask(__name__);
app.config["ALLOWED_EXTENSIONS"] = set(['png', 'jpg', 'jpeg']);


def main():
    # All things global should be defined here
    global ocrEngine, lbpEngine, shapesEngine;
    lbpEngine = LocalBinaryPatterns(8, 24, "uniform");
    shapesEngine = Shapes();
    ocrEngine = OCR();


@app.route("/")
def hello_world():
    return render_template("index.html");


def valid_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"];

@app.route("/api/v0/classify", methods=["POST"])
def classify_endpoint():
    # TODO: handle different query params (e.g: SVM, KNN, both, etc)
    # example: user = request.args.get('user')
    # Unverified, just followed some example to handle multiple file upload
    uploaded_files = request.files.getlist("file[]");
    for file in uploaded_files:
        if file and valid_file(file.filename):
            img = decode_img(file);

            lbpFeatures = getLBPHistogram(lbpEngine, img);
            shapeFeatures = shapesEngine.boxFeatures(img);
            _, ocrFeatures = ocr.recognize(img);

            features = np.append(lbpFeatures, shapeFeatures.append(ocrFeatures));
            # Round to five decimal places
            features = np.around(features, decimal=5);

            # Give features to our trained model here



@app.route("/api/v0/ocr", methods=["POST"])
def ocr_endpoint():
    img = handle_file_upload(request);
    if img.shape[0] == 0:
        return "400 BAD REQUEST", 400;
    results, frequency = ocrEngine.recognize(img);

    # JPEG files supported only for the moment
    _, buffer = cv2.imencode(".jpg", results[0]);
    response = make_response(buffer.tobytes());
    response.headers["Content-Type"] = "image/jpeg"
    return response, 201;


@app.route("/api/v0/lbp", methods=["POST"])
def lbp_endpoint():
    img = handle_file_upload(request);
    if img.shape[0] == 0:
        return "400 BAD REQUEST", 400;

    randomID = random.getrandbits(128);
    blocksize = 10; # blocksize of region subdivisions

    print('{}: starting preprocessing..'.format(randomID));
    preprocessedImg = lbpEngine.preprocess(img);
    print('{}: computing distance array..'.format(randomID));
    dist_array = lbpEngine.compute_distance_array(preprocessedImg, blocksize)
    print('{}: computing bottom shift..'.format(randomID));
    bottomshifted = lbpEngine.bottom_shift(dist_array);
    print('{}: computing right shift..'.format(randomID));
    rightshifted = lbpEngine.right_shift(dist_array);
    print('{}: done!'.format(randomID));
    resultImg = dist_array;

    _, buffer = cv2.imencode(".jpg", resultImg);
    response = make_response(buffer.tobytes());
    response.headers["Content-Type"] = "image/jpeg"
    return response, 201;


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404;

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("405_error.html"), 405


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

    if file:
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

