from __future__ import absolute_import

from pathlib import Path
import sys
import subprocess

from ocrd_models import OcrdMets
from ocrd_utils.logging import getLogger, initLogging
from atomicwrites import atomic_write
from ocrd_models.constants import NAMESPACES as NS

def get_metadata(mets):
    title = mets._tree.getroot().find('.//mods:title', NS)
    subtitle = mets._tree.getroot().find('.//mods:subtitle', NS)
    title = title.text if title is not None else ""
    title += "Subtitle: "+subtitle.text if subtitle else ""
    publisher = mets._tree.getroot().find('.//mods:publisher', NS)
    author = mets._tree.getroot().find('.//mods:creator', NS)
    return {'Author':author.text if author is not None else "",
            'Title': title,
            'Keywords': publisher.text+" (Publisher)" if publisher is not None else ""}

def read_from_mets(metsfile, filegrp, outputfile, pagelabel='pageId', overwrite=False):
    overwrite = overwrite == 'true'
    mets = OcrdMets(filename=metsfile)
    inputfiles = []
    pagelabels = []
    metadata = get_metadata(mets)
    for f in mets.find_files(mimetype='application/pdf', fileGrp=filegrp):
        # ignore multipaged pdfs
        if f.pageId:
            inputfiles.append(f.local_filename)
            if pagelabel != "pagenumber":
                pagelabels.append(getattr(f, pagelabel,""))
    if inputfiles:
        if not pdfmerge(inputfiles, outputfile, pagelabels=pagelabels, metadata=metadata):
            mets.add_file(filegrp, mimetype='application/pdf', ID=outputfile, url=str(Path(filegrp).joinpath(outputfile+'.pdf')), force=overwrite)
            with atomic_write(metsfile, overwrite=True) as f:
                f.write(mets.to_xml(xmllint=True).decode('utf-8'))
    return None

def create_pdfmarks(pdfdir, pagelabels=None, metadata=None):
    pdfmarks = pdfdir.joinpath('pdfmarks.ps')
    with pdfmarks.open('w') as marks:
        if metadata:
            marks.write("[ ")
            for kwarg in ['Title', 'Author', 'Keywords']:
                if kwarg in metadata:
                    marks.write(f"/{kwarg} ({metadata[kwarg]})\n")
            marks.write("/DOCINFO pdfmark\n")
        if pagelabels:
            marks.write("[{Catalog} <<\n\
                    /PageLabels <<\n\
                    /Nums [\n")
            for idx, pagelabel in enumerate(pagelabels):
                #marks.write(f"1 << /S /D /St 10>>\n")
                marks.write(f"{idx} << /P ({pagelabel}) >>\n")
            marks.write("] >> >> /PUT pdfmark")
    return pdfmarks

def pdfmerge(inputfiles, outputfile, pagelabels=None, metadata=None, store_tmp=False):
    log = getLogger('processor.pagetopdf')
    if isinstance(inputfiles, str):
        inputfiles = inputfiles.split(",")
    log.info("Merging PDFs..")
    pdfmarks = None
    try:
        pdfdir = Path(inputfiles[0]).parent
        pdfmarks = create_pdfmarks(pdfdir, pagelabels, metadata)
        stdout = subprocess.check_output(
            f"gs -sDEVICE=pdfwrite \
            -dNOPAUSE -dBATCH -dSAFER \
            -sOutputFile={pdfdir.joinpath(outputfile+'.pdf')} \
            {' '.join(inputfiles)}\
            {pdfmarks}", shell=True,
            stderr=subprocess.STDOUT,
            # give us str instead of bytes:
            universal_newlines=True)
        for line in stdout.split('\n'):
            log.debug(line)
        return True
    except Exception:
        log.exception(f"Couldn't merge the pdf files.")
        return False
    finally:
        if pdfmarks and not store_tmp:
            pdfmarks.unlink()

if __name__=='__main__':
    initLogging()
    read_from_mets(*sys.argv[1:])
