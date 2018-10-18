import os
import cv2 as cv
import numpy as np

class Shapes:

    def __init__ (self):
        self.image = None;          # Original Image
        self.imgHeight = None;      # Original Image's Height
        self.imgWidth = None;       # Original Image's Width

    def getImageHeightWidth (self, image):
        # Get the Height and width of the original image and save it
        height, width = image.shape[:2]
        return height, width

    def getImageArea(self):
        # Returns the area of the original image
        img_area = self.imgHeight * self.imgWidth
        return img_area

    def medianBlurImage (self, image):
        # Remove noise. Blur the Image
        kernel_size = 3
        median_blur = cv.medianBlur(image, kernel_size)
        return median_blur
    
    def binarizeImage (self, image):
        # Binarizing the grayscaled image using otsu. Since we have different kind of images, trial and error for the best threshold for all images is not ideal here. 
        # So, otsu is used instead to allow an automatic calculation of a threshold value from an image histogram into bimodal image.
        (thresh, binarized) = cv.threshold(image, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        return binarized

    def invertImage (self, image):
        # Invert the image colour. Input image have to be black and white
        # Since openCV findContours function treats white as foreground and black as blackground, we invert it for a better detection.
        inv_img = 255 - image
        return inv_img

    def preProcess(self):
        # Preprocess the image for shape detection.
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY);
        img_blur = self.medianBlurImage(gray);
        img_binarized = self.binarizeImage(img_blur)
        img_inverted = self.invertImage(img_binarized)
        return img_inverted

    def morphHoriLines(self, img):
        # This function performs a morphological operation HORIZONTALLY on the image
        #   Extracting only Lines that are detected to be horizontal occurding to the specified kernel 
        hori_kernel = self.imgWidth // 30
   
        # Create structure element for extracting horizontal lines through morphology operations
        horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (hori_kernel, 1))
    
        # Apply morphology operations
        hori_img = cv.erode(img, horizontalStructure)
        hori_img = cv.dilate(hori_img, horizontalStructure)
 
        return hori_img

    def morphVertLines(self, img):
        # This function performs a morphological operation VERTICALLY on the image
        #   Extracting only Lines that are detected to be vertical occurding to the specified kernel 
        vert_kernel = self.imgHeight // 30
    
        # Create structure element for extracting vertical lines through morphology operations
        verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, vert_kernel))

        # Apply morphology operations
        vert_img = cv.erode(img, verticalStructure)
        vert_img = cv.dilate(vert_img, verticalStructure)

        return vert_img

    def combineHoriVert(self, horizontal_img, vertical_img):
        # Combining both vertical image and horizontal image
        #   To allow a better detection on only the vertical and horizontal lines of the box
        
        # Inverting the image to fit in the findContour function later on
        adding = ~cv.add(vertical_img, horizontal_img)
        
        return adding

    def featuresExtraction(self, img, output_limit = 8):
        # Find contours for image, which will detect all the boxes
        # Find all the contours
        im2, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        # Sort all the contours by the largest to the smallest area
        contour = sorted(contours, key=cv.contourArea, reverse = True)

        # Define all the threshold of the box we do not want to detect. These boxes appear due to noises or uneccessary stuff
        smallest_threshed_height = self.imgHeight *0.2
        smallest_threshed_width = self.imgWidth * 0.2

        # Putting all the features into the array
        featureArray = []

        # Looping through all contours to get the features
        for c in contour:
            # Returns the location, width and height
            x, y, w, h = cv.boundingRect(c)
            contour_area = w*h      # Gets the area of the contour
            image_area = self.getImageArea()    # Get the area of the image

            # If the contour detected is not the border of the image, continue on
            if (contour_area != image_area):
                # Threshold that was defined previously
                if (w >= smallest_threshed_width and h >= smallest_threshed_height ):
                    cv.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    # Get the area ratio as the data for Machine Learning later on
                    area_ratio = contour_area / image_area
                    # Put it into the area
                    featureArray.append(area_ratio)

            # If there are more features detected then we just stop, cause we dont want more
            if len(featureArray) == output_limit:
                break;

        # If we detected way less contour as usual, then we append 0's to make up for the space
        while len(featureArray) < output_limit:
            featureArray.append(0);

        return featureArray

    def boxFeatures(self, img):
        # Starts the shape feature extraction for the image.
        self.image = img
        self.imgHeight = self.image.shape[0]
        self.imgWidth = self.image.shape[1]

        # Perform a pre-process on the image
        processed = self.preProcess()

        # Both morphological horizontal lines and vertical lines are taken from openCV's website. The following is the source
        # source: https://docs.opencv.org/3.4/dd/dd7/tutorial_morph_lines_detection.html
        hori_img = self.morphHoriLines(processed)
        vert_img = self.morphVertLines(processed)

        # Perform a combination of both vertical image and horizontal image.
        combined_img = self.combineHoriVert(hori_img, vert_img)        

        # Get the features
        array_features = self.featuresExtraction(combined_img)

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
    cv.destroyAllWindows()

    writeToFile(the_features)



