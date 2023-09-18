import os
import shutil
import cv2
import numpy as np
import json
import argparse
import re

import fitz  # PyMuPDF # text extractor
# from . import util  # package # utf-8
import util  # package # utf-8


def f_remove_watermark(image, target_color):
    diff = np.abs(image - target_color)
    mask = np.all(diff <= 20, axis=-1)
    image[mask] = [255, 255, 255]

    return image


def f_add_border_lines(image):
    lower_color = np.array([230, 230, 230])
    upper_color = np.array([230, 230, 230])
    mask = cv2.inRange(image, lower_color, upper_color)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    border_thickness = 2
    border_color = (0, 0, 0) 

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w >= 1000: 
            cv2.rectangle(image, (x, y), (x + w, y + h), border_color, border_thickness)

    return image


def f_process_list(input_list):
    result_list = []
    current_group = []
    prev_length = None

    for item in input_list:
        current_length = len(item)

        if prev_length is None:
            prev_length = current_length
            current_group = [item]
        elif prev_length == current_length:
            current_group.append(item)
        else:
            result_list.append(current_group)
            current_group = [item]
            prev_length = current_length

    if current_group:
        result_list.append(current_group)

    
    return result_list


def f_test(result_list):
    print("==========================")
    print(result_list)


def f_format_conversion(total_data_list):
    final_result = []

    for data in total_data_list:
        all_columns = [item['columns'] for item in data]

        for item in all_columns:
            if item and len(item) > 0:
                
                if len(item) == 1:
                    result = [{'th': data[0] for data in item}]
                    final_result.extend(result)
                else:
                    result = []

                    header = item[0]

                    for item in item[1:]:
                        data_dict = {}
                        for i, value in enumerate(item):
                            key = header[i]
                            data_dict[key] = value
                        result.append(data_dict)

                    final_result.extend(result)

    return final_result


# PDF TO Image
def f_convert_pdf_to_images(pdf_path, output_dir):
    pdf_document = fitz.open(pdf_path)

    os.makedirs(output_dir, exist_ok=True)
    print(output_dir)

    image_paths = []

    for page_number in range(pdf_document.page_count-1):
        page = pdf_document[page_number]
        pixmap = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # DPI

        image_path = os.path.join(output_dir, f"page_{page_number + 1}.png")
        pixmap.save(image_path, "png")
        image_paths.append(image_path)

        print(f"Page {page_number + 1} converted to image: {image_path}")

    return image_paths, pdf_document, page_number 


def path_parse(input_pdf_path):
    dir_path, name_extension = os.path.split(input_pdf_path)
    name, _ = os.path.splitext(name_extension)

    return dir_path, name_extension, name


def filter_characters(input_string):
    characters_to_exclude = ['열\n', '열 \n', '람\n', '람 \n', '용\n', '용 \n', '열 람\n', '열 람 \n', '람 용\n', '람 용 \n', '열 람 용\n', '열 람 용 \n', '열람\n', '열람 \n', '람용\n', '람용 \n', '열람용\n', '열람용 \n']
    pattern = '|'.join(map(re.escape, characters_to_exclude))
    filtered_string = re.sub(pattern, '', input_string)

    return filtered_string


