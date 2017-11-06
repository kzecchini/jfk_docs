#!/usr/bin/env python

# This script is necessary because ImageMagick was creating hundreds of gigs
# of memory in the temp directory while running a long script for conversion. # Instead we run smaller batches and clean the temp directory inbetween runs.

import os
import click
from glob import glob
import logging
import sys
from pdf_2_png_jfk import find_files_abs
from dotenv import find_dotenv, load_dotenv


def cleanup_temp(base_path, file_wildcard):
    to_delete = glob(os.path.join(base_path, file_wildcard))
    if len(to_delete) > 0:
        for f in to_delete:
            os.remove(f)
            logging.info("removed temp directory: {}".format(f))
    return None


@click.command()
@click.option('--index', type=click.INT, default=0)
@click.option('--batch_size', type=click.INT, default=100)
def main(index, batch_size):
    num_files = len(find_files_abs(pdf_dir))
    
    while (index < num_files):
        cleanup_temp(tmp_rootdir, "magick-*")
        if (index + batch_size) > num_files:
            index = num_files
        else:
            index = index + batch_size
        sys.exit(0)
        os.system("activate tensorflow && python {} --start_index {} --batch_size {}".format("C:\\Users\\kzecchini\\deep_learning\\scripts\\pdf_2_png_jfk.py", index, batch_size))


if __name__ == "__main__":
    # load dotenv
    load_dotenv(find_dotenv())
    project_dir = os.environ.get("project_dir")
    tmp_rootdir = os.environ.get("tmp_dir")
    pdf_dir = os.path.join(project_dir, os.environ.get("pdf_dir"))

    # setup logging
    FORMAT = '%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s'
    log_path = os.path.join(project_dir, os.environ.get("log_dir"))
    file_name = 'scheduled_job.log'
    logging.basicConfig(format=FORMAT, handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(os.path.join(log_path, file_name))])
    logger = logging.getLogger()
    logger.setLevel("INFO")

    main()
