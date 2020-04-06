from __future__ import absolute_import

import os.path
from pathlib import Path
import sys

from ocrd_modelfactory import page_from_file
from ocrd_models.ocrd_page_generateds import parse
from ocrd_models.ocrd_page import to_xml

def update_points(points):
    points = points.split(" ")
    for idx, point in enumerate(points):
        if "-" in point:
            points[idx] = "0,0"
        else:
            points[idx] = point
    return " ".join(points)

def negative2zero(inputfile, outputfile):
    print("Setting negative coords to zero..")
    pcgts = parse(inputfile, silence=True)
    page = pcgts.get_Page()
    for attr in dir(page):
        if "get_" in attr and "Region" in attr:
            for regiondata in getattr(page,attr)():
                if attr == "get_TextRegion":
                    for textline in regiondata.get_TextLine():
                        textcoords = textline.get_Coords()
                        textcoords.set_points(update_points(textcoords.get_points()))
                regcoords = regiondata.get_Coords()
                regcoords.set_points(update_points(regcoords.get_points()))
    content = to_xml(pcgts)
    with open(outputfile,"w") as fout:
        fout.write(content)
if __name__=="__main__":
	negative2zero(sys.argv[1],sys.argv[2])