def main(input_pdf_path, output_path=None, json_file_out=None, processed_img_out=None):

    if output_path is None:
        output_path = input_pdf_path

    dir_path, name_extension, name = path_parse(input_pdf_path)
    dir_path_out, _, _ = path_parse(output_path)
    
    pdf_path = input_pdf_path
    pdf_name = name_extension
    output_dir = dir_path_out + "/" + name + "/" 

    if processed_img_out:
        line_image_dir =  output_dir + "/processed_images/"
        os.makedirs(line_image_dir, exist_ok=True)
    
    image_paths, pdf_document, page_number = f_convert_pdf_to_images(pdf_path, output_dir)

    total_data_list = []

    for page_number, image_path in enumerate(image_paths, start=0):

        image = util.utf_imread(image_path)
        
        image_height, image_width, _ = image.shape

        #precessed_image = f_image_preocessing(image)

        added_border_image = f_add_border_lines(image)

        watermark_color_1 = (213, 213, 213)  # D5D5D5
        watermark_color_2 = (224, 224, 224)  # E0E0E0

        removed_watermark_image = f_remove_watermark(added_border_image, watermark_color_1)
        removed_watermark_image = f_remove_watermark(removed_watermark_image, watermark_color_2)

        gray_image = cv2.cvtColor(removed_watermark_image, cv2.COLOR_BGR2GRAY)

        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        _, thresholded_image = cv2.threshold(blurred_image, 200, 255, cv2.THRESH_BINARY)

        edges = cv2.Canny(thresholded_image, threshold1=50, threshold2=150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        tables = []

        line_image = image.copy()

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 1000 and h > 100: 
                tables.append((x, y, w, h))

        tables.reverse()

        pdf_page = pdf_document[page_number]

        pdf_page_width = pdf_page.rect.width
        pdf_page_height = pdf_page.rect.height

        prev_column_count = None
        row_list = []

        for table_number, (x, y, w, h) in enumerate(tables, start=1):

            if table_number == 1:
                new_list = []

            roi = thresholded_image[y:y + h, x:x + w]
            cell_contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cell_number = 1

            cell_rows = {}

            cell_contours = sorted(cell_contours, key=lambda c: cv2.boundingRect(c)[1])

            for idx, contour in enumerate(cell_contours):
                x_cell, y_cell, w_cell, h_cell = cv2.boundingRect(contour)
                x_global, y_global = x + x_cell, y + y_cell

                if w == w_cell or h == h_cell or w_cell <= 10 or h_cell <= 10:
                    continue

                cv2.rectangle(line_image, (x_global, y_global), (x_global + w_cell, y_global + h_cell), (0, 255, 0), 2)
                cv2.putText(line_image, f"[T_{table_number} C_{cell_number}]", (x_global + w_cell // 2, y_global + h_cell // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

                pdf_x1 = x_global * (pdf_page_width / image_width)
                pdf_y1 = y_global * (pdf_page_height / image_height)
                pdf_x2 = (x_global + w_cell) * (pdf_page_width / image_width)
                pdf_y2 = (y_global + h_cell) * (pdf_page_height / image_height)

                text = pdf_page.get_text("text", clip=(pdf_x1, pdf_y1, pdf_x2, pdf_y2))
                text = filter_characters(text) # 텍스트 필터링

                if y_global not in cell_rows:
                    cell_rows[y_global] = []
                cell_rows[y_global].append({
                    "x": x_global,
                    "y": y_global,
                    "width": w_cell,
                    "height": h_cell,
                    "text": text.strip()
                })

                cell_number += 1

                if idx == 0:
                    new_list = []

                new_list = f_process_list(list(cell_rows.values()))
            #print(new_list)

            #f_test(reversed(new_list))

            '''
            for idx, group in enumerate(new_list):
                
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                if(len(group)!=0):
                    height_values = [item["height"] for row in group for item in row]
                    print(height_values)

                    first_value = height_values[0]
                    check_list = [i for i, value in enumerate(height_values) if value != first_value]
                    print(check_list)

                    group = [list(reversed())]

                else :
                    print("[]")
            '''

            # print(new_list)

            data_list = []
            for idx, group in enumerate(new_list):

                '''
                # 작업하던 부분 
                # 위에 주석 부분은 height 비교해서 check_list 값 만드는 거

                for sublist in group:
                    reversed_dict_list = list(reversed(sublist))  # 리스트를 뒤집음
                    #print(reversed_dict_list)
                    #for data in reversed_dict_list:
                    #    print(data)

                    row_length = len(reversed_dict_list[0])
                    grouped_values = [list(reversed_dict_list[i:i + row_length]) for i in range(0, len(reversed_dict_list), row_length)]
                    # print("----------------------------")
                    # print(grouped_values)
                    data_list.append(grouped_values)
                    # data_list.append({"row": str(idx), "columns": grouped_values})
                '''

                text_values = [item["text"] for row in group for item in row]
                row_length = len(group[0])
                grouped_text_values = [list(reversed(text_values[i:i + row_length])) for i in range(0, len(text_values), row_length)]
                data_list.append({"row": str(idx), "columns": grouped_text_values})
                #print(type(data_list))

            # print(data_list)
            json_data = json.dumps(data_list, indent=4, ensure_ascii=False)
            #print("------------------------------------------------------")
            #print(json_data)
            total_data_list.append(data_list)
            #print(total_data_list)

            #prev_column_count = None
            #row_list = []

        image = None

        if processed_img_out:
            f_make_processed_img(line_image_dir, page_number, line_image)

    # total_data_list = f_format_conversion(total_data_list)

    # print(total_data_list)

    json_data_combined = json.dumps(total_data_list, indent=4, ensure_ascii=False)
    
    if json_file_out:
        f_make_json_file(json_data_combined, output_dir, pdf_name)

    pdf_document.close()

    # f_delete_directory(output_dir)

    return json_data_combined


def f_make_processed_img(output_dir, page_number, processed_image):
    line_image_path = os.path.join(output_dir, f"processed_image_{page_number + 1}.png")
    util.utf_imwrite(line_image_path, processed_image)
    print(f"Line image for page {page_number + 1} saved to {line_image_path}")


def f_make_json_file(data, output_dir, pdf_name):
    print(output_dir)
    combined_output_path = output_dir + pdf_name + ".json"
    with open(combined_output_path, "w", encoding="utf-8") as combined_output_file:
        combined_output_file.write(data)
    print("JSON data saved to", combined_output_path)


def f_delete_directory(path):
    try:
        shutil.rmtree(path)
        print(f"Removed directory : {path} ")
    except Exception as e:
        print(f"Error removing directory: {str(e)}")

        
def is_valid_pdf(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()
    return file_extension == '.pdf'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract tables from PDF files To JSON data")
    parser.add_argument("-i", "--input", required=True, help="Input PDF file path")
    parser.add_argument("-o", "--output", default=None, help="[Optional] Output directory to save the extracted datas")
    parser.add_argument("-j", "--json_file", default=None, help="[Optional] JSON Data file out")
    parser.add_argument("-p", "--image", default=None, help="[Optional] Processed Image file out")
    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output
    json_file_out = args.json_file
    processed_img_out = args.image

    if not is_valid_pdf(input_path):
        print("Input file is not a valid PDF file.")
    elif not (output_dir or json_file_out or processed_img_out):
        main(input_path, output_dir, None, None)
        print("No output path specified. PDF will not be saved.")
    else:
        main(input_path, output_dir, json_file_out, processed_img_out)
