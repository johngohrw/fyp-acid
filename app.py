import tensorflow as tf

import io
import numpy as np
import cv2
#from skimage import data, io, filters
from flask import *

# Path to your python modules
import sys
sys.path.append("./ocr/");

from ocr import OCR

global ocrEngine
app = Flask(__name__);


def main():
    # All things global should be defined here
    global ocrEngine;
    ocrEngine = OCR();


@app.route("/")
def hello_world():
    return render_template("index.html");


@app.route("/api/v0/ocr", methods=["POST"])
def file_upload():
    print(request.files);
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return "400 BAD REQUEST", 400;
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('No selected file')
        return "400 BAD REQUEST", 400;

    if file:
        in_memory_img = io.BytesIO();
        imgbuf = np.fromstring(in_memory_img.getvalue(), np.uint8);
        img = cv2.imdecode(imgbuf, cv2.IMREAD_UNCHANGED);
        edges, binImg = ocrEngine.preprocess(img);
        resultImg = ocrEngine.recognize(img, edges, binImg);

        # JPEG files supported only for the moment
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


if __name__ == "__main__":
    main();
    app.run();

