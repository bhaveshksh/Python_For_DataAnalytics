"""
Hospital Management System - Service Layer
Business logic and orchestration for hospital operations
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict
from models import (
    Hospital, Department, Doctor, Patient, Appointment, Diagnosis, 
    Prescription, Billing, PatientStatus, AppointmentStatus, 
    SeverityLevel, PaymentStatus
)


# ==================== PATIENT SERVICE ====================
class PatientService:
    """Service class for patient-related operations"""
    
    def __init__(self, hospital: Hospital):
        self.hospital = hospital
        self.patients: Dict[str, Patient] = {}
    
    def admit_patient(self, patient: Patient, doctor: Doctor) -> bool:
        """Admit a patient to the hospital"""
        try:
            if self.hospital.available_beds <= 0:
                raise Exception("No available beds in the hospital")
            
            patient.admit(doctor)
            self.patients[patient.patient_id] = patient
            self.hospital.update_available_beds(-1)
            
            # Add to medical history
            patient.add_medical_history(f"Admitted to {self.hospital.name} under Dr. {doctor.name}")
            
            return True
        except Exception as e:
            print(f"Error admitting patient: {str(e)}")
            return False
    
    def discharge_patient(self, patient_id: str) -> bool:
        """Discharge a patient from the hospital"""
        try:
            patient = self.get_patient_details(patient_id)
            if patient is None:
                raise Exception(f"Patient {patient_id} not found")
            
            if patient.status != PatientStatus.ADMITTED:
                raise Exception(f"Patient is not currently admitted")
            
            patient.discharge()
            self.hospital.update_available_beds(1)
            patient.add_medical_history("Discharged from hospital")
            
            return True
        except Exception as e:
            print(f"Error discharging patient: {str(e)}")
            return False
    
    def get_patient_details(self, patient_id: str) -> Optional[Patient]:
        """Get patient details by ID"""
        return self.patients.get(patient_id)
    
    def update_patient_info(self, patient_id: str, **kwargs) -> bool:
        """Update patient information"""
        try:
            patient = self.get_patient_details(patient_id)
            if patient is None:
                raise Exception(f"Patient {patient_id} not found")
            
            for key, value in kwargs.items():
                if hasattr(patient, key):
                    setattr(patient, key, value)
            
            return True
        except Exception as e:
            print(f"Error updating patient: {str(e)}")
            return False
    
    def get_all_patients(self) -> List[Patient]:
        """Get all patients"""
        return list(self.patients.values())
    
    def search_patients_by_name(self, name: str) -> List[Patient]:
        """Search patients by name"""
        return [p for p in self.patients.values() if name.lower() in p.name.lower()]


# ==================== APPOINTMENT SERVICE ====================
class AppointmentService:
    """Service class for appointment-related operations"""
    
    def __init__(self):
        self.appointments: Dict[str, Appointment] = {}
    
    def schedule_appointment(self, patient: Patient, doctor: Doctor, 
                           appointment_date_time: str, reason: str) -> Optional[Appointment]:
        """Schedule a new appointment"""
        try:
            # Check doctor availability
            if not doctor.is_available(appointment_date_time):
                raise Exception(f"Dr. {doctor.name} is not available at {appointment_date_time}")
            
            # Check for conflicting appointments
            if self._has_conflict(doctor, appointment_date_time):
                raise Exception("Doctor has another appointment at this time")
            
            appointment = Appointment(patient, doctor, appointment_date_time, reason)
            self.appointments[appointment.appointment_id] = appointment
            
            return appointment
        except Exception as e:
            print(f"Error scheduling appointment: {str(e)}")
            return None
    
    def reschedule_appointment(self, appointment_id: str, new_date_time: str) -> bool:
        """Reschedule an existing appointment"""
        try:
            appointment = self.appointments.get(appointment_id)
            if appointment is None:
                raise Exception(f"Appointment {appointment_id} not found")
            
            if appointment.status == AppointmentStatus.CANCELLED:
                raise Exception("Cannot reschedule a cancelled appointment")
            
            if not self._is_valid_reschedule(appointment, new_date_time):
                raise Exception("Invalid reschedule time")
            
            appointment.reschedule(new_date_time)
            return True
        except Exception as e:
            print(f"Error rescheduling appointment: {str(e)}")
            return False
    
    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel an appointment"""
        try:
            appointment = self.appointments.get(appointment_id)
            if appointment is None:
                raise Exception(f"Appointment {appointment_id} not found")
            
            appointment.cancel()
            return True
        except Exception as e:
            print(f"Error cancelling appointment: {str(e)}")
            return False
    
    def get_doctor_appointments(self, doctor: Doctor, date: str) -> List[Appointment]:
        """Get all appointments for a doctor on a specific date"""
        return [apt for apt in self.appointments.values() 
                if apt.doctor == doctor and apt.appointment_date_time.startswith(date)
                and apt.status != AppointmentStatus.CANCELLED]
    
    def complete_appointment(self, appointment_id: str, notes: str = "") -> bool:
        """Mark appointment as completed"""
        try:
            appointment = self.appointments.get(appointment_id)
            if appointment is None:
                raise Exception(f"Appointment {appointment_id} not found")
            
            appointment.mark_completed()
            if notes:
                appointment.add_notes(notes)
            return True
        except Exception as e:
            print(f"Error completing appointment: {str(e)}")
            return False
    
    def _has_conflict(self, doctor: Doctor, appointment_date_time: str) -> bool:
        """Check if doctor has conflicting appointments"""
        for apt in self.appointments.values():
            if (apt.doctor == doctor and apt.appointment_date_time == appointment_date_time 
                and apt.status != AppointmentStatus.CANCELLED):
                return True
        return False
    
    def _is_valid_reschedule(self, appointment: Appointment, new_date_time: str) -> bool:
        """Validate reschedule request"""
        if appointment.status in [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED]:
            return False
        return True


