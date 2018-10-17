import os
import cv2 as cv
import numpy as np

class Shapes:

    def __init__ (self):
        self.image = None;
        self.imgHeight = None;
        self.imgWidth = None;

    def getImageHeightWidth (self, image):
        # Get the Height and width of the original image
        height, width = image.shape[:2]
        return height, width

    def binarizeImage (self, image):
        # Binarizing the grayscaled image using otsu. Since we have different kind of images, trial and error for the best threshold for all images
        #       is not ideal here. So, otsu is used instead to allow an automatic calculation of a threshold value from an image histogram into bimodal image.
        (thresh, binarized) = cv.threshold(image, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        return binarized

    def invertImage (self, image):
        # Invert the image colour. Input image have to be black and white
        # Since FindContours treats white as foreground and black as blackground, we invert it for a better detection.
        inv_img = 255 - image
        return inv_img

    def medianBlurImage (self, image):
        # Remove noise. Blur Image
        kernel_size = 3
        median_blur = cv.medianBlur(image, kernel_size)
        return median_blur

    def preProcess(self):
        # Preprocess the image for shape detection.
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY);
        img_blur = self.medianBlurImage(gray);
        img_binarized = self.binarizeImage(img_blur)
        img_inverted = self.invertImage(img_binarized)
        return img_inverted

    def getImageArea(self):
        # Returns the area of the original image
        img_area = self.imgHeight * self.imgWidth
        return img_area

    def detectHoriLines(self, img, kernel):
        # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv.getStructuringElement(cv.MORPH_RECT, (kernel, 1))
        
        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv.erode(img, hori_kernel, iterations=3)
        hori_img = cv.dilate(img_temp2, hori_kernel, iterations=3)
        return hori_img


    def detectVertLines(self, img, kernel):
        # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
        verticle_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, kernel))

        # Morphological operation to detect verticle lines from an image
        img_temp1 = cv.erode(img, verticle_kernel, iterations=3)
        vert_img = cv.dilate(img_temp1, verticle_kernel, iterations=3)
        return vert_img

    def combineHoriVert(self, horizontal_img, vertical_img):
        # A kernel of (3 X 3) ones.
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

        # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
        alpha = 0.5
        beta = 1.0 - alpha

        # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
        combined = cv.addWeighted(vertical_img, alpha, horizontal_img, beta, 0.0)
        combined = cv.erode(~combined, kernel, iterations=2)
        (thresh, combined) = cv.threshold(combined, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

        return combined

    def getBoxFeatures(self, img, output_limit = 8):
        # Find contours for image, which will detect all the boxes
        # Find all the contours
        im2, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        # Sort all the contours by the largest to the smallest
        contour = sorted(contours, key=cv.contourArea, reverse = True)

        threshed_height = self.imgHeight *0.3
        threshed_width = self.imgWidth * 0.3

        featureArray = []

        for c in contour:
            # Returns the location and width,height for every contour
            x, y, w, h = cv.boundingRect(c)
            cv.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv.imshow('rect', self.image)
            cv.waitKey(0)

            contour_area = w*h
            area_ratio = contour_area / self.getImageArea()
            featureArray.append(area_ratio)
            if len(featureArray) == output_limit:
                break;

        while len(featureArray) < output_limit:
            featureArray.append(0);

        return featureArray

    def boxFeatures(self, img):
        # Starts the shape feature extraction for the image.
        self.image = img
        self.imgHeight = self.image.shape[0]
        self.imgWidth = self.image.shape[1]

        processed = self.preProcess()

        # Defining a kernel length
        kernel_length = np.array(self.image).shape[1]//40

        hori_img = self.detectHoriLines(processed, kernel_length)
        vert_img = self.detectVertLines(processed, kernel_length)

        combined_img = self.combineHoriVert(hori_img, vert_img)        

        array_features = self.getBoxFeatures(combined_img)

        return array_features
        


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



