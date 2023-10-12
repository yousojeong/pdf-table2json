import converter
import converter_2
import json

path = "path/name.pdf"
# result = converter.main(path, json_file_out=True, image_file_out=True)
result = converter_2.main(path, json_file_out=True, image_file_out=True)

print(result)