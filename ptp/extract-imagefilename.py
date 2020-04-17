from __future__ import absolute_import

import sys

from ocrd_models.ocrd_page_generateds import parse

def get_imagefilename(inputfile):
    pcgts = parse(inputfile, silence=True)
    page = pcgts.get_Page()
    print(page.get_imageFilename())

if __name__== "__main__":
    get_imagefilename(sys.argv[1])
