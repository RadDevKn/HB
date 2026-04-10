import sqlite3


# Erstellt Datenbank

def setup_database():
    connection = sqlite3.connect("haushaltsbuch.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eintraege (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_type TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL
       )
""")
    
    connection.commit()
    connection.close()

# Eintträge hinzufügen

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
    
    date = input("Datum: ")
    description = input("Beschreibung: ")
    amount = float(input("Betrag in Euro "))

    connection = sqlite3.connect("haushaltsbuch.db")
    cursor = connection.cursor()

    cursor.execute("""
                   INSERT INTO eintraege (entry_type, date, description, amount)
                   VALUES (?, ?, ?, ?)
                   """, (entry_type, date, description, amount))

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
        print("3 - Beenden")

        choice = input("Deine Wahl: ")

        if choice == "1":
            add_entry()
        elif choice == "2":
            show_overview()
        elif choice == "3":
            print("Beendet")
            break
        else:
            print("Ungültige Eingabe, bitte 1, 2 oder 3 wählen")

# Zeigt Gesamtübersicht und Endsumme

def show_overview():
    connection = sqlite3.connect("haushaltsbuch.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, entry_type, date, description, amount FROM eintraege")
    entries = cursor.fetchall()

    connection.close()

    if len(entries) == 0:
        print("\n Keine Einträge vorhanden.")
        return
    
    print("\n-Übersicht-")
    total = 0

    for entry in entries:
        entry_id = entry[0]
        entry_type = entry[1]
        date = entry[2]
        description = entry[3]
        amount = entry[4]

        if entry_type == "Einnahme":
            total += amount
        else:
            total -= amount

        print(str(entry_id) + " ! " + entry_type + " ! " + date + " ! " + description + " ! " + str(amount) + " €")
    
    print("\nKontostand: " + str(total) + " €")


main()

