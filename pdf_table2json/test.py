import pdf_table2json.converter as converter

path = "PATH/PDF_NAME.pdf"
result = converter.main(path)

print("----------------------------------")
print(result)