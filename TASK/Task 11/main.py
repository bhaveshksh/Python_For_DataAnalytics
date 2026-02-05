"""
Hospital Management System - Main Demonstration
Complete real-time functioning of models and services
"""

from datetime import datetime, timedelta
from models import (
    Hospital, Department, Doctor, Patient, Appointment, Diagnosis,
    Prescription, Billing, PatientStatus, AppointmentStatus,
    SeverityLevel, PaymentStatus
)
from services import (
    PatientService, AppointmentService, DiagnosisService,
    PrescriptionService, BillingService, DischargeService
)


def print_separator(title=""):
    """Print a formatted separator"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'-'*60}\n")


def demonstrate_hospital_setup():
    """Demonstrate hospital and department setup"""
    print_separator("STEP 1: HOSPITAL & DEPARTMENT SETUP")
    
    # Create Hospital
    hospital = Hospital("H001", "City Medical Center", "123 Main St, City", "555-1000", "info@citymedical.com")
    print(f"✓ Hospital Created: {hospital}")
    
    # Create Departments
    cardiology = Department("D001", "Cardiology", "Heart and cardiovascular diseases")
    orthopedics = Department("D002", "Orthopedics", "Bones and joint treatment")
    general = Department("D003", "General Medicine", "General medical treatments")
    
    hospital.add_department(cardiology)
    hospital.add_department(orthopedics)
    hospital.add_department(general)
    print(f"✓ Departments Created: {len(hospital.departments)} departments added")
    
    # Create Doctors
    doctor1 = Doctor("DR001", "Dr. Rajesh Kumar", "Cardiologist", "555-2001", "rajesh@citymedical.com")
    doctor2 = Doctor("DR002", "Dr. Priya Singh", "Orthopedic Surgeon", "555-2002", "priya@citymedical.com")
    doctor3 = Doctor("DR003", "Dr. Amit Patel", "General Physician", "555-2003", "amit@citymedical.com")
    
    cardiology.add_doctor(doctor1)
    cardiology.set_head_doctor(doctor1)
    orthopedics.add_doctor(doctor2)
    orthopedics.set_head_doctor(doctor2)
    general.add_doctor(doctor3)
    general.set_head_doctor(doctor3)
    
    print(f"✓ Doctors Created and Assigned to Departments")
    print(f"  - Cardiology Head: {doctor1}")
    print(f"  - Orthopedics Head: {doctor2}")
    print(f"  - General Medicine Head: {doctor3}")
    
    return hospital, cardiology, orthopedics, general, doctor1, doctor2, doctor3


def demonstrate_patient_services(hospital, doctor1, doctor2, doctor3):
    """Demonstrate patient admission and management"""
    print_separator("STEP 2: PATIENT ADMISSION & MANAGEMENT")
    
    # Initialize services
    patient_service = PatientService(hospital)
    
    # Create Patients
    patient1 = Patient("P001", "Rajesh Kumar", 45, "Male", "555-3001", "rajesh.k@email.com", "456 Oak Ave")
    patient2 = Patient("P002", "Priya Desai", 32, "Female", "555-3002", "priya.d@email.com", "789 Pine Rd")
    patient3 = Patient("P003", "Arjun Singh", 28, "Male", "555-3003", "arjun.s@email.com", "321 Elm St")
    
    # Admit patients
    print("Admitting Patients...")
    result1 = patient_service.admit_patient(patient1, doctor1)
    result2 = patient_service.admit_patient(patient2, doctor2)
    result3 = patient_service.admit_patient(patient3, doctor3)
    
    if result1 and result2 and result3:
        print(f"✓ All patients admitted successfully")
        print(f"  - {patient1}")
        print(f"  - {patient2}")
        print(f"  - {patient3}")
        print(f"\n  Hospital Available Beds: {hospital.available_beds}/{hospital.total_beds}")
    
    return patient_service, patient1, patient2, patient3


def demonstrate_appointments(doctor1, patient1, patient2):
    """Demonstrate appointment scheduling"""
    print_separator("STEP 3: APPOINTMENT SCHEDULING")
    
    appointment_service = AppointmentService()
    
    # Schedule appointments
    apt1_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d 10:00:00")
    apt2_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d 14:30:00")
    
    apt1 = appointment_service.schedule_appointment(patient1, doctor1, apt1_date, "Follow-up for cardiac checkup")
    apt2 = appointment_service.schedule_appointment(patient2, doctor1, apt2_date, "Initial consultation")
    
    if apt1 and apt2:
        print(f"✓ Appointments Scheduled Successfully")
        print(f"  - {apt1}")
        print(f"  - {apt2}")
        
        # Complete an appointment
        print_separator("Completing Appointment")
        appointment_service.complete_appointment(apt1.appointment_id, "Patient doing well, continue medication")
        apt1.mark_completed()
        print(f"✓ Appointment Completed: {apt1.appointment_id}")
        print(f"  Status: {apt1.status.value}")
        print(f"  Notes: {apt1.notes}")
    
    return appointment_service, apt1, apt2


def demonstrate_diagnosis(doctor1, patient1):
    """Demonstrate diagnosis recording"""
    print_separator("STEP 4: DIAGNOSIS RECORDING")
    
    diagnosis_service = DiagnosisService()
    
    # Record diagnosis
    diagnosis = diagnosis_service.record_diagnosis(
        patient1, doctor1,
        "Hypertension (High Blood Pressure)",
        "Patient has elevated blood pressure readings. Requires medication and lifestyle changes.",
        SeverityLevel.MEDIUM
    )
    
    if diagnosis:
        print(f"✓ Diagnosis Recorded Successfully")
        print(f"  - {diagnosis}")
        print(f"  - Description: {diagnosis.description}")
        print(f"  - Recorded by: Dr. {diagnosis.doctor.name}")
    
    return diagnosis_service, diagnosis


def demonstrate_prescriptions(doctor1, patient1, diagnosis):
    """Demonstrate prescription creation"""
    print_separator("STEP 5: PRESCRIPTION MANAGEMENT")
    
    prescription_service = PrescriptionService()
    
    # Create prescription
    prescription = prescription_service.create_prescription(patient1, doctor1, diagnosis)
    
    if prescription:
        print(f"✓ Prescription Created: {prescription}")
        
        # Add medicines
        print("\nAdding Medicines...")
        prescription_service.add_medicine_to_prescription(
            prescription.prescription_id, "Amlodipine", "5mg", "Once daily", "30 days"
        )
        prescription_service.add_medicine_to_prescription(
            prescription.prescription_id, "Lisinopril", "10mg", "Once daily", "30 days"
        )
        prescription_service.add_medicine_to_prescription(
            prescription.prescription_id, "Metoprolol", "50mg", "Twice daily", "30 days"
        )
        
        print(f"✓ Medicines Added Successfully\n")
        print("Prescribed Medicines:")
        for medicine in prescription.get_medicines():
            print(f"  - {medicine['name']}: {medicine['dosage']}, {medicine['frequency']} for {medicine['duration']}")
    
    return prescription_service, prescription


def demonstrate_billing(hospital, patient1, prescription):
    """Demonstrate billing system"""
    print_separator("STEP 6: BILLING & PAYMENT")
    
    billing_service = BillingService()
    
    # Generate bill
    bill = billing_service.generate_bill(patient1)
    
    if bill:
        print(f"✓ Bill Generated: {bill.bill_id}")
        
        # Add charges
        print("\nAdding Charges...")
        billing_service.add_charges(bill.bill_id, "Room Charges (3 days)", 3000.0)
        billing_service.add_charges(bill.bill_id, "Lab Tests", 1500.0)
        billing_service.add_charges(bill.bill_id, "X-Ray", 800.0)
        bill.add_medicine_cost(2500.0)
        
        print(f"✓ All charges added")
        print(f"\n  Consultation Fee: Rs. {bill.consultation_fee:.2f}")
        print(f"  Room Charges: Rs. {bill.room_charges:.2f}")
        print(f"  Medicines Cost: Rs. {bill.medicines_cost:.2f}")
        print(f"  Services Total: Rs. {sum(s['cost'] for s in bill.services):.2f}")
        print(f"  {'='*50}")
        print(f"  TOTAL AMOUNT: Rs. {bill.total_amount:.2f}")
        print(f"  Payment Status: {bill.payment_status.value.upper()}")
        
        # Process payment
        print_separator("Processing Payment")
        payment_amount = 5000.0
        billing_service.process_payment(bill.bill_id, payment_amount)
        print(f"✓ Payment Processed: Rs. {payment_amount:.2f}")
        print(f"\n  Total Amount: Rs. {bill.total_amount:.2f}")
        print(f"  Paid Amount: Rs. {bill.paid_amount:.2f}")
        print(f"  Pending Amount: Rs. {bill.pending_amount:.2f}")
        print(f"  Payment Status: {bill.payment_status.value.upper()}")
        
        # Generate receipt
        print_separator("Bill Receipt")
        print(bill.generate_receipt())
    
    return billing_service, bill


def demonstrate_discharge(patient_service, patient1, doctor1):
    """Demonstrate discharge process"""
    print_separator("STEP 7: DISCHARGE & FOLLOW-UP")
    
    discharge_service = DischargeService(patient_service)
    
    # Generate discharge summary
    print("Generating Discharge Summary...")
    summary = discharge_service.generate_discharge_summary(patient1)
    print(summary)
    
    # Initiate discharge
    print("\nInitiating Discharge...")
    discharge_service.initiate_discharge(patient1.patient_id)
    print(f"✓ Patient Discharged Successfully")
    print(f"  Patient Status: {patient1.status.value}")
    print(f"  Discharge Date: {patient1.discharge_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Schedule follow-up
    followup_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    followup_msg = discharge_service.schedule_follow_up(patient1, followup_date)
    print(f"\n✓ {followup_msg}")


def demonstrate_medical_history(patient1):
    """Display medical history"""
    print_separator("STEP 8: MEDICAL HISTORY")
    
    print(f"Patient: {patient1.name} (ID: {patient1.patient_id})\n")
    print("Medical History:")
    for entry in patient1.get_medical_history():
        print(f"  {entry}")


def demonstrate_reports(billing_service, patient1):
    """Generate reports"""
    print_separator("STEP 9: BILLING REPORT")
    
    report = billing_service.get_billing_report(patient1)
    
    print(f"Patient Name: {report['patient_name']}")
    print(f"Patient ID: {report['patient_id']}")
    print(f"\n{'='*50}")
    print(f"Total Bills Generated: {report['total_bills']}")
    print(f"Total Charged: Rs. {report['total_charged']:.2f}")
    print(f"Total Paid: Rs. {report['total_paid']:.2f}")
    print(f"Total Pending: Rs. {report['total_pending']:.2f}")
    print(f"{'='*50}\n")
    
    if report['bills']:
        print("Bill Details:")
        for bill in report['bills']:
            print(f"\n  Bill ID: {bill['bill_id']}")
            print(f"  Date: {bill['date']}")
            print(f"  Amount: Rs. {bill['amount']:.2f}")
            print(f"  Paid: Rs. {bill['paid']:.2f}")
            print(f"  Pending: Rs. {bill['pending']:.2f}")
            print(f"  Status: {bill['status'].upper()}")


def main():
    """Main function to run complete demonstration"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "HOSPITAL MANAGEMENT SYSTEM" + " "*22 + "║")
    print("║" + " "*15 + "Real-time Functioning Demo" + " "*18 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # Step 1: Hospital Setup
        hospital, cardiology, orthopedics, general, dr1, dr2, dr3 = demonstrate_hospital_setup()
        
        # Step 2: Patient Services
        patient_svc, pat1, pat2, pat3 = demonstrate_patient_services(hospital, dr1, dr2, dr3)
        
        # Step 3: Appointments
        apt_svc, apt1, apt2 = demonstrate_appointments(dr1, pat1, pat2)
        
        # Step 4: Diagnosis
        diag_svc, diag1 = demonstrate_diagnosis(dr1, pat1)
        
        # Step 5: Prescriptions
        pres_svc, pres1 = demonstrate_prescriptions(dr1, pat1, diag1)
        
        # Step 6: Billing
        bill_svc, bill1 = demonstrate_billing(hospital, pat1, pres1)
        
        # Step 7: Discharge
        demonstrate_discharge(patient_svc, pat1, dr1)
        
        # Step 8: Medical History
        demonstrate_medical_history(pat1)
        
        # Step 9: Reports
        demonstrate_reports(bill_svc, pat1)
        
        # Final Summary
        print_separator("DEMONSTRATION COMPLETE")
        print("✓ All hospital management features demonstrated successfully!")
        print(f"\nFinal Hospital Status:")
        print(f"  - Hospital: {hospital}")
        print(f"  - Total Doctors: {len(dr1.department.doctors) + len(dr2.department.doctors) + len(dr3.department.doctors)}")
        print(f"  - Active Patients: {len([p for p in patient_svc.get_all_patients() if p.status == PatientStatus.ADMITTED])}")
        print(f"  - Total Appointments: {len(apt_svc.appointments)}")
        print(f"  - Total Bills: {len(bill_svc.bills)}")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
