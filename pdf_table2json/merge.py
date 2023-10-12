import json
try:
    from . import util
except ImportError:
    import util

# Compare the height value of index 0 of the first groups with the height values ​​of the remaining indexes, 
#   and if there are different values, it is assumed to be vertically divided.

# Subheader processing (Remove the upper header and connect the lower header to display.)
'''
ex) | th1 |     th2     |
    |     | sub1 | sub2 |  
'''
# If the header is divided as above and a subheader is created, it is sorted as follows
# >> 'th1', 'sub1', 'sub2'
# (removed 'th2')

def f_colspan(data):
    cnt = 0 
    total_list = []
    for item in data:

        check_list = []
        current_row = None
        before_column = None

        temp_list = []

        for entry in item:
            row = entry.get("row")
            groups = entry.get("groups")

            temp = []
            if row != current_row:
                current_row = row

                if((groups and len(groups) > 0) and (len(check_list)==0)):
                    check = False
                    before_column = groups[0]

                    first_column_value = groups[0]
                    height_values = [entry['height'] for entry in first_column_value]
                    first_height_values = height_values[0]
                    check_list =  [i for i, value in enumerate(height_values) if value != first_height_values]

                    res = [item for sublist in groups for item in sublist]
                    # res = [item['text'] for item in res]
                    # print(res)
                    
                else:
                    check = True
                    for index in check_list:
                        del before_column[index]
                        before_column[index:index] = groups[0]
                        res = before_column
                        # res = [item['text'] for item in before_column]
                        # print(res)

                    check_list=[]
                    
                temp.append(res)

            else :
                check = False
                res = [item for sublist in groups for item in sublist]
                # res = [item['text'] for item in res]
                # print(res)
                temp.append(res)

            if check:
                temp_list.pop()

            temp_list.extend(temp)


        temp_list = util.f_group_list(temp_list)
        data_list = []
        for sub in temp_list:
            data_list.append({"row:" : str(cnt), "groups": sub})
        total_list.append(data_list)

        cnt += 1 

    # total_list = json.dumps(total_list, indent=4, ensure_ascii=False)
    # print(total_list)
    return total_list



# The data in the first header is the same, separated by line breaks.
# Based on width, parent groups should have more cells than child groups.

'''
ex) | no |  th |
    | 1  |  a  |
    | -- | --- |
    |    |  b  |
    | 2  | --- |
    |    |  c  |
'''
# The data in the first header is the same, separated by line breaks.
# >> '1', 'a', '2', 'b@c'
# (Concatenate the following data with a delimiter "@")
# (The first value must not be divided)
def f_rowspan(data):
    before_groups = None
    total_list = []

    for item in data:
        temp_list = []

        for group in item:
            check = False
            current_groups = group['groups']

            text_values = []
            for group in current_groups:
                t = []
                for item in group:
                    t.append(item['text'])
                text_values.append(t)

            if before_groups is None:
                before_groups = current_groups
            else:
                if len(before_groups[0]) > len(current_groups[0]):

                    before_width = [item['width'] for item in before_groups[0]]
                    current_width = [item['width'] for item in current_groups[0]]

                    indices = []
                    used_indices = set()
                    for item in current_width:
                        for index, value in enumerate(before_width):
                            if index not in used_indices and item == value:
                                indices.append(index)
                                used_indices.add(index)

                    if len(indices) != 0:
                        check = True
                        last_list = before_groups[-1] 
                        A = [item['text'] for item in last_list]  
                        b_list = current_groups[0]
                        B = [item['text'] for item in b_list]  

                        result_list = A[:]
                        for i in range(len(indices)):
                            a_index = indices[i]
                            b_index = i
                            result_list[a_index] += "@" + B[b_index]

                        temp_list.pop(-1)
                        temp_list.append(result_list)

                before_groups = current_groups

            if not check:
                temp_list.extend(text_values)
                
        temp_list = util.f_group_list(temp_list)
        data_list = []
        for sub in temp_list:
            data_list.append({"row:" : str(0), "groups": sub})
        total_list.append(data_list)

    # total_list = json.dumps(total_list, indent=4, ensure_ascii=False)
    # print(total_list)
    return total_list
