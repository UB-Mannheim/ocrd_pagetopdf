# ocrd-pagetopdf

> OCR-D wrapper for prima-pagetopdf

Transforms all PAGE-XML+IMG to PDF with text

### Requirements

- OCR-D Workflow
- JAVA Runtime

### Start the process

    $ ocrd-pagetopdf -I PAGE-XML-FOLDER,IMG-FOLDER -O PDF-FOLDER -p '{"text-source":"W"}'

Run the script and create an PDF with text based on wordlevel

If "java.lang.NullPointerException" appears, try (a little workaround) and set negative coordinates to zero:

    $ ocrd-pagetopdf -I PAGE-XML-FOLDER,IMG-FOLDER -O PDF-FOLDER -p '{"text-source":"W","negative2zero":true}'

Please note that the standard displayed font does not support utf-8 completely, please reset the font:

    $ ocrd-pagetopdf -I PAGE-XML-FOLDER,IMG-FOLDER -O PDF-FOLDER -p '{"text-source":"W","font":"/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"}'
