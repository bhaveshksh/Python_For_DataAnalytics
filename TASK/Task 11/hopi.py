from datetime import datetime

class Department:
    def __init__(self, name):
        self.name = name
        self.doctors = []

class Doctor:
    def __init__(self, name, department):
        self.name = name
        self.department = department
        self.patients = []
        department.doctors.append(self)

class Patient:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.admitted = False
        self.diagnosis = None
        self.prescriptions = []
        self.bill = None
        self.appointments = []
        self.discharged = False

class Prescription(Doctor, Patient, Department):
    def __init__(self, doctor, patient, medicines, diagnosis):
        # Initialize Department with doctor's department
        Department.__init__(self, doctor.department.name)
        # Initialize Doctor
        Doctor.__init__(self, doctor.name, self)
        # Initialize Patient
        Patient.__init__(self, patient.name, patient.age)
        self.medicines = medicines
        self.diagnosis = diagnosis
        self.date = datetime.now()
        # Store references for clarity
        self.doctor_obj = doctor
        self.patient_obj = patient
        self.department_obj = doctor.department

    def get_prescription_details(self):
        return {
            'doctor': self.name,
            'department': self.department.name,
            'patient': self.patient_obj.name,
            'age': self.patient_obj.age,
            'diagnosis': self.diagnosis,
            'medicines': self.medicines,
            'date': self.date.strftime('%Y-%m-%d %H:%M')
        }

class Billing:
    def __init__(self, patient, amount):
        self.patient = patient
        self.amount = amount
        self.paid = False

class Hospital:
    def __init__(self, name):
        self.name = name
        self.departments = []
        self.patients = []
        self.doctors = []

    def admit_patient(self, patient):
        patient.admitted = True
        self.patients.append(patient)
        print(f"Patient {patient.name} admitted.")

    def schedule_appointment(self, patient, doctor, date):
        appointment = {'doctor': doctor, 'date': date}
        patient.appointments.append(appointment)
        doctor.patients.append(patient)
        print(f"Appointment scheduled for {patient.name} with Dr. {doctor.name} on {date}.")

    def diagnose(self, patient, doctor, diagnosis):
        patient.diagnosis = diagnosis
        print(f"Diagnosis for {patient.name}: {diagnosis}")

    def prescribe(self, doctor, patient, medicines):
        prescription = Prescription(doctor, patient, medicines, patient.diagnosis)
        patient.prescriptions.append(prescription)
        details = prescription.get_prescription_details()
        print("Prescription generated:")
        for key, value in details.items():
            print(f"  {key}: {value}")

    def generate_bill(self, patient, amount):
        bill = Billing(patient, amount)
        patient.bill = bill
        print(f"Bill generated for {patient.name}: {amount}")

    def discharge_patient(self, patient):
        patient.discharged = True
        patient.admitted = False
        print(f"Patient {patient.name} discharged.")

    def schedule_recheckup(self, patient, doctor, date):
        self.schedule_appointment(patient, doctor, date)
        print(f"Re-checkup scheduled for {patient.name} with Dr. {doctor.name} on {date}.")

# Example usage
if __name__ == "__main__":
    hospital = Hospital("City Hospital")
    dept = Department("Cardiology")
    hospital.departments.append(dept)
    doc = Doctor("Dr. Smith", dept)
    hospital.doctors.append(doc)
    pat = Patient("John Doe", 45)
    hospital.admit_patient(pat)
    hospital.schedule_appointment(pat, doc, "2026-02-10")
    hospital.diagnose(pat, doc, "Hypertension")
    hospital.prescribe(doc, pat, ["Medicine A", "Medicine B"])
    hospital.generate_bill(pat, 5000)
    hospital.discharge_patient(pat)
    hospital.schedule_recheckup(pat, doc, "2026-03-01")
