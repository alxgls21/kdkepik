import pandas as pd
from myapp.models import FCTDirectory  # Υποθέτω ότι το νέο μοντέλο είναι το FCTDirectory

# Διαβάζουμε το CSV αρχείο με την σωστή κωδικοποίηση
file_path = 'myapp/static/docs/call_fct.csv'

# Χρήση της σωστής κωδικοποίησης 'ISO-8859-7' για ελληνικά
try:
    df = pd.read_csv(file_path, encoding='ISO-8859-7')
except FileNotFoundError:
    print(f"Το αρχείο {file_path} δεν βρέθηκε.")
    exit()

# Print the columns to debug
print(df.columns)

# Remove any extra spaces from column headers
df.columns = df.columns.str.strip()

# Εισάγουμε τα δεδομένα στο μοντέλο
for index, row in df.iterrows():
    # Ελέγχουμε αν όλες οι απαραίτητες στήλες υπάρχουν στο CSV
    try:
        fct_entry = FCTDirectory(
            epiteleio_sximatismos=row['Επιτελείο - Σχηματισμός'].strip(),  # από το CSV αρχείο
            katigoria=row['Κατηγορία'].strip(),  # από το CSV αρχείο
            antapokritis=row['Ανταποκριτής'].strip(),  # από το CSV αρχείο
            arithmos_call=row['Αριθμός Κλήσεως'].strip()  # από το CSV αρχείο
        )
        fct_entry.save()
    except KeyError as e:
        print(f"Λείπει η στήλη: {e} στο CSV αρχείο. Παρακαλώ ελέγξτε το αρχείο.")
        continue

print("Τα δεδομένα εισήχθησαν επιτυχώς!")
