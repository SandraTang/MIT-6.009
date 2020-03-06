#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, x, y):
    if x < 0:
        x = 0
    if x >= image['width']:
        x = image['width'] -1
    if y < 0:
        y = 0
    if y >= image['height']:
        y = image['height'] -1
    return image['pixels'][image['width']*y+x]


def set_pixel(image, x, y, c):
    image['pixels'][image['width']*y+x] = c


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': image['pixels'].copy()
    }
    for x in range(image['width']):
        for y in range(image['height']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS

def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    A kernel is a list of lists.
    So
    0 1 2
    3 4 5 
    6 7 8
    is represented as
    [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    """
    result = {
        'height': (image['height']),
        'width': (image['width']),
        'pixels': image['pixels'].copy()
    }

    #iterate through all pixels in image
    for x in range(image['width']):
        for y in range(image['height']):
            color = get_pixel(image, x, y)
            kernel_width = len(kernel[0])
            kernel_height = len(kernel)
            effect = 0
            #iterate and sum effect of kernel application
            for i in range(kernel_width):
                for j in range(kernel_height):
                    # print(kernel[j][i])
                    # print(get_pixel(image, x-(kernel_width//2)+i, y-(kernel_height//2)+j))
                    effect += kernel[j][i] * get_pixel(image, x-(kernel_width//2)+i, y-(kernel_height//2)+j)
            set_pixel(result, x, y, effect)
    # print(result)
    return result


def round_and_clip_helper(c):
    if c < 0:
        c = 0
    if c > 255:
        c = 255
    c = round(c)
    return c

def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    return apply_per_pixel(image, round_and_clip_helper)


# FILTERS

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    kernel = []
    for _ in range(n):
        kernel.append([1/(n**2)]*n)
    # print(kernel)

    # then compute the correlation of the input image with that kernel
    img = correlate(image, kernel)
    # print(img)
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    img = round_and_clip_image(img)
    # print(img)
    return img

def sharpened(i, n):
    kernel = []
    for _ in range(n):
        kernel.append([-1/(n**2)]*n)
    kernel[n//2][n//2] += 2
    img = correlate(i, kernel)
    img = round_and_clip_image(img)
    return img

def edges(i):
    kernel_x = [[-1, 0, 1], 
                [-2, 0, 2], 
                [-1, 0, 1]]
    kernel_y = [[-1, -2, -1], 
                [0, 0, 0],
                [1, 2, 1]]
    img_x = correlate(i, kernel_x)
    img_y = correlate(i, kernel_y)
    #combine effects of x and y kernel
    #square, add, square root

    result = {
        'height': i['height'],
        'width': i['width'],
        'pixels': i['pixels'].copy()
    }
    for x in range(i['width']):
        for y in range(i['height']):
            color_x = get_pixel(img_x, x, y)
            color_y = get_pixel(img_y, x, y)
            newcolor = (color_x**2 + color_y**2)**0.5
            set_pixel(result, x, y, newcolor)

    img = round_and_clip_image(result)
    return img

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    # pic = load_image('test_images/bluegill.png')
    # pic = inverted(pic)
    # save_image(pic, "bluegill.png")
    # # # test_images/pigbird.png
    # pic = load_image('test_images/construct.png')
    # pic = edges(pic)
    # save_image(pic, "construct.png")
    pass