from __future__ import absolute_import

import os.path
from pathlib import Path
import sys
import subprocess
import traceback

from ocrd_models import OcrdMets

def read_from_mets(metsfile, outputfile):
    mets = OcrdMets(filename=metsfile)
    inputfiles = []
    page_ids = []
    for f in mets.find_files(mimetype="application/pdf"):
        inputfiles.append(f.local_filename)
        page_ids.append(f.ID)
    if inputfiles:
        return pdfmerge(inputfiles, page_ids, outputfile)
    return None

def pdfmerge(inputfiles, page_ids, outputfile, metadata=None):
    if isinstance(inputfiles, str):
        inputfiles = inputfiles.split(",")
    print("Merging PDFs..")
    try:
        pdfdir = Path(inputfiles[0]).parent
        with open(pdfdir.joinpath("pdfmarks.ps"),"w") as marks:
            if metadata:
                marks.write("[ ")
                for kwarg in ["Title","Author","Keywords"]:
                    if kwarg in metadata:
                        marks.write(f"/{kwarg} ({metadata[kwarg]})\n")
                marks.write("/DOCINFO pdfmark\n")
            marks.write("[{Catalog} <<\n\
                        /PageLabels <<\n\
                        /Nums [\n")
            for idx, page_id in enumerate(page_ids):
                #marks.write(f"1 << /S /D /St 10>>\n")
                marks.write(f"{idx} << /P ({page_id}) >>\n")
            marks.write("] >> >> /PUT pdfmark")
        subprocess.Popen(f"gs -sDEVICE=pdfwrite \
                -dNOPAUSE -dBATCH -dSAFER \
                -sOutputFile={pdfdir.joinpath(outputfile+'.pdf')} \
                {' '.join(inputfiles)}\
                {pdfdir.joinpath('pdfmarks.ps')}", shell=True, stderr=subprocess.STDOUT)
    except Exception as ex:
        print(f"Couldn't merge the pdf files. Error: {ex}")
        traceback.print_exc(file=sys.stdout)

if __name__=="__main__":
    read_from_mets(sys.argv[1], sys.argv[2])
