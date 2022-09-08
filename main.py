# MEDTRONIC Config Reader
# Reads the configuration from a
# data export file (csv) of a
# medtronic insulin pump.
# The data must be shared with CareLink portal
# and exported as csv data.

import easygui
import os


def process():
    key_date = "Date"
    key_time = "Time"
    key_bolus_number = "Bolus Number"
    key_bolus_volume = "Bolus Volume Selected (U)"

    unit_blood_glucose = "mg/dl"
    unit_insulin = "I.E."

    if welcome_message():
        csv_file = get_csv_data_file(os.getcwd())
        if csv_file:
            data_sets = read_csv_file_data(csv_file)
            for entry in data_sets:
                if key_date in entry \
                        and key_time in entry \
                        and key_bolus_number in entry \
                        and len(entry[key_bolus_number]) > 0:
                    print(entry[key_date] + " " + entry[key_time] + ": " + entry[key_bolus_number] + " " + unit_blood_glucose)

                    if key_bolus_volume in entry and len(entry[key_bolus_volume]):
                        print("\t" + entry[key_bolus_volume] + " " + unit_insulin)


def welcome_message():
    msg = "Willkommen zum MEDTRONIC Config Reader\n" \
          "Dieses Tool liest die Konfiguration des automatischen Algorithmus der Minimed Insulinpumpen aus.\n\n" \
          "Es kann keine Gewährleistung auf Korrektheit oder auf fehlerfreies Verhalten gegeben werden!\n" \
          "Nutzen Sie die Daten nur für Anlysezwecke.\n" \
          "Für Ihre Therapieeinstellung, sprechen Sie mit Ihrem/Ihrer behandelnden/m Arzt/Ärztin.\n\n" \
          "Haben Sie dies zu Nenntnis genommen und verstanden?"
    title = ""
    options = ["Ja", "Nein"]

    return easygui.ynbox(msg, title, options)


def get_csv_data_file(default_path, allowed_file_type="*.csv"):
    msg = "Wählen Sie die CSV-Daten Datein aus dem CareLink Export aus."
    title = "Datenquelle wählen"

    return easygui.fileopenbox(msg, title, default_path, allowed_file_type)


def read_csv_file_data(csv_data_file):
    f = open(csv_data_file, 'r')
    delimiter_char = ';'
    header_line_number = 7
    line_number = 0
    header = []
    data_sets = []

    for line in f:
        # skip not needed lines at start
        if line_number < header_line_number - 1:
            pass

        # read header line
        elif line_number == header_line_number - 1:
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

            if len(current_set) == len(header):
                data_sets.append(current_set)

        line_number += 1

    f.close()

    return data_sets


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process()
