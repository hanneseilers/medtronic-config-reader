# MEDTRONIC Config Reader
# Reads the configuration from a
# data export file (csv) of a
# medtronic insulin pump.
# The data must be shared with CareLink portal
# and exported as csv data.
import getopt
import os
import sys
import statistics
import collections

from subroutines.functions import *
from subroutines.messageboxes import *

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
    key_basal_rate = "Basal Rate (U/h)"
    key_bolus_volume_delivered = "Bolus Volume Delivered (U)"
    key_bolus_source = "Bolus Source"

    value_bolus_source_auto_basal = "CLOSED_LOOP_AUTO_BASAL"

    unit_blood_glucose = "mg/dl"
    unit_insulin = "I.E."
    unit_insulin_per_hour = unit_insulin + "/h"

    # process data file
    if csv_file:
        data_sets = read_csv_file_data(csv_file)

        # got through each line of data sets
        data_sets = filter_data_sets(data_sets, keys_to_filter=[
            key_date,
            key_time,
            key_bolus_volume_delivered,
            key_bolus_source])

        # filter for basal rate
        basal_rate = get_basal_rate(
            data_sets=data_sets,
            key_time=key_time,
            key_bolus_delivered=key_bolus_volume_delivered,
            key_bolus_source=key_bolus_source,
            value_bolus_auto_basal=value_bolus_source_auto_basal)
        for time in basal_rate:
            print("{:8}{:.2f} {}".format(time, basal_rate[time], unit_insulin_per_hour))


def get_basal_rate(data_sets, key_time, key_bolus_delivered, key_bolus_source, value_bolus_auto_basal):
    timeslots = {}
    if isinstance(data_sets, list):

        # get all basal rates
        for entry in data_sets:

            if key_time in entry \
                    and key_bolus_delivered in entry \
                    and key_bolus_source in entry\
                    and value_bolus_auto_basal in entry[key_bolus_source]:
                # TODO: Filter for dates
                time = entry[key_time]
                basal_rate = float(str(entry[key_bolus_delivered]).replace(',', '.'))

                # check for valid basel rate
                if basal_rate > 0:
                    # get timeslot
                    time = str(time).split(':')
                    if not len(time) > 1:
                        break

                    h = int(time[0])
                    m = int(time[1])

                    if m <= 15:
                        m = "00"
                    elif 15 < m <= 45:
                        m = "30"
                    else:
                        m = "00"
                        h += 1

                    time = "{:02d}:{}".format(h, m)
                    if time not in timeslots:
                        timeslots[time] = []
                    timeslots[time].append(basal_rate)

        # calculate basal_rate
        for time in timeslots:
            data = timeslots[time]
            timeslots[time] = statistics.median(data)

        return collections.OrderedDict(sorted(timeslots.items()))


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
