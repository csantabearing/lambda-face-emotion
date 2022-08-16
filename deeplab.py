import os
import cv2
import numpy as np
import tensorflow as tf
from icrawler.builtin import GoogleImageCrawler
from pymatting import estimate_foreground_ml, estimate_alpha_cf, blend


class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513

    def __init__(self, path):
        self.graph = tf.Graph()
        graph_def = tf.compat.v1.GraphDef.FromString(open(path, 'rb').read())
        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')
        self.sess = tf.compat.v1.Session(graph=self.graph)

    def get_mask(self, image):
        height, width = image.shape[:2]
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        return resized_image, seg_map, resize_ratio

    def transform(self, image, mask, query):
        if query != '':
            os.mkdir(query)
            google_crawler = GoogleImageCrawler(storage={'root_dir': f'./{query}'})
            google_crawler.crawl(keyword=query, max_num=1)
            background = cv2.imread(f'./{queryword}/000001.jpg')
        else:
            background = cv2.blur(image)
        if (mask > 0.9).sum():
            mask = estimate_alpha_cf(img / 255, mask)
        img = cv2.resize(image,)
        foreground = estimate_foreground_ml(image / 255, mask)
        new_img = blend(background / 255, foreground / 255, mask)
        return (255 * new_img).astype(np.uint8)
