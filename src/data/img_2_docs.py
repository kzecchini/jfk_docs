#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytesseract
try:
    import Image
except ImportError:
    from PIL import Image
from pdf_2_png_jfk import find_files_abs
import pickle
import os
import logging
import sys
from dotenv import find_dotenv, load_dotenv
import click

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'


def group_by_doc_id(img_paths: list) -> list:
    prev_path = img_paths[0]
    prev_doc_id = os.path.split(prev_path)[1].split("_")[0]
    new_paths = []
    current_id_pages = [prev_path]
    for path in img_paths[1:]:
        filename = os.path.split(path)[1]
        doc_id, page_ext = filename.split("_")
        page = page_ext.split(".")[0]
        if (doc_id == prev_doc_id):
            current_id_pages.append(path)
        else:
            new_paths.append(current_id_pages)
            current_id_pages = [path]
        prev_doc_id = doc_id
    return new_paths


def create_document(doc_id_pages: list) -> dict:
    document = u''
    doc_id = os.path.split(doc_id_pages[0])[1].split("_")[0]
    for doc_page in doc_id_pages:
        page = os.path.split(doc_id_pages[doc_id_pages.index(doc_page)])[1].split("_")[1].split(".")[0]
        try:
            # OCR with pytesseract
            logger.info("processing doc_id: {} at page: {}".format(doc_id, page))
            img_string = pytesseract.image_to_string(Image.open(doc_page))
            # append pages in document with a newline
            if document == u'':
                document = document + img_string
            else:
                document = document + u"\n" + img_string
        except:
            logger.warning("could not process document_id: {} at page: {} - {}".format(doc_id, page, sys.exc_info()[0]))
    return {doc_id: document}


@click.command()
@click.option('--batch_size', type=click.INT, default=500)
def main(batch_size):
    img_paths = find_files_abs(img_rootdir)
    grouped_img_paths = group_by_doc_id(img_paths)

    for i in range(0, len(grouped_img_paths), batch_size):
        documents = {}
        for doc_id_pages in grouped_img_paths[i:i + batch_size]:
            doc_id = os.path.split(doc_id_pages[0])[1].split("_")[0]
            try:
                logger.info("processing doc_id: {}".format(doc_id))
                documents.update(create_document(doc_id_pages))
            except Exception as inst:
                logger.warning("could not process doc_id {}: {}".format(doc_id, sys.exc_info()[0]))
        logger.info("saving to pkl file: {}".format(pickle_file))
        with open(pickle_file, "wb") as f:
            pickle.dump(documents, f)
        break


if __name__ == "__main__":
    # load dotenv
    load_dotenv(find_dotenv())
    
    # set globals
    project_dir = os.environ.get("project_dir")
    img_rootdir = os.path.join(project_dir, os.environ.get('img_dir'))
    pkl_path = os.path.join(project_dir, os.environ.get('pkl_dir'))
    pickle_file = os.path.join(pkl_path, os.environ.get("pkl_file"))
    
    # setup logging
    FORMAT = '%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s'
    log_path = os.path.join(project_dir, os.environ.get('log_dir'))
    file_name = 'img_2_docs.log'
    logging.basicConfig(format=FORMAT, handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(os.path.join(log_path, file_name))])
    logger = logging.getLogger()
    logger.setLevel("INFO")

    main()
