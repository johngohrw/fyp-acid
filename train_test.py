import os

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


if __name__ == "__main__":
    dataFilename = "data.csv";
    labelFilename = "labels.txt";
    # Data or label file does not exist then just extract the features, give
    # label and write them to their respective files
    if not os.path.isfile(dataFilename) or not os.path.isfile(labelFilename):
        print("No data CSV file or label file");
    else:
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
        # Split the dataset to train+validation and test first
        X_train, X_test, y_train, y_test = train_test_split(npData, npLabels, random_state=0);

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

        # Grid search (aka parameter testing) and cross validation
        cross_k = 5;

        # Testing best parameters for linear SVM
        linear_param_grid = {"C": [0.001, 0.01, 0.1, 1, 10, 100]};
        linear_grid_search = GridSearchCV(LinearSVC(random_state=0), linear_param_grid, cv=cross_k);
        linear_grid_search.fit(X_train, y_train);
        print("Linear SVM");
        print("===========");
        print("Linear SVM best cross-validation score: {:.2f}".format(linear_grid_search.best_score_));
        print("Linear SVM best parameters: {}".format(linear_grid_search.best_params_));
        print("Linear SVM Train set score: {:.2f}".format(linear_grid_search.score(X_train, y_train)));
        print("Linear SVM Test set predictions:\n{}".format(linear_grid_search.predict(X_test)));
        print("Linear SVM Test set score: {:.2f}\n".format(linear_grid_search.score(X_test, y_test)));

        # Testing the best parameters for RBF kernel SVM
        kernel_param_grid = {"gamma": [0.001, 0.01, 0.1, 1, 10, 100],
                "C": [0.001, 0.01, 0.1, 1, 10, 100]};
        kernel_grid_search = GridSearchCV(SVC(random_state=0), kernel_param_grid, cv=cross_k);
        kernel_grid_search.fit(X_train, y_train);
        print("RBF Kernel SVM");
        print("==============");
        print("RBF Kernel SVM best cross-validation score: {:.2f}".format(kernel_grid_search.best_score_));
        print("RBF Kernel SVM best parameters: {}".format(kernel_grid_search.best_params_));
        print("RBF Kernel SVM Train set score: {:.2f}".format(kernel_grid_search.score(X_train, y_train)));
        print("RBF Kernel SVM Test set predictions:\n{}".format(kernel_grid_search.predict(X_test)));
        print("RBF Kernel SVM Test score: {:.2f}\n".format(kernel_grid_search.score(X_test, y_test)));

        # Testing the best parameters for KNN
        knn_param_grid = {"n_neighbors": [1, 2, 3]};
        knn_grid_search = GridSearchCV(KNeighborsClassifier(), knn_param_grid, cv=cross_k);
        knn_grid_search.fit(X_train, y_train);
        print("K nearest neighbours");
        print("====================");
        print("KNN best cross-validation score: {:.2f}".format(knn_grid_search.best_score_));
        print("KNN best parameters: {}".format(knn_grid_search.best_params_));
        print("KNN Train set score: {:.2f}".format(knn_grid_search.score(X_train, y_train)));
        print("KNN Test set predictions:\n{}".format(knn_grid_search.predict(X_test)));
        print("KNN Test set score: {:.2f}\n".format(knn_grid_search.score(X_test, y_test)));


        # Confusion matrix is a 2x2 matrix, where row is the true class
        # while column is the predicted class
        #     0  1
        # 0 |TN|FP|         TN = True Negative (Predicted 0 and is actually 0)
        # 1 |FN|TP|         FP = False Positive (Predicted 1 but actually 0)
        #                   FN = False Negative (Predicted 0 but actually 1)
        #                   TP = True Positive (Predicted 1 and is actually 1)
        #
        #confusion = confusion_matrix(y_test, y_pred);
        #print("Kernel SVM confustion matrix:\n{}".format(confusion));

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
        #print(y_test);
        #print(classification_report(y_test, y_pred, target_names=["not-compound", "compound"]));

