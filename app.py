import tensorflow as tf

import numpy as np
import cv2
from skimage import data, io, filters
from flask import *

app = Flask(__name__);

@app.route("/")
def hello_world():
    return render_template("index.html");

@app.route("/upload", methods=["POST"])
def file_upload():
    imgbuf = np.fromstring(request.data, np.uint8);
    img = cv2.imdecode(imgbuf, cv2.IMREAD_GRAYSCALE);
    return "File received!", 201;

@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404;

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("405_error.html"), 405

