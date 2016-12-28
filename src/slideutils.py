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
