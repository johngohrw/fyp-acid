from PIL import Image
from pylab import *

img = array(Image.open('5.jpg').convert('L'))

figure()

contour(img, levels=[245], colors = 'black', origin = 'image')
axis('equal')

show()
