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

class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv.imshow(self.windowname, self.dests[0])
        cv.imshow(self.windowname + ": mask", self.dests[1])

    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv.EVENT_LBUTTONUP:
            self.prev_pt = None

        if self.prev_pt and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", default="sample.jpeg", help = 'required image path file')
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
