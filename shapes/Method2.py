import os
import cv2 as cv
import numpy as np

class Shapes:

    def __init__ (self):
        self.image = None;
        self.imgHeight = None;
        self.imgWidth = None;


    def sort_contours(self, cnts, method="left-to-right"):
        # initialize the reverse flag and sort index
        reverse = False
        i = 0

        # handle if we need to sort in reverse
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True

        # handle if we are sorting against the y-coordinate rather than
        # the x-coordinate of the bounding box
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1

        # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
            key=lambda b:b[1][i], reverse=reverse))

        # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)

    def getImageHeightWidth (self, image):
        height, width = image.shape[:2]
        return height, width

    def binarizeImage (self, image):
        (thresh, binarized) = cv.threshold(image, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)  # Thresholding the image

        return binarized

    def invertImage (self, image):
        inv_img = 255 - image

        return inv_img

    def medianBlurImage (self, image):
        kernel_size = 3
        median_blur = cv.medianBlur(image, kernel_size)
        #cv.imshow('blurry', median_blur)

        return median_blur

    def preProcess(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY);
        img_blur = self.medianBlurImage(gray);
        img_binarized = self.binarizeImage(img_blur)
        img_inverted = self.invertImage(img_binarized)
        return img_inverted

    def getImageArea(self):
        img_area = self.imgHeight * self.imgWidth
        return img_area

    def boxFeatures(self, img, output_limit = 8):
        self.image = img
        self.imgHeight = self.image.shape[0]
        self.imgWidth = self.image.shape[1]

        processed = self.preProcess()

        # Defining a kernel length
        kernel_length = np.array(self.image).shape[1]//40

        # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
        verticle_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, kernel_length))

        # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv.getStructuringElement(cv.MORPH_RECT, (kernel_length, 1))

        # A kernel of (3 X 3) ones.
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

        # Morphological operation to detect verticle lines from an image
        img_temp1 = cv.erode(processed, verticle_kernel, iterations=3)
        verticle_lines_img = cv.dilate(img_temp1, verticle_kernel, iterations=3)

        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv.erode(processed, hori_kernel, iterations=3)
        horizontal_lines_img = cv.dilate(img_temp2, hori_kernel, iterations=3)

        # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
        alpha = 0.5
        beta = 1.0 - alpha

        # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
        img_final_bin = cv.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
        img_final_bin = cv.erode(~img_final_bin, kernel, iterations=2)
        (thresh, img_final_bin) = cv.threshold(img_final_bin, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

        # Find contours for image, which will detect all the boxes
        im2, contours, hierarchy = cv.findContours(
            img_final_bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Sort all the contours by top to bottom.
        (contours, boundingBoxes) = self.sort_contours(contours, method="top-to-bottom")

        threshed_height = self.imgHeight *0.3
        threshed_width = self.imgWidth * 0.3

        featureArray = []

        for c in contours:
            # Returns the location and width,height for every contour
            x, y, w, h = cv.boundingRect(c)
            cv.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            contour_area = w*h
            area_ratio = contour_area / self.getImageArea()
            featureArray.append(area_ratio)
            if len(featureArray) == output_limit:
                break;

        while len(featureArray) < output_limit:
            featureArray.append(0);

        return featureArray


def writeToFile (toWrite):
    resultArea = open('resultShape.txt', 'w')
    resultArea.write(str(the_features))
    resultArea.write('\n')
    resultArea.close()

if __name__ == "__main__":
    currentDir = os.path.dirname(os.path.realpath(__file__));
    img_name = "Images/" + str(1) + ".jpg"
    img_path = os.path.join(currentDir, img_name )

    image = cv.imread(img_path)
    shape = Shapes();
    the_features = shape.boxFeatures(image)

    writeToFile(the_features)



