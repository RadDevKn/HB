import sqlite3
from datetime import datetime


# Erstellt Datenbank

def setup_database():
    connection = sqlite3.connect("haushaltsbuch.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eintraege (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_type TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL
       )
""")
    
    connection.commit()
    connection.close()

# Einträge hinzufügen

def add_entry():
    print("\n-Neuer Eintrag-")
    entry_type = input("Einnahme oder Ausgabe? (e/a)")
    if entry_type == "e":
        entry_type = "Einnahme"
    elif entry_type == "a":
        entry_type = "Ausgabe"
    else:
        print("Ungültige Eingabe!")
        return
    
    print("\nKategorie")
    print("1 - Miete")
    print("2 - Lebensmittel")
    print("3 - Transport")
    print("4 - Freizeit")
    print("5 - Gehalt")
    print("6 - Sonstige")
    category = input("Kategorie wählen: ")
    if category == "1":
        category = "Miete"
    elif category == "2":
        category = "Lebensmittel"
    elif category == "3":
        category = "Transport"
    elif category == "4":
        category = "Freizeit"
    elif category == "5":
        category = "Gehalt"
    elif category == "6":
        category = "Sonstiges"
    else:
        print("Ungültige Eingabe")
        return

    while True:
        date = input("Datum (YYYY-MM-DD): ")
        try:
            datetime.strptime(date,"%Y-%m-%d")
            break
        except ValueError:
            print("Falsches Format: YYYY-MM-DD verwenden.")

    description = input("Beschreibung: ")
    amount = float(input("Betrag in Euro "))

    connection = sqlite3.connect("haushaltsbuch.db")
    cursor = connection.cursor()

    cursor.execute("""
                   INSERT INTO eintraege (entry_type, category, date, description, amount)
                   VALUES (?, ?, ?, ?, ?)
                   """, (entry_type, category, date, description, amount))

    connection.commit()
    connection.close()


    print("\nEintrag gespeichert:")
    print(entry_type + " ! " + date + " ! " + description + " ! " + str(amount) + " €")

# Hauptfunktion

def main ():
    setup_database()
    print("-Haushaltsbuch-")

    while True:
        print("\n1 - Eintrag hinzufügen")
        print("2 - Übersicht anzeigen")
        print("3 - Auswertung anzeigen")
        print("4 - Beenden")

        choice = input("Deine Wahl: ")

        if choice == "1":
            add_entry()
        elif choice == "2":
            show_overview()
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            print("Beendet")
            break
        else:
            print("Ungültige Eingabe, bitte 1, 2, 3 oder 4 wählen")

# Zeigt Gesamtübersicht und Endsumme, Monats und Jahresfilter

def show_overview():
    print("\n- Übersicht -")
    print("1 - Alle Einträge anzeigen")
    print("2 - Nach Monat filtern")
    print("3 - Nach Jahr filtern")
    choice = input("Deine Wahl: ")

    connection = sqlite3.connect("haushaltsbuch.db")
    cursor = connection.cursor()

    if choice == "1":
        cursor.execute("SELECT id, entry_type, category, date, description, amount FROM eintraege")
    elif choice == "2":
        while True:
            monat = input("Monat eingeben (YYYY-MM): ")
            try:
                datetime.strptime(monat, "%Y-%m")
                break
            except ValueError:
                print("Falsches Format: YYYY-MM verwenden.")
        cursor.execute("SELECT id, entry_type, category, date, description, amount FROM eintraege WHERE date LIKE ?", (monat + "%",))
    elif choice == "3":
        while True:
            jahr = input("Jahr eingeben: ")
            try:
                datetime.strptime(jahr, "%Y")
                break
            except ValueError:
                print("Falsches Format: YYYY verwenden.")
        cursor.execute("SELECT id, entry_type, category, date, description, amount FROM eintraege WHERE date LIKE ?", (jahr + "%",))
    else:
        print("Ungültige Eingabe")
        connection.close()
        return 

    entries = cursor.fetchall()

    if len(entries) == 0:
        print("\n Keine Einträge vorhanden.")
        connection.close()
        return
    
    print("\n-Übersicht-")
    total = 0

    for entry in entries:
        entry_id = entry[0]
        entry_type = entry[1]
        category = entry[2]
        date = entry[3]
        description = entry[4]
        amount = entry[5]

        if entry_type == "Einnahme":
            total += amount
        else:
            total -= amount

        print(str(entry_id) + " ! " + entry_type + " ! " + category + " ! " + date + " ! " + description + " ! " + str(amount) + " €")
    
    print("\nKontostand: " + str(total) + " €")

#Zeigt höchste und durchschnittliche Ausgabe und Einnahme

def show_statistics():
    connection = sqlite3.connect("haushaltsbuch.db")
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(amount), AVG(amount) FROM eintraege WHERE entry_type = ?", ("Ausgabe",))
    result = cursor.fetchone()

    print("\n-Auswertung-")
    print("Höchste Ausgabe: " + str(result[0]) + " €")
    print("Durchschnitt Ausgaben: " + str(result[1]) + " €")

    cursor.execute("SELECT MAX(amount), AVG(amount) FROM eintraege WHERE entry_type = ?", ("Einnahme",))
    result = cursor.fetchone()

    connection.close()

    print("Höchste Einnahme: " + str(result[0]) + " €")
    print("Durchschnitt Einnahme: " + str(result[1]) + " €")


main()

