import pdf_table2json.converter as converter
import json

path = "path/name.pdf"
result = converter.main(path, json_file_out=True, image_file_out=True)

print(result)