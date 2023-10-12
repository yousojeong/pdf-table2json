# pdf-table2json
Extract tables data from pdf files To JSON

- Locate the table with oepncv and read the contents with a text reader (Your table should be blocked by a border)
- (If you don't have a border, add a border through adjustment)
- The pdf must be readable by a text reader. Drag on pdf to see if the text is captured.
- Check version before install
    - [1.0.1](#version-101) : Only the basic table is supported
    - [2.0.1](#version-201-or-higher) : Handling tables with separate headers or cells [(example)](#version-201-or-higher)

## Current Status(Change the values ​​if adjustments are needed)
- Finds a table with a horizontal length greater than 1000 and a height greater than 100.
- Cells are excluded if their width or height is equal to the width or height of the table, or if the width or height of the cell is less than 10.
- Adding border lines to areas with a color of (230, 230, 230) and a width of 1000 or more to recognize them as table regions.
- Removing watermark images with a color of (213, 213, 213 == #D5D5D5).
- The specific string list is removed from the PDF text for the purpose of removing text watermarks (Currently empty).

## Installation
- Rquired Python >= 3.8
- install with pip
```py
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



## version-1.0.1
- Only the basic table is supported. (Supports only tables with horizontal headers).
- The number of headers and the number of cells must be the same
- Example Table
    | Header 1 | Header 2 | Header 3 |
    |:--------:|:--------:|:--------:|
    |   cel1   |   cel2   |   cel3   |
    |   cel1   |   cel2   |   cel3   |
    |   cel1   |   cel2   |   cel3   |

- Example
    - `converter.py`
    
    ```py
    import pdf_table2json.converter as converter

    path = "PATH/PDF_NAME.pdf"
    result = converter.main(path, json_file_out=True, image_file_out=True)
    print(result)
    ```

## version-2.0.1 or Higher
1. Tables in general format that can be processed in version 1.0.1 can be processed.
    - Example Table
        | Header 1 | Header 2 | Header 3 |
        |:--------:|:--------:|:--------:|
        |   cel1   |   cel2   |   cel3   |
        |   cel1   |   cel2   |   cel3   |
        |   cel1   |   cel2   |   cel3   |

2. Table with separated header and subheader
    - Example Table
        <table>
        <tr>
        <th rowspan="2">Header 1</th>
        <th style="text-align:center" colspan="2">Header 2</th>
        </tr>
        <tr>
        <th>Sub Header 1</th>
        <th>Sub Header 2</th>
        </tr>
        <tr>
        <td>cel1</td>
        <td>cel2</td>
        <td>cel3</td>
        </tr>
        <tr>
        <td>cel1</td>
        <td>cel2</td>
        <td>cel3</td>
        </tr>
        <tr>
        <td>cel1</td>
        <td>cel2</td>
        <td>cel3</td>
        </tr>
        </table>

    - Output
        - Delete separated parent header, use child header

            ```
            Header 1 : cel1
            Sub Header 1 : cel2
            Sub Header 2 : cel3
            ```

3. Tables with columns separated, except for the first cell
    - Example Table
        <table>
        <tr>
        <th>Header 1</th>
        <th>Header 2</th>
        <th>Header 3</th>
        </tr>
        <tr>
        <td>cel1</td>
        <td>cel2</td>
        <td>cel3</td>
        </tr>
        <tr>
        <td rowspan=2>cel1</td>
        <td>cel2-1</td>
        <td>cel3-1</td>
        </tr>
        <tr>
        <td>cel2-2</td>
        <td>cel3-2</td>
        </tr>
        </table>

    - Output
        - Add to data in the top row (with "@")
            
            ```
            Header 1 : cel1
            Header 2 : cel2
            Header 3 : cel3
            Header 1 : cel1
            Header 2 : cel2-1@cel2-2
            Header 3 : cel3-1@cel3-2
            ```

- Use Example
    - `converter_2.py`

    ```py
    import pdf_table2json.converter_2 as converter_2

    path = "PATH/PDF_NAME.pdf"
    result = converter_2.main(path, json_file_out=True, image_file_out=True)
    print(result)
    ```



## License
- GPL-3.0 license

## Contact
- [Reporting a bug](https://github.com/yousojeong/pdf-table-extract/issues)
- [@yousojeong](https://github.com/yousojeong)

## Read Text From PDF library
- PyMuPDF [GitHub](https://github.com/pymupdf/PyMuPDF)