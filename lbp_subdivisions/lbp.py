# import the necessary packages
from pyimagesearch.localbinarypatterns import LocalBinaryPatterns
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--input", required=True, help="input folder which contains images to lbp")
args = vars(ap.parse_args())

print(args)
 
# initialize the local binary patterns descriptor along with
# the data and label lists
desc = LocalBinaryPatterns(24, 8)
data = []
labels = []

# loop over the images
print('processing images..')
for imagePath in paths.list_images(args["input"]):
	# load the image, convert it to grayscale, and describe it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)
 
	# extract the label from the image path, then update the
	# label and data lists
	labels.append(imagePath.split("/")[-2])
	data.append(hist)


print(data)