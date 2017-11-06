#!/usr/bin/env python

import os
import sys
from wand.image import Image as Img, Color
try:
    import Image
except ImportError:
    from PIL import Image
import logging
from glob import glob
import datetime
import argparse
from dotenv import find_dotenv, load_dotenv


class Args():
    
    def __init__(self):
        pass

    def setup_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--start_index', type=int, dest="start_index", default=0)
        parser.add_argument('--batch_size', type=int, dest="batch_size", default=100)
        parser.parse_args(namespace=self)


def find_files_abs(rootdir: str) -> list:
    file_paths = []
    for folder, subs, files in os.walk(rootdir):
        for filename in files:
            file_paths.append(os.path.abspath(os.path.join(folder, filename)))
    return file_paths


def save_pdf_2_png(filename, output_path, resolution=300):
    all_pages = Img(filename=filename, resolution=resolution)
    for i, page in enumerate(all_pages.sequence):
        with Img(page) as img:
            img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = '{}_{:0>3}.png'.format(image_filename, i)
            image_filename = os.path.join(output_path, image_filename)

            img.save(filename=image_filename)
    return None


def main(args: Args):
    pdf_paths = find_files_abs(pdf_rootdir)
    if (args.start_index is not None):
        # starting where we left off - should be an optional argument
        logger.info("starting with path: {} at index: {}".format(pdf_paths[args.start_index], args.start_index))

    for path in pdf_paths[args.start_index:(args.start_index + args.batch_size)]:
        try:
            logger.info("processing {}".format(path))
            save_pdf_2_png(path, img_rootdir)
            logger.info("done processing {}".format(path))
        except:
            logger.warning("could not process file {}: {}".format(path, sys.exc_info()[0]))


if __name__ == "__main__":
    # load dotenv
    load_dotenv(find_dotenv())

    # set globals
    project_dir = os.environ.get("project_dir")
    img_rootdir = os.path.join(project_dir, os.environ.get('img_dir'))
    args = Args()
    args.setup_args()

    # setup logging
    FORMAT = '%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s'
    log_path = os.path.join(project_dir, os.environ.get['log_dir'])
    file_name = 'pdf_2_png_jfk.log'
    logging.basicConfig(format=FORMAT, handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(os.path.join(log_path, file_name))])
    logger = logging.getLogger()
    logger.setLevel("INFO")

    main(args)
