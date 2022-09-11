import easygui


# ---- MESSAGE BOXES ----
def question_welcome_message(version=""):
    msg = "Willkommen zum MEDTRONIC Config Reader\n" \
          "Dieses Tool liest die Konfiguration des automatischen Algorithmus der Minimed Insulinpumpen aus.\n\n" \
          "Es kann keine Gewährleistung auf Korrektheit oder auf fehlerfreies Verhalten gegeben werden!\n" \
          "Nutzen Sie die Daten nur für Anlysezwecke.\n" \
          "Für Ihre Therapieeinstellung, sprechen Sie mit Ihrem/Ihrer behandelnden/m Arzt/Ärztin.\n\n" \
          "Haben Sie dies zu Nenntnis genommen und verstanden?"
    title = "Medtronic Config Reader " + version
    options = ["Ja (Weiter)", "Nein (Abbrechen)"]

    return easygui.ynbox(msg, title, options)


def question_need_help_export_carelink():
    msg = "Exportieren Sie Daten für einen gewünschten Zeitraum aus Medtronic Carelink(TM) als CV Daten\n" \
          "Brauchen Sie dabei Hilfe und eine Anleitung?"
    title = "Daten-Export - Brauchen Sie Hilfe?"
    options = ["Weiter (keine Hilfe)", "Hilfe anzeigen"]

    return easygui.ynbox(msg, title, options)


def show_help_export_carelink():
    msg = "Um Ihre Daten aus CareLink (TM) zu exportieren gehen Sie wie folgt vor:\n\n" \
          "1. Loggen Sie sich auf https://carelink.minimed.eu/ ein.\n" \
          "2. Laden Sie ggf. Ihre Pumpendaten für den gewünschten Zeiraum hoch.\n" \
          "3. Gehen Sie in den bereich Berichte und wählen den gewünschten Zeitraum aus.\n" \
          "4. Klicken Sie ganz unten rechts auf der Seite aus 'Daten Export (CSV)' und speichern die Datei ab.\n" \
          "5. Klicken Sie auf 'Fortzsetzen' und wählen Sie im nächsten Schritt die soeben heruntergeladene Datei aus."
    title = "Daten-Export - Anleitung"
    ok_button = "Fortsetzen"

    return easygui.msgbox(msg, title, ok_button)