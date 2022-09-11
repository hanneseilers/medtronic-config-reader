import re


def read_csv_file_data(csv_data_file):
    f = open(csv_data_file, 'r')
    delimiter_char = ';'
    header_line_number = 7
    header_line_number -= 1     # starting with line 0
    line_number = 0
    header = []
    data_sets = []

    for line in f:
        # skip not needed lines at start
        if line_number < header_line_number:
            pass

        # read header line
        elif line_number == header_line_number:
            header = line.split(delimiter_char)

        # read data
        else:
            n = 0
            current_set = {}
            for data in line.split(delimiter_char):
                if n < len(header):
                    current_set[header[n]] = data
                else:
                    break
                n += 1

            if len(current_set) >= len(header):
                data_sets.append(current_set)

        line_number += 1

    f.close()

    return data_sets


def filter_data_sets(data_sets, keys_to_filter=[]):
    filtered_data_sets = []
    key_index = "Index"
    for entry in data_sets:

        # check if entry is a valid dictionary
        if isinstance(entry, dict):

            # check for valid index
            if key_index in entry and is_float(entry[key_index]):

                # search for keys in entry
                add = True
                for key in keys_to_filter:
                    if key not in entry or len(entry[key]) == 0:
                        add = False
                        break
                if add:
                    filtered_data_sets.append(entry)

    return filtered_data_sets


def is_float(string):
    string = str(string)
    string = string.replace(',', '.')
    return re.match(r'^-?\d+(?:\.\d+)$', string) is not None
