import json
import hashlib
import datetime

with open('DataEngineeringQ2.json') as json_file:
    data = json.load(json_file)

def is_valid_mobile(phone_number):
    if phone_number is None:
        return False
    if phone_number.startswith(('+91', '91')):
        phone_number = phone_number[3:] if phone_number.startswith('+91') else phone_number[2:]
    return len(phone_number) == 10 and phone_number.isdigit() and phone_number[:1] in ['6', '7', '8', '9']


transformed_data = []

for appointment in data:
    selected_data = {
        'appointmentId': appointment['appointmentId'],
        'phoneNumber': appointment['phoneNumber'],
        'firstName': appointment['patientDetails']['firstName'],
        'lastName': appointment['patientDetails'].get('lastName', ''),
        'gender': 'male' if appointment['patientDetails'].get('gender', '').upper() == 'M' else 'female' if appointment['patientDetails'].get('gender', '').upper() == 'F' else 'others',
        'DOB': appointment['patientDetails'].get('birthDate', None),
        'medicines': appointment['consultationData']['medicines']
    }
    
    selected_data['fullName'] = f"{selected_data['firstName']} {selected_data['lastName']}".strip()
    
    selected_data['isValidMobile'] = is_valid_mobile(selected_data['phoneNumber'])
    
    if selected_data['isValidMobile']:
        selected_data['phoneNumberHash'] = hashlib.sha256(selected_data['phoneNumber'].encode()).hexdigest()
    else:
        selected_data['phoneNumberHash'] = None
    
    if selected_data['DOB'] is not None:
        dob = datetime.datetime.strptime(selected_data['DOB'], "%Y-%m-%dT%H:%M:%S.%fZ")
        today = datetime.datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        selected_data['Age'] = age
    else:
        selected_data['Age'] = None
    
    transformed_data.append(selected_data)
    
aggregated_data = {}
medicine_names = {}

for appointment in transformed_data:
    appointment_id = appointment['appointmentId']
    
    if appointment_id not in aggregated_data:
        aggregated_data[appointment_id] = {
            'noOfMedicines': 0,
            'noOfActiveMedicines': 0,
            'noOfInActiveMedicines': 0,
            'medicineNames': []
        }
    
    aggregated_data[appointment_id]['noOfMedicines'] += len(appointment['medicines'])
    
    for medicine in appointment['medicines']:
        if medicine['isActive']:
            aggregated_data[appointment_id]['noOfActiveMedicines'] += 1
            aggregated_data[appointment_id]['medicineNames'].append(medicine['medicineName'])
        else:
            aggregated_data[appointment_id]['noOfInActiveMedicines'] += 1

for appointment_id, data in aggregated_data.items():
    data['medicineNames'] = ', '.join(data['medicineNames'])

print("Transformed and Aggregated Data:")
for appointment_id, data in aggregated_data.items():
    print(appointment_id, data)

# STEP 2
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