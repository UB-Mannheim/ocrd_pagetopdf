# ocrd-pagetopdf

> OCR-D wrapper for prima-page-to-pdf

Transforms all PAGE-XML+IMG to PDF with text layer and (optionally) polygon outlines.

(Converts original images together with text and layout annotations of all pages in the PAGE input file group to PDF. The text is rendered as an overlay.)

### Requirements

- GNU `make`
- Python 3 with `pip` and `venv`
- [OCR-D](https://github.com/OCR-D/core)
- Java runtime (OpenJDK 8 works for [PageToPdf](https://github.com/PRImA-Research-Lab/prima-page-to-pdf/releases) 1.1.2)

### Installation

Once you have installed Java, make, Python, and set up your [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/), do:

    make deps # or: pip install ocrd
    make install # copies into PREFIX or VIRTUAL_ENV

### Usage

The command-line interface conforms to [OCR-D processor](https://ocr-d.de/en/spec/cli) specifications.

Assuming you have an [OCR-D workspace](https://ocr-d.de/en/user_guide#preparing-a-workspace) in your current working directory, simply do:

    ocrd-pagetopdf -I PAGE-FILGRP -O PDF-FILEGRP -p '{"textequiv_level" : "word"}'

This will run the script and create PDF files for each page with a text layer based on word-level annotations.

### FAQ

- `Illegal reflective access by com.itextpdf.text.io.ByteBufferRandomAccessSource$1 to method java.nio.DirectByteBuffer.cleaner()`
   If that appears, try installing OpenJDK 8.

- `java.lang.NullPointerException` 
  If that appears, try (a little workaround) and set negative coordinates to zero:
  
      ocrd-pagetopdf -I PAGE-FILGRP -O PDF-FILEGRP -p '{"textequiv_level" : "word", "negative2zero": true}'

- Some letters are illegible?
  Please note that the standard displayed font ([AletheiaSans.ttf](https://github.com/PRImA-Research-Lab/prima-aletheia-web/raw/master/war/aletheiasans-webfont.ttf)) does not support all Unicode glyphs. In case yours are missing, set a (monospace) Unicode font yourself:

      ocrd-pagetopdf -I PAGE-FILGRP -O PDF-FILEGRP -p '{"textequiv_level" : "word", "font": "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"}'
