import os
import re

import openslide
import tensorflow as tf
import tensorflow.python.platform
from tensorflow.python.platform import gfile
import numpy as np
import pandas as pd
import cPickle as pickle
from PIL import Image

from boto.s3.connection import S3Connection
from boto.s3.key import Key

'''
Inspired by:
KERNIX blog - Image classification with a pre-trained deep neural network
http://www.kernix.com/blog/image-classification-with-a-pre-trained-deep-neural-network_p11
'''

def create_graph():
    '''
    In TensorFlow, a graph describes the computations to be done,
    which are then executed in sessions.  Credit: KERNIX blog (see above)
    '''
    model_dir = '../model/imagenet'
    with gfile.FastGFile(os.path.join(
            model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def extract_features(df):
    '''
    augment a pandas df containing image file S3 keys (as 'key') with
    a pandas series of features
    '''

    temp_tiff = '../data/temp.tiff'
    temp_jpg = '../data/temp.jpg'
    nb_features = 2048
    features = np.empty((df.shape[0], nb_features))

    create_graph()

    with tf.Session() as sess:

        next_to_last_tensor = sess.graph.get_tensor_by_name('pool_3:0')

        for i,k in enumerate(df['key']):
            if (i % 100 == 0):
                print('Processing %s... (%s of %s)' % (k, i, df.shape[0]))

            # save the file locally
            key = bucket.get_key(k, validate=False)
            key.get_contents_to_filename(temp_tiff)

            # convert tiff to jpg
            try:
                im = Image.open(temp_tiff)
                im.thumbnail(im.size)
                im.save(temp_jpg, "JPEG", quality=100)
            except Exception, e:
                print e

            image_data = gfile.FastGFile(temp_jpg, 'rb').read()

            predictions = sess.run(next_to_last_tensor,
                                    {'DecodeJpeg/contents:0': image_data})
            features[i, :] = np.squeeze(predictions)

    return features

if __name__ == '__main__':

    # get the tile metadata dataframe from S3 and load it with pickle
    tile_df_filename = os.path.join(os.path.dirname(__file__), '../data/tiles_df.pkl')
    k = Key(bucket)
    k.key = 'tiles_df.pkl'
    k.set_contents_from_filename(tile_df_filename)
    with open(df_filename, 'r') as f:
        df = pickle.load(f)

    features = extract_features(df)
