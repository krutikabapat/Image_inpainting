import cv2
import numpy as np 

img = cv2.imread('/home/Desktop/latest.jpeg')
img = np.zeros(img, np.uint8)

img = cv2.line(img,(22,44),(82,102),(255,0,0),1)
cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()