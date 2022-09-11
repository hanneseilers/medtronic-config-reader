# MEDTRONIC Config Reader
# Reads the configuration from a
# data export file (csv) of a
# medtronic insulin pump.
# The data must be shared with CareLink portal
# and exported as csv data.
import os
import sys, getopt
from subroutines.messageboxes import *
from subroutines.functions import *

version = "0.0.1a"


def welcome(csv_file=None, skip=False):
    # show welcome message and acknowledgement
    if skip or question_welcome_message(version=version):

        # aks if to show export instructions
        if not skip and not question_need_help_export_carelink():
            show_help_export_carelink()

        # maybe get data file
        if isinstance(csv_file, str) and len(csv_file) > 0:
            process(csv_file)
        else:
            process(get_csv_data_file(os.getcwd()))


def process(csv_file=None):
    key_date = "Date"
    key_time = "Time"
    key_bolus_number = "Bolus Number"
    key_bolus_volume = "Bolus Volume Selected (U)"

    unit_blood_glucose = "mg/dl"
    unit_insulin = "I.E."

    # process data file
    if csv_file:
        data_sets = read_csv_file_data(csv_file)

        # got through each line of data sets
        data_sets = filter_data_sets(data_sets, keys_to_filter=[
            key_date,
            key_time,
            key_bolus_number,
            key_bolus_volume])
        for entry in data_sets:
            print(entry[key_date] + " " + entry[key_time] + ": " + entry[key_bolus_number]
                  + " " + unit_blood_glucose)
            print("\t" + entry[key_bolus_volume] + " " + unit_insulin)


# ---- MAIN ----
if __name__ == '__main__':
    input_file = None
    skip_questions=False
    argv = sys.argv[1:]

    # try to get arguments
    try:

        opts, args = getopt.getopt(argv, "ish", ["input_csv=", "skip", "help"])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(str(sys.argv[0]) + " <option>\n"
                                         "-i --input_csv\tInput csv data file\n"
                                         "-s --skip\tSkip all welcome messages and acknowledgement questions"
                                         "-h --help\tThis help")
            elif opt in ("-i", "--input_csv"):
                input_file = arg
            elif opt in ("-s", "--skip"):
                skip_questions = True

    except getopt.GetoptError:
        pass

    welcome(input_file, skip_questions)
