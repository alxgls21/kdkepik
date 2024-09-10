import pandas as pd
from myapp.models import HARPDirectory

# Διαβάζουμε το CSV αρχείο
file_path = 'myapp/static/docs/call_harp.csv'

df = pd.read_csv(file_path, encoding='utf-8')

# Print the columns to debug
print(df.columns)

# Remove any extra spaces from column headers
df.columns = df.columns.str.strip()

# Εισάγουμε τα δεδομένα στο μοντέλο
for index, row in df.iterrows():
    harp_entry = HARPDirectory(
        epiteleio_sximatismos=row['Επιτελείο - Σχηματισμός'],
        aa_ana_sximatismo=row['Α/Α (ανα σχηματισμό)'],
        antapokritis=row['Ανταποκριτής'],
        arithmos_sip=row['Αριθμός SIP'],
        syskeyi=row['Συσκευή']
    )
    harp_entry.save()

print("Τα δεδομένα εισήχθησαν επιτυχώς!")
