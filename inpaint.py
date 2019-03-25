
'''
Usage:
  python3 inpaint.py [<image>]

Keys:
  SPACE - inpaint
  r     - reset the inpainting mask
  ESC   - exit
'''

from __future__ import print_function

import numpy as np
import cv2 as cv
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", help = 'required image path file')
args = vars(ap.parse_args())


from common import Sketcher

def main():
    img = cv.imread(args["image"])

    if img is None:
        print('Failed to load image file:', args["image"])


    img_mark = img.copy()
    mark = np.zeros(img.shape[:2], np.uint8)
    sketch = Sketcher('img', [img_mark, mark], lambda : ((255, 255, 255), 255))

    while True:
        ch = cv.waitKey()
        if ch == 27:
            break
        if ch == ord(' '):
            res = cv.inpaint(img_mark, mark, 3, cv.INPAINT_TELEA)
            cv.imshow('inpaint', res)
        if ch == ord('r'):
            img_mark[:] = img
            mark[:] = 0
            sketch.show()

    print('Completed')


if __name__ == '__main__':
    main()
    cv.destroyAllWindows()
