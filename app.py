from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

patients = []
doctors = [
    {"name": "Dr. John Doe", "specialty": "Cardiologist"},
    {"name": "Dr. Jane Smith", "specialty": "Dermatologist"},
    {"name": "Dr. Emily Johnson", "specialty": "Pediatrician"},
]

appointments = []
consultation_records = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        phone = request.form['phone']
        patients.append({
            "name": name,
            "age": age,
            "address": address,
            "phone": phone
        })
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/appointments', methods=['GET', 'POST'])
def manage_appointments():
    if request.method == 'POST':
        if 'add_appointment' in request.form:
            patient_name = request.form['patient_name']
            doctor_name = request.form['doctor_name']
            appointment_date = request.form['appointment_date']
            appointments.append({
                "patient_name": patient_name,
                "doctor_name": doctor_name,
                "appointment_date": datetime.strptime(appointment_date, '%Y-%m-%d')
            })
        elif 'delete_appointment' in request.form:
            appointment_index = int(request.form['appointment_index'])
            if 0 <= appointment_index < len(appointments):
                appointments.pop(appointment_index)
        return redirect(url_for('manage_appointments'))

    # Sort appointments by date
    sorted_appointments = sorted(appointments, key=lambda x: x['appointment_date'])
    return render_template('appointments.html', doctors=doctors, appointments=sorted_appointments)

@app.route('/list_patient' , methods=['GET', 'POST'])
def manage_patients():
    if request.method == 'POST':
        patient_index = int(request.form['patient_index'])
        if 0 <= patient_index < len(patients):
            patients.pop(patient_index)
        return redirect(url_for('manage_patients'))

    return render_template('list_patient.html', patients=patients)

@app.route('/consultation_history', methods=['GET', 'POST'])
def consultation_history():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        consultation_result = request.form['consultation_result']
        consultation_records.append({
            "patient_name": patient_name,
            "doctor_name": doctor_name,
            "result": consultation_result
        })
        return redirect(url_for('consultation_history'))

    return render_template('consultation_history.html', doctors=doctors, records=consultation_records)

@app.route('/search_appointments', methods=['GET', 'POST'])
def search_appointments():
    if request.method == 'POST':
        search_name = request.form['search_name']
        filtered_appointments = [appt for appt in appointments if appt['patient_name'] == search_name]
        return render_template('search_appointments.html', appointments=filtered_appointments, search_name=search_name)
    
    return render_template('search_appointments.html', appointments=[])

if __name__ == '__main__':
    app.run(debug=True)