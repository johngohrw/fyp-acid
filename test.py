import os

import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

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

        # Data has 'X' as prefix while the labels have 'y' as prefix
        #
        # This method randomly shuffles the data and labels for us.
        # Potentially useful params:
        #   test_size: float, int (between 0.0 and 1.0), default = 0.25
        #   train_size: float, int (between 0.0 and 1.0)
        #   random_state: A fixed seed value to give to the PRNG
        #
        X_train, X_test, y_train, y_test = train_test_split(npData, npLabels, random_state=0);
        print(X_train);
        print(X_test);
        print(y_train);
        print(y_test);

        # Training with KNN (2 neighbor classifier)
        knn = KNeighborsClassifier(n_neighbors=2);
        knn.fit(X_train, y_train);
        print("KNN Train set score: {:.2f}".format(knn.score(X_train, y_train)));

        # Testing with KNN
        y_pred = knn.predict(X_test);
        print("KNN Test set predictions:\n{}".format(y_pred));
        print("KNN Test set score: {:.2f}".format(knn.score(X_test, y_test)));

        # Training with SVM
        svm = LinearSVC(random_state=0, C=750);
        svm.fit(X_train, y_train);
        print("SVM Train set score: {:.2f}".format(svm.score(X_train, y_train)));

        # Testing with SVM
        svm_y_pred = svm.predict(X_test);
        print("SVM Test set predictions:\n{}".format(svm_y_pred));
        print("SVM Test set score: {:.2f}".format(svm.score(X_test, y_test)));

        # Performing k fold cross validation (5 folds)
        # NOTE: Cross validation is not used to build a model for
        # new data. K models are build when running a k fold cross validation
        # so it just evaluate how well the model will generalize when
        # trained on a specific dataset
        #
        # Other cross validation methods:
        # LeaveOneOut: Like k fold cross validation, but each fold is a single
        #              sample
        # ShuffleSplit: Shuffles and splits the data set into training
        #               set and into testing set, and repeats this for N
        #               iterations. Training and test set do not have to
        #               be 100% together, which means some samples could be
        #               left out in each iteration, useful for large datasets
        # GroupKFold: Groups related data together. Data that are of the
        #             of the same group should not be split when doing k fold
        #             cross validation. An example would be like for a model
        #             that attempts to recognize emotions. If there are
        #             multiple shots of the same person but with different
        #             emotions, its better that all the images of that person
        #             to be in the training set, rather than having some in
        #             training and some in testing.
        knn2 = KNeighborsClassifier(n_neighbors=2);
        kfold = KFold(n_splits=5, shuffle=True, random_state=0);
        scores = cross_val_score(knn2, npData, npLabels, cv=kfold);
        print("Cross validation scores: {}".format(scores));
        print("Average cross-validation score: {:.2f}".format(scores.mean()));

