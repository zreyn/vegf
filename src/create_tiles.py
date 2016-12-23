import openslide
import numpy as np
import mahotas as mh
import matplotlib
import os
from PIL import Image

# for S3 interaction
from boto.s3.connection import S3Connection
from boto.s3.key import Key

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


def create_and_upload_tiles(slide, slide_name, s3_bucket, tile_size=(64,64), level=0, temp_file='../data/temp.tiff'):
    '''
    This function breaks an openslide slide into tiles, discards empty tiles (just blank slide area),
    and uploads the tiles to the given s3 bucket.

    INPUT:  slide - in openslide format
            s3_bucket - bucket to store the resulting tiles
            tile_size - size of resulting tiles as a tuple (width,height)
            level - resolution level (0=max)
    OUTPUT: success/failure of whether putting tiles in s3 bucket
    '''

    dimensions = slide.dimensions # (width, height)
    temp_tile_file = os.path.join(os.path.dirname(__file__),temp_file)

    print 'creating', (dimensions[0]/tile_size[0]) * (dimensions[1]/tile_size[1]), 'tiles for slide', slide_name

    i = 0
    for x in xrange(0, dimensions[0], tile_size[0]):
        for y in xrange(0, dimensions[1], tile_size[1]):

            # create the tile (read_region takes location (upper left pixel), level, and size)
            tile = slide.read_region((x,y), level, tile_size)

            # don't save blank tiles
            if not is_empty(tile):

                # save the file locally temporarily
                tile.save(temp_tile_file, "TIFF")

                # upload to s3 (skip it if it already exists)
                k = Key(s3_bucket)
                k.key = 'tiles/slide_' + slide_name + '_' + '{:06d}'.format(i) + '.tiff'
                if not s3_bucket.get_key(k.key):
                    k.set_contents_from_filename(temp_tile_file)

            # update the tile num
            i+=1

            if i%1000==0:
                print i

    return

def main():

    conn = S3Connection()
    bucket = conn.get_bucket('vegf')

    # get all the slides from the bucket
    slide_names = []
    for key in bucket.list():
        if key.name.endswith('.svs'):
            slide_names.append(key.name)

    temp_slide_file = os.path.join(os.path.dirname(__file__),'../data/temp.svs')

    # open each slide
    for s3_key in slide_names:

        # save the file to a temporary local file
        k = bucket.get_key(s3_key)
        k.get_contents_to_filename(temp_slide_file)

        # open it with openslide
        slide = openslide.OpenSlide(temp_slide_file)

        # break the slide into tiles and save them to s3
        create_and_upload_tiles(slide, s3_key[:-4], bucket)


if __name__ == '__main__':
    main()
