

::
:: Loop through all files within the specified folder
::

FOR %%c in ("input\*.xml") DO (
  java -jar ..\PageToPdf.jar -xml "%%c" -image "input\%%~nc.png" -pdf "output\%%~nc.pdf" -text-source R -outlines L -font "..\data\AletheiaSans.ttf"
)