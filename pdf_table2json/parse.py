import pdf_table2json.converter as converter
import json

# PDF 파일 경로
# path = ""
path = ""
result = converter.main(path)

print(result)