# Hierarchy
# Each Contour has either a parent or a child or both
# Like in a box, there are things in it. The things are the child, and boundary is the parent
# Hierarchy Representation
# Each contour has info on who is the child and parent
# [Next, Previous, First_Child, Parent]
# Next = Whoever is in the same hierarchy level
#   Same Hierarchy means that both contour is separated, but in the same level
#   Starting from 0 -> n, numbers of same hierarchy level contour
#   If there are no Next, then next = -1
# Previous = reverse of Next

import cv2
import numpy as np

imagy = '1.jpg'
img = cv2.imread(imagy)

# find contours and get the external one
# Second Parameter
#   RETR_LIST (When Hierarchy is not important)
#        retrieves all the contours, 
#           but doesn't create any parent-child relationship
#        PARENTS AND CHILD ARE EQUAL. 
#        EVERY CONTOUR BELONGS TO THE SAME HIERARCHY LEVEL
#        So in [N, P, 1st_child, parent] => 1st_child and parent will always be -1
#        So, what you will see from contour 0 is a list of all contours

#   RETR_EXTERNAL
#       Only Returns Extreme Outer Flags
#       All child contours are left behind
#       So, the interest is the same hierarchy level, no other contours 
#           are taken into account      

#   RETR_CCOMP
#       Retrieves all contours and arranges them to 2 level hierarchy
#       Contour label as 1 -> If there are other contour inside this contour
#       Contour label as 2 -> If there are no objects or contour inside the object
#       Contour from 2 to 1 -> If previously labeled as 2 and there is
#                               a contour in it, change to 1

#   RETR_TREE
#       Retrieves all contours and creates a full family hierarchy list
#       Tells more than parent and child. 
#           i.e. Grandparent Father Son Grandson...
#       

image, contours, hier = cv2.findContours(img, cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)