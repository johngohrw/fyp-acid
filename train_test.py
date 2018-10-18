import os
import sys

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.externals import joblib


class ACIDTrainTest:

    def __init__(self, dataFilename, labelFilename):
        npData = np.genfromtxt(dataFilename, delimiter=",");
        npLabels = np.genfromtxt(labelFilename, delimiter="\n", dtype=np.uint8);
        assert npData.shape[0] == npLabels.shape[0];

        # Training and testing set
        #
        # The train_test_split method randomly shuffles the data and labels for us.
        # Potentially useful params:
        #   test_size: float, int (between 0.0 and 1.0), default = 0.25
        #   train_size: float, int (between 0.0 and 1.0)
        #   random_state: A fixed seed value to give to the PRNG
        #
        # X denotes the features/data while y denotes the class labels
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(npData, npLabels, random_state=1);
        print("\nTraining set size: {}".format(self.y_train.shape[0]));
        print("Test set size: {}".format(self.y_test.shape[0]));

        train_comp_count = np.count_nonzero(self.y_train);
        train_comp_percent = train_comp_count/self.y_train.shape[0];
        train_nocomp_percent = 1 - train_comp_percent;
        print("Compound images in training set: {:.2f}".format(train_comp_percent));
        print("Non-compound images in training set: {:.2f}".format(train_nocomp_percent));

        test_comp_count = np.count_nonzero(self.y_test);
        test_comp_percent = test_comp_count/self.y_test.shape[0];
        test_nocomp_percent = 1 - test_comp_percent;
        print("Compound images in test set: {:.2f}".format(test_comp_percent));
        print("Non-compound images in test set: {:.2f}\n".format(test_nocomp_percent));


    def paramTestCrossValidate(self, estimator, model_name, param_grid, cross_k):
        #
        # Grid search (aka parameter testing) and cross validation
        #
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

        grid_search = GridSearchCV(estimator, param_grid, cv=cross_k);
        grid_search.fit(self.X_train, self.y_train);
        print("{}".format(model_name));
        print("===========");
        print("{} best cross-validation score: {:.2f}".format(model_name, grid_search.best_score_));
        print("{} best parameters: {}".format(model_name, grid_search.best_params_));
        print("{} Train set score: {:.2f}".format(model_name, grid_search.score(self.X_train, self.y_train)));
        print("{} Test set score: {:.2f}\n".format(model_name, grid_search.score(self.X_test, self.y_test)));

        # Confusion matrix is a 2x2 matrix, where row is the true class
        # while column is the predicted class
        #     0  1
        # 0 |TN|FP|         TN = True Negative (Predicted 0 and is actually 0)
        # 1 |FN|TP|         FP = False Positive (Predicted 1 but actually 0)
        #                   FN = False Negative (Predicted 0 but actually 1)
        #                   TP = True Positive (Predicted 1 and is actually 1)
        #
        y_pred = grid_search.predict(self.X_test);
        confusion = confusion_matrix(self.y_test, y_pred);
        print("{} confusion matrix:\n{}".format(model_name, confusion));

        # Summarizing the confustion matrix
        #
        # Precision = TP / TP + FP (how many predicted positive are actually
        #                           positive)
        # Recall = TP / TP + FN (identify all positive samples and measure
        #                        its correctness to predict positive samples)
        #
        # f1-score (F) = 2 * precision * recall
        #                   --------------------
        #                    precision + recall
        print(classification_report(self.y_test, y_pred, target_names=["non-compound", "compound"]));
        print();

        # Saves the model for persistence
        filename = model_name.lower().replace(' ', '_') + ".model";
        joblib.dump(grid_search.best_estimator_, filename);


if __name__ == "__main__":
    dataFilename = "data.csv";
    labelFilename = "labels.txt";
    if not os.path.isfile(dataFilename) or not os.path.isfile(labelFilename):
        print("No data CSV file or label file");
    else:
        model_names = ["Linear SVM", "RBF Kernel SVM", "KNN"];
        model_filenames = [name.lower().replace(' ','_') + ".model" for name in model_names];

        # Check the existence of persistent models, to prevent having
        # to build the model again
        for model_file in model_filenames:
            if os.path.isfile(model_file):
                print("{} already exists".format(model_file));
                sys.exit();


        acid = ACIDTrainTest(dataFilename, labelFilename);

        # Stratified version ensures that the percentages of the samples
        # for each class (compound and non-compound) are preserved in
        # each fold, preventing an imbalance distribution
        cross_k = StratifiedKFold(n_splits=5);

        # Testing best parameters for linear SVM
        linear_param_grid = {"C": [0.001, 0.01, 0.1, 1, 10, 100]};
        acid.paramTestCrossValidate(LinearSVC(random_state=0), model_names[0], linear_param_grid, cross_k);

        # Testing the best parameters for RBF kernel SVM
        kernel_param_grid = {"gamma": [0.001, 0.01, 0.1, 1, 10, 100],
                "C": [0.001, 0.01, 0.1, 1, 10, 100]};
        acid.paramTestCrossValidate(SVC(random_state=0), model_names[1], kernel_param_grid, cross_k);

        # Testing the best parameters for KNN
        knn_param_grid = {"n_neighbors": [1, 2, 3, 4, 5, 6]};
        acid.paramTestCrossValidate(KNeighborsClassifier(), model_names[2], knn_param_grid, cross_k);

