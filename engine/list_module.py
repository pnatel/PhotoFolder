# https://www.codespeedy.com/find-the-common-elements-in-two-lists-in-python/
# payload = request.get_data().decode("utf-8")
# list = getListOfFiles(cfg._destinationFolder)

def common(lst1, lst2):
    if type(lst1) is str:
        return common_string_in_list (lst1, lst2)
    elif type(lst2) is str:
        return common_string_in_list (lst2, lst1)
    else:
        return list(set(lst1).intersection(lst2))
        # return list(set(lst1) & set(lst2))

def uncommon(base_list, special_list):
    # remove EOL special string
    # base_list = [item.replace('\n', '') for item in base_list]
    # special_list = [item.replace('\n', '') for item in special_list]
    a = set(base_list)
    b = set(special_list)
    print(base_list, a)
    print(special_list, b)
    print(list(a - b))
    return list(a - b)

def common_string_in_list(string, list):
    new_list = []
    for item in list:
        if str(item) in string and '/' in str(item):
            item = item.split('/')[-1:]
            new_list.append(item[0])
        elif str(item) in string:
            new_list.append(item)
    return new_list

def clear_duplicates(file):
    with open(file, "r") as f:
        file_list = f.readlines()

        # Walk the list and remove empty lines
        for item in file_list:
            if item == '':
                file_list.pop(item)

    # remove duplicates before record
        file_list.sort()
        new_list = set(file_list)
    with open(file, "w") as f:
        f.writelines(new_list)

# "borrowed" from https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def append_multiple_lines(file_name, lines_to_append):
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        appendEOL = False
        # Move read cursor to the start of file.
        file_object.seek(0)
        # Check if file is not empty
        data = file_object.read(100)
        if len(data) > 0:
            appendEOL = True
            file_object.seek(0)
            source = file_object.readlines()
            # clear unwanted EOL from original file
            source = [item.replace('\n', '') for item in source]
            # remove possible duplicates
            lines_to_append = uncommon(lines_to_append, source)
        # Iterate over each string in the list
        for line in lines_to_append:
            # If file is not empty then append '\n' before first line for
            # other lines always append '\n' before appending line
            if appendEOL == True:
                file_object.write("\n")
            else:
                appendEOL = True
            # Append element at the end of file
            file_object.write(line)



if __name__ == "__main__":
    a=[2,9,4,5]
    b=[3,5,7,9]
    c='2,9,4,5'
    print('[9, 5] ==', common(a,b))
    print('[5, 9] ==', common(b,c))
    print('[2, 4] ==', uncommon(a, b))
    print(uncommon(b,c))