# ==================== DIAGNOSIS SERVICE ====================
class DiagnosisService:
    """Service class for diagnosis-related operations"""
    
    def __init__(self):
        self.diagnoses: Dict[str, Diagnosis] = {}
    
    def record_diagnosis(self, patient: Patient, doctor: Doctor, diagnosis_name: str, 
                        description: str, severity_level: SeverityLevel) -> Optional[Diagnosis]:
        """Record a diagnosis for a patient"""
        try:
            diagnosis = Diagnosis(patient, doctor, diagnosis_name, description, severity_level)
            self.diagnoses[diagnosis.diagnosis_id] = diagnosis
            patient.add_diagnosis(diagnosis)
            
            # Add to medical history
            patient.add_medical_history(f"Diagnosed with {diagnosis_name} by Dr. {doctor.name}")
            
            return diagnosis
        except Exception as e:
            print(f"Error recording diagnosis: {str(e)}")
            return None
    
    def get_patient_diagnoses(self, patient: Patient) -> List[Diagnosis]:
        """Get all diagnoses for a patient"""
        return patient.diagnoses
    
    def get_diagnosis_details(self, diagnosis_id: str) -> Optional[Diagnosis]:
        """Get diagnosis details by ID"""
        return self.diagnoses.get(diagnosis_id)
    
    def update_diagnosis(self, diagnosis_id: str, diagnosis_name: str, 
                        description: str, severity_level: SeverityLevel) -> bool:
        """Update diagnosis information"""
        try:
            diagnosis = self.get_diagnosis_details(diagnosis_id)
            if diagnosis is None:
                raise Exception(f"Diagnosis {diagnosis_id} not found")
            
            diagnosis.update_diagnosis(diagnosis_name, description, severity_level)
            return True
        except Exception as e:
            print(f"Error updating diagnosis: {str(e)}")
            return False


# ==================== PRESCRIPTION SERVICE ====================
class PrescriptionService:
    """Service class for prescription-related operations"""
    
    def __init__(self):
        self.prescriptions: Dict[str, Prescription] = {}
    
    def create_prescription(self, patient: Patient, doctor: Doctor, diagnosis: Diagnosis) -> Optional[Prescription]:
        """Create a new prescription"""
        try:
            prescription = Prescription(patient, doctor, diagnosis)
            self.prescriptions[prescription.prescription_id] = prescription
            patient.add_prescription(prescription)
            
            return prescription
        except Exception as e:
            print(f"Error creating prescription: {str(e)}")
            return None
    
    def add_medicine_to_prescription(self, prescription_id: str, medicine_name: str, 
                                    dosage: str, frequency: str, duration: str) -> bool:
        """Add a medicine to a prescription"""
        try:
            prescription = self.prescriptions.get(prescription_id)
            if prescription is None:
                raise Exception(f"Prescription {prescription_id} not found")
            
            prescription.add_medicine(medicine_name, dosage, frequency, duration)
            return True
        except Exception as e:
            print(f"Error adding medicine: {str(e)}")
            return False
    
    def get_patient_prescriptions(self, patient: Patient) -> List[Prescription]:
        """Get all prescriptions for a patient"""
        return patient.prescriptions
    
    def get_prescription_details(self, prescription_id: str) -> Optional[Prescription]:
        """Get prescription details by ID"""
        return self.prescriptions.get(prescription_id)
    
    def is_prescription_valid(self, prescription_id: str) -> bool:
        """Check if a prescription is still valid"""
        prescription = self.get_prescription_details(prescription_id)
        if prescription is None:
            return False
        return prescription.is_valid()


