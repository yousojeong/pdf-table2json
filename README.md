# pdf-table-extract
Extract tables data from pdf files To JSON

- Locate the table with oepncv and read the contents with a text reader (Your table should be blocked by a border)
- (If you don't have a border, add a border through adjustment)

- Currently, only the basic table is supported. (Supports only tables with horizontal headers).
- The number of headers and the number of cells must be the same

    | Header 1 | Header 2 | Header 3 |
    |:--------:|:--------:|:--------:|
    |   cel1   |   cel2   |   cel3   |
    |   cel1   |   cel2   |   cel3   |
    |   cel1   |   cel2   |   cel3   |

- The pdf must be readable by a text reader. Drag on pdf to see if the text is captured.

## Current Status(Change the values ​​if adjustments are needed)
- Finds a table with a horizontal length greater than 1000 and a height greater than 100.
- Cells are excluded if their width or height is equal to the width or height of the table, or if the width or height of the cell is less than 10.
- Adding border lines to areas with a color of (230, 230, 230) and a width of 1000 or more to recognize them as table regions.
- Removing watermark images with a color of (213, 213, 213 == #D5D5D5).
- The specific string list is removed from the PDF text for the purpose of removing text watermarks (Currently empty).

## Installation
- Rquired Python >= 3.8
- install with pip
```
pip install pdf-table2json
```

## Example
#### import
```py
import pdf_table2json.converter as converter

path = "PATH/PDF_NAME.pdf"
result = converter.main(path, json_file_out=True, image_file_out=True)
print(result)
```

#### CLI
```py
python converter.py -i "pdf_path/pdf_name.pdf" [-j] [-o]
```
- "-i", "--input", required=True, help="[Required] Input PDF file path"
- "-j", "--json_file", action="store_true", help="[Optional] Create JSON Data file"
- "-o", "--image_file", action="store_true", help="[Optional] Save Image Data file"

#### Colab
[![Open In Colab](https://colab.research.google.com/github/yousojeong/pdf-table2json/blob/main/colab_example.ipynb)]

## License
- GPL-3.0 license

## Contact
- [Reporting a bug](https://github.com/yousojeong/pdf-table-extract/issues)
- [@yousojeong](https://github.com/yousojeong)

## Read Text From PDF library
- PyMuPDF [GitHub](https://github.com/pymupdf/PyMuPDF)