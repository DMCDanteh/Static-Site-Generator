from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from gencontent import generate_page, generate_pages_recursive
import os
import shutil
import sys

def main():
    path_to_docs = "docs"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists(path_to_docs):
        shutil.rmtree(path_to_docs)
    os.mkdir(path_to_docs)
    copy_files_recursive("static", path_to_docs)
    generate_pages_recursive("content", "template.html", path_to_docs, basepath)

main()