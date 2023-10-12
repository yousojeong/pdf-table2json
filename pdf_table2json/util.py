import numpy as np
import cv2
import os

# imread, imwrite utf-8 
def utf_imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

# imread, imwrite utf-8 
def utf_imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    

# Make Group
# ex) {"row": "", "groups" : [[],[]]}
# Group based on the number of items present in the same row
def f_group_list(input_list):
    
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


# Change format
# Return in dictionary form with 0 groups set to keys and the remaining values set to values
# ex) {"header":"data", "header":"data"}
# if the group has one value, create as {"th": ["",""]} for table name
def f_format_conversion(total_data_list):
    final_result = []

    for data in total_data_list:
        all_groups = [item['groups'] for item in data]
        for item in all_groups:
            if item and len(item) > 0:
                if len(item) == 1:
                    result = [{'th': data for data in item}]
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