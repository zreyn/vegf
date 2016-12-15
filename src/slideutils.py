import openslide
import numpy as np
import mahotas as mh
import matplotlib
from PIL import Image

def show(pix):
    '''
    Takes a numpy array of pixels and shows it with matplotlib
    '''
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(pix, interpolation='nearest', aspect='equal')


'''
================================================================================
Tiling images
================================================================================
'''
def rgb2gray_invert(rgb):
    return 256 - np.dot(rgb[...,:3], [0.299, 0.587, 0.114]).astype('uint8')

def is_empty(img):
    pix = rgb2gray_invert(np.array(img)) # convert to gray scale and invert
    return np.sum(pix) < 60000  # 60K determined empirically

def create_and_save_tiles(slide_filename, tile_directory, tile_size=(64,64), level=0):
    '''
    Reads in a slide, breaks it into tiles, saves the non-empty tiles to the
    tile_directory.

    tile_size = (width, height)
    level = resolution_level (0 = full resolution)
    '''

    # read in the slide and get its dimensions
    slide = openslide.OpenSlide(slide_filename)
    dimensions = slide.dimensions

    # output status
    print 'creating', (dimensions[0]/tile_size[0]) * (dimensions[1]/tile_size[1]), \
        'tiles for slide', slide_num, '...'

    i = 0
    for x in xrange(0, dimensions[0], tile_size[0]):
        for y in xrange(0, dimensions[1], tile_size[1]):

            # create the tile (read_region takes location (upper left pixel), level, and size)
            tile = slide.read_region((x,y), level, tile_size)

            # create the filename and save the tile
            filename = 'data/tiles/slide_' + slide_names[slide_num] + '_' + '{:06d}'.format(i) + '.tiff'

            # don't save blank tiles
            if not is_empty(tile):
                tile.save(filename, "TIFF")

            # update the tile num
            i+=1

    print 'done.'



'''
================================================================================
Finding VEGF in images
================================================================================
'''
def reddish_mask(pix, blue_tolerance=10):
    '''
    Takes a numpy array of pixels in RGB or RGBA format and returns a 2-d boolean array indicating the red-dominant
    pixels within the specified blue tolerance.
    '''
    return (pix[:,:,0] > pix[:,:,1]) & (pix[:,:,0] > pix[:,:,2]-blue_tolerance)

def dark_mask(pix, thresh=200):
    '''
    Takes a numpy array of pixels in RGB or RGBA format and returns a 2-d boolean array indicating the pixels where
    each color value is lower than the given threshold.
    '''
    return (pix[:,:,0] < thresh) & (pix[:,:,1] < thresh) & (pix[:,:,2] < thresh)



def find_vegf(pix):
    '''
    Takes a numpy array of pixels and isolates the brown-ish pixels (i.e.
    red-dominant), which are associated with vegf in this dataset.  Returns
    the mask and percentage of pixels that are vegf.
    '''

    reddish = reddish_mask(pix)
    dark = dark_mask(pix)
    pct_vegf = float(sum(sum(reddish & dark))) / (reddish.shape[0]*reddish.shape[1])

    return pct_vegf, pix[reddish & dark]
