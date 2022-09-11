# MEDTRONIC Config Reader
# Reads the configuration from a
# data export file (csv) of a
# medtronic insulin pump.
# The data must be shared with CareLink portal
# and exported as csv data.
import os
from subroutines.messageboxes import *
from subroutines.functions import *

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
                print(entry[key_date] + " " + entry[key_time] + ": " + entry[key_bolus_number]
                     + " " + unit_blood_glucose)
                print("\t" + entry[key_bolus_volume] + " " + unit_insulin)


# ---- MAIN ----
if __name__ == '__main__':
    process()
