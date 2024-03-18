import pandas as pd
import json
import matplotlib.pyplot as plt

df = pd.DataFrame(aggregated_data).T.reset_index()
df.columns = ['appointmentId', 'noOfMedicines', 'noOfActiveMedicines', 'noOfInActiveMedicines', 'medicineNames']

df_csv = df[['appointmentId', 'noOfMedicines', 'noOfActiveMedicines', 'noOfInActiveMedicines', 'medicineNames']]
df_csv.to_csv('aggregated_data.csv', sep='~', index=False)

aggregated_json = df.to_dict(orient='records')
with open('aggregated_data.json', 'w') as json_file:
    json.dump(aggregated_json, json_file)

gender_counts = df['gender'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Number of Appointments by Gender')
plt.axis('equal')
plt.show()