# ==================== BILLING SERVICE ====================
class BillingService:
    """Service class for billing-related operations"""
    
    def __init__(self):
        self.bills: Dict[str, Billing] = {}
    
    def generate_bill(self, patient: Patient) -> Optional[Billing]:
        """Generate a bill for a patient"""
        try:
            bill = Billing(patient)
            self.bills[bill.bill_id] = bill
            return bill
        except Exception as e:
            print(f"Error generating bill: {str(e)}")
            return None
    
    def add_charges(self, bill_id: str, service_name: str, cost: float) -> bool:
        """Add charges to a bill"""
        try:
            bill = self.bills.get(bill_id)
            if bill is None:
                raise Exception(f"Bill {bill_id} not found")
            
            bill.add_service(service_name, cost)
            return True
        except Exception as e:
            print(f"Error adding charges: {str(e)}")
            return False
    
    def process_payment(self, bill_id: str, amount: float) -> bool:
        """Process payment for a bill"""
        try:
            bill = self.bills.get(bill_id)
            if bill is None:
                raise Exception(f"Bill {bill_id} not found")
            
            if amount <= 0:
                raise Exception("Payment amount must be greater than 0")
            
            bill.process_payment(amount)
            return True
        except Exception as e:
            print(f"Error processing payment: {str(e)}")
            return False
    
    def get_billing_report(self, patient: Patient) -> Dict:
        """Get billing report for a patient"""
        report = {
            "patient_name": patient.name,
            "patient_id": patient.patient_id,
            "total_bills": 0,
            "total_charged": 0.0,
            "total_paid": 0.0,
            "total_pending": 0.0,
            "bills": []
        }
        
        for bill in self.bills.values():
            if bill.patient == patient:
                report["total_bills"] += 1
                report["total_charged"] += bill.total_amount
                report["total_paid"] += bill.paid_amount
                report["total_pending"] += bill.pending_amount
                report["bills"].append({
                    "bill_id": bill.bill_id,
                    "date": bill.bill_date.strftime("%Y-%m-%d"),
                    "amount": bill.total_amount,
                    "paid": bill.paid_amount,
                    "pending": bill.pending_amount,
                    "status": bill.payment_status.value
                })
        
        return report
    
    def get_bill_details(self, bill_id: str) -> Optional[Billing]:
        """Get bill details by ID"""
        return self.bills.get(bill_id)


# ==================== DISCHARGE SERVICE ====================
class DischargeService:
    """Service class for discharge-related operations"""
    
    def __init__(self, patient_service: PatientService):
        self.patient_service = patient_service
    
    def initiate_discharge(self, patient_id: str) -> bool:
        """Initiate discharge for a patient"""
        return self.patient_service.discharge_patient(patient_id)
    
    def generate_discharge_summary(self, patient: Patient) -> str:
        """Generate a discharge summary for a patient"""
        summary = f"""
        ========== DISCHARGE SUMMARY ==========
        Patient Name: {patient.name}
        Patient ID: {patient.patient_id}
        Age: {patient.age}
        Gender: {patient.gender}
        
        ---- HOSPITALIZATION DETAILS ----
        Admission Date: {patient.admission_date.strftime("%Y-%m-%d %H:%M:%S") if patient.admission_date else "N/A"}
        Discharge Date: {patient.discharge_date.strftime("%Y-%m-%d %H:%M:%S") if patient.discharge_date else "N/A"}
        Status: {patient.status.value.upper()}
        """
        
        if patient.assigned_doctor:
            summary += f"\nAssigned Doctor: Dr. {patient.assigned_doctor.name} ({patient.assigned_doctor.specialization})"
        
        if patient.diagnoses:
            summary += "\n\n---- DIAGNOSES ----\n"
            for diagnosis in patient.diagnoses:
                summary += f"- {diagnosis.diagnosis_name} (Severity: {diagnosis.get_severity()})\n"
        
        if patient.prescriptions:
            summary += "\n---- PRESCRIPTIONS ----\n"
            for prescription in patient.prescriptions:
                summary += f"Prescription ID: {prescription.prescription_id}\n"
                for medicine in prescription.get_medicines():
                    summary += f"  - {medicine['name']}: {medicine['dosage']}, {medicine['frequency']} for {medicine['duration']}\n"
        
        summary += "\n========================================\n"
        return summary
    
    def schedule_follow_up(self, patient: Patient, follow_up_date: str) -> str:
        """Schedule a follow-up appointment after discharge"""
        return f"Follow-up appointment scheduled for {patient.name} on {follow_up_date}"
