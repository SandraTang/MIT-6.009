#!/usr/bin/env python3

import math

from PIL import Image

#Lab 0 stuff

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
        'pixels': [0]*image['height']*image['width']
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
                    # debugging - passingin tuples?
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

# VARIOUS FILTERS

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    #split the image, apply greycale filter, put image back together
    def split_color_image(img):

        split_image0 = []
        for p in img['pixels']:
            split_image0.append(p[0])

        split_image1 = []
        for p in img['pixels']:
            split_image1.append(p[1])

        split_image2 = []
        for p in img['pixels']:
            split_image2.append(p[2])

        split_images = [split_image0, split_image1, split_image2]

        return split_images

    def recombine_color_image(img):
        pix = []
        img_pixels = split_color_image(img)
        img0 = {'height': img['height'], 'width': img['width'], 'pixels': img_pixels[0]}
        img0 = filt(img0)
        img1 = {'height': img['height'], 'width': img['width'], 'pixels': img_pixels[1]}
        img1 = filt(img1)
        img2 = {'height': img['height'], 'width': img['width'], 'pixels': img_pixels[2]}
        img2 = filt(img2)
        for i in range(len(img['pixels'])):
            pix.append((img0['pixels'][i], img1['pixels'][i], img2['pixels'][i]))
        new_img = {'height': img['height'], 'width': img['width'], 'pixels': pix}
        return new_img

    return recombine_color_image

# def make_box(color):
#     def create_image(h, w):
#         return {'height': h, 'width': w, 'pixels': [color for _ in range(h*w)]}
#     return create_image

# maker = make_box(40)
# im = maker(20, 30)

def make_blur_filter(n):
    def blurred(image):
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
            kernel.append([1.0/(n**2)]*n)

        # then compute the correlation of the input image with that kernel
        # print(image['pixels'])
        img = correlate(image, kernel)
        # print(img)
        # and, finally, make sure that the output is a valid image (using the
        # helper function from above) before returning it.
        img = round_and_clip_image(img)
        # print(img)
        return img
    return blurred

def make_sharpen_filter(n):
    def sharpened(i):
        kernel = []
        for _ in range(n):
            kernel.append([-1.0/(n**2)]*n)
        kernel[n//2][n//2] += 2
        img = correlate(i, kernel)
        img = round_and_clip_image(img)
        return img
    return sharpened


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    # filt()
    def compound(img):
        all_filters = filters[0](img)
        for f in filters[1::]:
            all_filters = f(all_filters)
        return all_filters

    return compound

    #itertive
    # compound = filters[0]
    # for f in filters[1::]:
    #     compound = f(compound)
    # return compound

    #recursive
    # if len(filters) == 1:
    #     return filters[0]
    # return filter_cascade(filters[1:])(filters[0])

# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    #temp use to mess up and turn grey and produce [s] from
    #affect and cut down BOTH temp and img
    img = image.copy()
    for _ in range(ncols):
        temp = greyscale_image_from_color_image(img)
        temp = compute_energy(temp)
        temp = cumulative_energy_map(temp)
        s = minimum_energy_seam(temp)
        img = image_without_seam(img, s)
        temp = img.copy()
    return img

# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    #copied structure from apply per pixel
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0]*image['height']*image['width']
    }
    for x in range(image['width']):
        for y in range(image['height']):
            color = get_pixel(image, x, y)
            r = color[0]
            g = color[1]
            b = color[2]
            #v=round(.299×r+.587×g+.114×b)
            newcolor = 0.299*r + 0.587*g + 0.114*b
            set_pixel(result, x, y, round(newcolor))
    return result


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey) 


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy function),
    computes a "cumulative energy map" as described in the lab 1 writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    #energy is a greyscale image

    result = {
        'height': energy['height'],
        'width': energy['width'],
        'pixels': energy['pixels'].copy()
    }
    # For each row of the "cumulative energy map":
    for y in range(energy['height'])[1::]:
        # For each pixel in the row:
        for x in range(energy['width']):
            # Set this value in the "cumulative energy map" to be:
            # the value of that location in the energy map, added 
            # to the minimum of the cumulative energies from the 
            # "adjacent" pixels in the row above
            color = get_pixel(result, x, y)
            left_above = get_pixel(result, x-1, y-1)
            above = get_pixel(result, x, y-1)
            right_above = get_pixel(result, x+1, y-1)
            newcolor = color + min(left_above, min(above, right_above))
            set_pixel(result, x, y, newcolor)
    return result


def minimum_energy_seam(c):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 1 writeup).
    """
    path = []
    #find index of smallest element in last row
    y = c['height']-1
    min_x = 0
    for x in range(c['width']):
        if get_pixel(c, x, y) < get_pixel(c, min_x, y):
            min_x = x
    path.append(c['width']*y+min_x)
    #make list of rows, from last to first (0)
    y_iter = range(c['height']-1, 0, -1)
    # print(c['height'])
    # print(list(y_iter))
    #for every row
    for y in y_iter:
        #find value and index of adjacent pixels above and compare
        #insert in beginning so path[] reads top to bottom (pixels)
        left_above = get_pixel(c, min_x-1, y-1)
        above = get_pixel(c, min_x, y-1)
        right_above = get_pixel(c, min_x+1, y-1)
        #center
        if min_x <= 0:
            #left 
            if above <= right_above:
                path.insert(0, c['width']*(y-1)+min_x)
            else:
                path.insert(0, c['width']*(y-1)+min_x+1)
                min_x += 1
        elif min_x >= c['width']-1:
            #right
            if left_above <= above:
                path.insert(0, c['width']*(y-1)+min_x-1)
                min_x -= 1
            else:
                path.insert(0, c['width']*(y-1)+min_x)
        else:
            if left_above <= above and left_above <= right_above:
                path.insert(0, c['width']*(y-1)+min_x-1)
                min_x-=1
            elif above <= right_above:
                path.insert(0, c['width']*(y-1)+min_x)
            else:
                path.insert(0, c['width']*(y-1)+min_x+1)
                min_x+=1  
    # print(path)      
    return path


def image_without_seam(im, s):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    # print(im['height'])
    # print(im['width']-1)
    # print(len(s))
    result = {
        'height': im['height'],
        'width': im['width']-1,
        'pixels': [None]*im['height']*(im['width']-1)
    }
    # print(result)
    # print(len(result['pixels']))
    s = sorted(s)
    # print('S list', s)
    counter = 0
    setback = 0
    for y in range(im['height']):
        setback = 0
        for x in range(im['width']):
            counter += 1
            # if the y pixel equals the y pixel that should be removed at the x row
            if im['width']*y+x == s[y]:
                setback = 1
            else:
                # print('SB', setback)
                set_pixel(result, x-setback, y, get_pixel(im, x, y))
    # print(result['pixels'])
    # print(len(result['pixels']))
    # print(im['height'])
    # print(im['width'])
    # print(setback)
    return result


def creative_filter(image, r_val, g_val, b_val):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0]*image['height']*image['width']
    }
    for x in range(image['width']):
        for y in range(image['height']):
            color = get_pixel(image, x, y)
            r = color[0]
            g = color[1]
            b = color[2]
            #v=round(.299×r+.587×g+.114×b)
            newcolor = r_val*r + g_val*g + b_val*b
            set_pixel(result, x, y, round(newcolor))
    return result

# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

def load_greyscale_image(filename):
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

def save_greyscale_image(image, filename, mode='PNG'):
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

    img = load_color_image('test_images/twocats.png')
    new_img = creative_filter(img, 1.25, 0.75, 0.75)
    save_color_image(new_img, 'big_red_cat.png')
    # pass
