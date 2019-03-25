"""
Usage:
  python3 inpaint.py [<image>]

Keys:
  SPACE - inpaint
  r     - reset the inpainting mask
  ESC   - exit
"""
import numpy as np
import cv2 as cv
import argparse
# TODO: Copy Sketcher class to inpaint.py
# TODO: Remove below line
from common import Sketcher

ap = argparse.ArgumentParser()
# TODO: Add default argument
ap.add_argument("-i", "--image", help = 'required image path file')
args = vars(ap.parse_args())


def main():
    # Read image in color mode
    img = cv.imread(args["image"], cv.IMREAD_COLOR)

    # If image is not read properly, return error
    if img is None:
        print('Failed to load image file: {}'.format(args["image"]))
        return

    # Create a copy of original image
    img_mark = img.copy()
    # Create a black copy of original image
    # Acts as a mask
    mark = np.zeros(img.shape[:2], np.uint8)
    # Create sketch using OpenCV Utility Class: Sketcher
    sketch = Sketcher('img', [img_mark, mark], lambda : ((255, 255, 255), 255))

    while True:
        ch = cv.waitKey()
        if ch == 27:
            break
        if ch == ord(' '):
            # Use Algorithm proposed by Alexendra Telea: Fast Marching Method (2004)
            # Reference: https://pdfs.semanticscholar.org/622d/5f432e515da69f8f220fb92b17c8426d0427.pdf
            res = cv.inpaint(src=img_mark, inpaintMask=mark, inpaintRadius=3, flags=cv.INPAINT_TELEA)
            cv.imshow('Inpaint Output', res)
        if ch == ord('r'):
            img_mark[:] = img
            mark[:] = 0
            sketch.show()

    print('Completed')


if __name__ == '__main__':
    main()
    cv.destroyAllWindows()
