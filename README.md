# axintdata-extract
Tool to extract data from AxintData folder in DRN experiment

## What is does
Takes a bunch of axintdata and generates a bunch of CSV files regrouping all sensor data either per date or per sensor

## Instructions
Set following parameters at the top of the file:
- ANDRA_DATA_ORIGIN: localisation of the data to treat
- EXTRACT_LIST: localisation of the list of dates to extract
- OUTPUT_FOLDER: localisation of the folder for all outputed csv files
- in main (uncomment) lines for output_CSV depending on the data needed (sorted by either date or sensor)

### Extractlist
Extractlist should be formatted as follows:
- One date per line
- Date with format: DD/MM/AAAA hhH (e.g. 03/01/2019 13H)

## Licence
The MIT License (MIT)

Copyright (c) 2019 Thomas Brichart

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
