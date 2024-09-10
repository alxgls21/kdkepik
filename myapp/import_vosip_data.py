import pandas as pd
from myapp.models import VOSIPTelephoneDirectory

# Διαβάζουμε το CSV αρχείο
file_path = 'myapp/static/docs/call_vosip.csv'

df = pd.read_csv(file_path, encoding='utf-8')

# Print the columns to debug
print(df.columns)

# Remove any extra spaces from column headers
df.columns = df.columns.str.strip()

# Εισάγουμε τα δεδομένα στο μοντέλο
for index, row in df.iterrows():
    vosip_entry = VOSIPTelephoneDirectory(
        epiteleio_sximatismos=row['Επιτελείο - Σχηματισμός'],
        xristis=row['Χρήστης'],
        arithmos_vosip=row['Αριθμός Τηλεφώνου VoSIP'],
        paratiriseis=row['Παρατηρήσεις']
    )
    vosip_entry.save()

print("Τα δεδομένα εισήχθησαν επιτυχώς!")
