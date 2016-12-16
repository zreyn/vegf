Author: Zane Reynolds (@zreyn)
Date: November 2016

Evan's: https://github.com/coradek/CNW_Wildlife_Identification/blob/master/src/feature_extractor.py

## TODO
* Create the tiles for all of the images, store them in an S3 bucket
* Feature extraction -  Inception-v3 from TensorFlow inspired by: http://www.kernix.com/blog/image-classification-with-a-pre-trained-deep-neural-network_p11
  ** Read the tiles from S3
  ** Define computation graph in TensorFlow
  ** Run the pre-trained CNN on each tile and save out the next-to-last layer as features
* Define distance metric
* Create distance matrix
* Heirarchical clustering


Install:
* pip install tensorflow
* python src/classify_image.py --model_dir model/imagenet
* add environment variables:
  AWS_ACCESS_KEY_ID - Your AWS Access Key ID
  AWS_SECRET_ACCESS_KEY - Your AWS Secret Access Key
