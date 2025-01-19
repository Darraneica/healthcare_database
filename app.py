from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

DATA_FILE = './data/patients.json'

# Helper functions
def load_data():
    """Load patient data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        # Create the file if it doesn't exist
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, reset to an empty list
        save_data([])
        return []

def save_data(data):
    """Save patient data to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# Routes
@app.route('/')
def intro():
    """Render the introductory page."""
    return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login page."""
    if request.method == 'POST':
        # Login logic (for simplicity, we assume a hardcoded username/password)
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':  # Simplified authentication
            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        else:
            return "Invalid credentials", 401

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Render the dashboard page with dynamic data."""
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    patients = load_data()
    total_patients = len(patients)
    
    # Get the name of the latest registered patient
    latest_patient = patients[-1] if patients else None
    latest_patient_name = f"{latest_patient['first_name']} {latest_patient['last_name']}" if latest_patient else "No patients registered"
    
    upcoming_appointments = "None"  # Placeholder for actual appointment data

    return render_template('dashboard.html', 
                           total_patients=total_patients, 
                           latest_patient_name=latest_patient_name, 
                           upcoming_appointments=upcoming_appointments)

@app.route('/home', methods=['GET', 'POST'])
def home():
    """Render the home page where users can register a patient."""
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    
    if request.method == 'POST':
        # Get data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        ssn = request.form['ssn']
        insurance = request.form['insurance']
        medical_history = request.form['medical_history']
        billing_history = request.form['billing_history']
        
        # Create a unique ID for the patient
        patient_id = str(random.randint(1000, 9999))

        new_patient = {
            'id': patient_id,
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'ssn': ssn,
            'insurance': insurance,
            'medical_history': medical_history,
            'billing_history': billing_history
        }

        # Load current patient data
        patients = load_data()
        patients.append(new_patient)

        # Save the updated data
        save_data(patients)

        # Display success message
        message = f"Patient {first_name} {last_name} registered successfully!"
        return render_template('home.html', message=message)

    return render_template('home.html')  # Return home.html for patient registration

@app.route('/logout')
def logout():
    """Handle logout."""
    session.pop('username', None)  # Remove user from session
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/patients', methods=['GET'])
def patients():
    """Search and display patients based on a query and additional filters."""
    patients = load_data()
    search_query = request.args.get('search_query', '').lower()
    insurance_filter = request.args.get('insurance', '').lower()
    min_age = request.args.get('min_age', '')
    max_age = request.args.get('max_age', '')

    if search_query:
        patients = [p for p in patients if search_query in (p['first_name'].lower() + ' ' + p['last_name'].lower()) or search_query in p['id']]

    # Filter by insurance type
    if insurance_filter:
        patients = [p for p in patients if insurance_filter in p['insurance'].lower()]

    # Filter by age range
    if min_age:
        patients = [p for p in patients if calculate_age(p['dob']) >= int(min_age)]
    if max_age:
        patients = [p for p in patients if calculate_age(p['dob']) <= int(max_age)]

    return render_template('patients.html', patients=patients, search_query=search_query)


@app.route('/patient/<patient_id>/edit', methods=['GET', 'POST'])
def edit_patient(patient_id):
    """Edit details of a specific patient."""
    patients = load_data()
    patient = next((p for p in patients if p['id'] == patient_id), None)
    
    if request.method == 'POST' and patient:
        patient['first_name'] = request.form['first_name']
        patient['last_name'] = request.form['last_name']
        patient['dob'] = request.form['dob']
        patient['ssn'] = request.form['ssn']
        patient['insurance'] = request.form['insurance']
        patient['medical_history'] = request.form['medical_history']
        patient['billing_history'] = request.form['billing_history']
        save_data(patients)
        return redirect(url_for('patient_profile', patient_id=patient_id))

    return render_template('edit_patient.html', patient=patient)


def calculate_age(dob):
    """Calculate age from date of birth."""
    from datetime import datetime
    birth_date = datetime.strptime(dob, '%Y-%m-%d')
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    
    return render_template('patients.html', patients=patients, search_query=search_query)

@app.route('/patient/<patient_id>', methods=['GET', 'POST'])
def patient_profile(patient_id):
    """View and edit details of a specific patient."""
    patients = load_data()
    patient = next((p for p in patients if p['id'] == patient_id), None)

    if request.method == 'POST' and patient:
        # Update patient details
        patient['first_name'] = request.form['first_name']
        patient['last_name'] = request.form['last_name']
        patient['dob'] = request.form['dob']
        patient['ssn'] = request.form['ssn']
        patient['insurance'] = request.form['insurance']
        patient['medical_history'] = request.form['medical_history']
        patient['billing_history'] = request.form['billing_history']

        save_data(patients)
        return redirect(url_for('patient_profile', patient_id=patient_id))

    elif request.method == 'GET' and patient:
        return render_template('patient_profile.html', patient=patient)

@app.route('/delete_patient/<patient_id>', methods=['POST'])
def delete_patient(patient_id):
    """Delete a specific patient from the database."""
    patients = load_data()
    patients = [p for p in patients if p['id'] != patient_id]  # Remove the patient with the given ID
    save_data(patients)
    return redirect(url_for('patients'))

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    """Manage appointments for patients."""
    if request.method == 'POST':
        # Add new appointment
        patient_id = request.form['patient_id']
        appointment_date = request.form['appointment_date']
        reason = request.form['reason']
        
        appointment = {
            'patient_id': patient_id,
            'appointment_date': appointment_date,
            'reason': reason
        }

        appointments_data = load_appointments_data()
        appointments_data.append(appointment)
        save_appointments_data(appointments_data)

        return redirect(url_for('appointments'))
    
    appointments_data = load_appointments_data()
    return render_template('appointments.html', appointments=appointments_data)

def load_appointments_data():
    """Load appointments data."""
    APPOINTMENTS_FILE = './data/appointments.json'
    if not os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, 'w') as f:
            json.dump([], f)
    try:
        with open(APPOINTMENTS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        save_appointments_data([])
        return []

def save_appointments_data(data):
    """Save appointment data."""
    APPOINTMENTS_FILE = './data/appointments.json'
    try:
        with open(APPOINTMENTS_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving appointments data: {e}")


if __name__ == '__main__':
    app.run(debug=True)
