# pdf-table-extract
Extract tables data from pdf files To JSON

- Locate the table with oepncv and read the contents with a text reader (Your table should be blocked by a border)
- (If you don't have a border, add a border through adjustment)

- Currently, only the basic table is supported. (Supports only tables with horizontal headers)

    | Header 1 | Header 2 | Header 3 |
    |:--------:|:--------:|:--------:|
    |   cel1   |   cel2   |   cel3   |
    |   cel1   |   cel2   |   cel3   |
    |   cel1   |   cel2   |   cel3   |

- The pdf must be readable by a text reader. Drag on pdf to see if the text is captured

## Installation
- Rquired Python >= 3.8
- install with pip
```
pip install pdf-table2json
```

## Example
#### import
```py
import pdf_table2json

```

#### CLI
```py
python a.py -i "pdf_path/pdf_name.pdf" -o "output_path/"
```

#### Colab
[![Open In Colab](https://colab.research.google.com/github/yousojeong/pdf-table2json/blob/main/colab_example.ipynb)

## License
- GPL-3.0 license

## Contact
- [Reporting a bug](https://github.com/yousojeong/pdf-table-extract/issues)
- [@yousojeong](https://github.com/yousojeong)
