import os

import cv2
import numpy as np
import sklearn

import sys
sys.path.append("./ocr/");

from ocr import OCR


def getOCRFeatures(imgNames, imgDir, ocr, data, labels, label_value, limit = 15):
    for i in range(limit):
        img = imgNames[i];
        print(img);
        imgPath = os.path.join(imgDir, img);
        img = cv2.imread(imgPath);
        _, texts = ocr.recognize(img);

        # Don't mind the code below, just doing some bullshit
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
        print(features);
        labels.append(label_value);


if __name__ == "__main__":
    dataFilename = "data.csv";
    labelFilename = "labels.txt";
    # Data or label file does not exist then just extract the features, give
    # label and write them to their respective files
    if not os.path.isfile(dataFilename) or not os.path.isfile(labelFilename):
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
        getOCRFeatures(compImgs, compPath, ocr, data, labels, 1);
        getOCRFeatures(noCompImgs, noCompPath, ocr, data, labels, 0, limit = 10);
        with open(dataFilename, "w") as dataFile, open(labelFilename, "w") as labelsFile:
            for i in range(len(data)):
                dataRow = data[i];
                dataStr = "";
                for j in range(len(dataRow)-1):
                    dataStr += str(dataRow[j]) + ",";
                dataStr += str(dataRow[len(dataRow)-1]) + "\n";
                dataFile.write(dataStr);

                label = labels[i];
                labelsFile.write(str(label) + "\n");
    else:
        npData = np.genfromtxt(dataFilename, delimiter=",");
        npLabels = np.genfromtxt(labelFilename, delimiter="\n", dtype=np.uint8);
        assert npData.shape[0] == npLabels.shape[0];
        print(npData);
        print(npLabels);

