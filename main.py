# MEDTRONIC Config Reader
# Reads the configuration from a
# data export file (csv) of a
# medtronic insulin pump.
# The data must be shared with CareLink portal
# and exported as csv data.
import os
from subroutines.messageboxes import *

version = "0.0.1a"


def process():
    key_date = "Date"
    key_time = "Time"
    key_bolus_number = "Bolus Number"
    key_bolus_volume = "Bolus Volume Selected (U)"

    unit_blood_glucose = "mg/dl"
    unit_insulin = "I.E."

    # show welcome message and acknowledgement
    if question_welcome_message(version=version):

        # aks if to show export instructions
        if not question_need_help_export_carelink():
            show_help_export_carelink()

        # get data file
        csv_file = get_csv_data_file(os.getcwd())
        if csv_file:
            data_sets = read_csv_file_data(csv_file)

            # got through each line of data sets
            data_sets = filter_data_sets(data_sets, keys_to_filter=[
                key_date,
                key_time,
                key_bolus_number,
                key_bolus_volume])
            for entry in data_sets:
                #print(entry[key_date] + " " + entry[key_time] + ": " + entry[key_bolus_number]
                #      + " " + unit_blood_glucose)
                #print("\t" + entry[key_bolus_volume] + " " + unit_insulin)
                print(entry)


def get_csv_data_file(default_path, allowed_file_type="*.csv"):
    msg = "Wählen Sie die CSV-Daten Datein aus dem CareLink Export aus."
    title = "Datenquelle wählen"

    return easygui.fileopenbox(msg, title, default_path, allowed_file_type)


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
    for entry in data_sets:
        if isinstance(entry, dict):

            # search for keys in entry
            add = True
            for key in keys_to_filter:
                if key not in entry or len(entry[key]) == 0:
                    add = False
                    break
            if add:
                filtered_data_sets.append(entry)

    return filtered_data_sets


# ---- MAIN ----
if __name__ == '__main__':
    process()
