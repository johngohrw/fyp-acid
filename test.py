import os

import cv2
import sklearn

import sys
sys.path.append("./ocr/");

from ocr import OCR


if __name__ == "__main__":
    currentDir = os.path.dirname(os.path.realpath(__file__));
    compPath = os.path.join(currentDir, "dataset/COMP");
    noCompPath = os.path.join(currentDir, "dataset/NOCOMP");

    compImgs = os.listdir(compPath);
    noCompImgs = os.listdir(noCompPath);
    print(len(compImgs));
    print(len(noCompImgs));

    ocr = OCR();

    data = [];
    labels = [];
    for comp in compImgs:
        imgPath = os.path.join(compPath, comp);
        img = cv2.imread(imgPath);
        _, texts = ocr.recognize(img);

        features = [];
        for key, value in texts.items():
            if len(key) == 0:
                continue;
            if len(features) == 6:
                break;
            if value > 1:
                features.append(value);

        while len(features) < 6:
            features.append(0);

        data.append(features);
        labels.append(1);

    print(len(data));
    print(len(labels));

