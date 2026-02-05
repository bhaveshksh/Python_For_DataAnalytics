"""
Hospital Management System - Model Classes
Core entity classes for the hospital management system
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict


class PatientStatus(Enum):
    """Enum for patient admission status"""
    ADMITTED = "admitted"
    DISCHARGED = "discharged"
    OUTPATIENT = "outpatient"


class AppointmentStatus(Enum):
    """Enum for appointment status"""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


class PaymentStatus(Enum):
    """Enum for payment status"""
    PENDING = "pending"
    PARTIAL = "partial"
    COMPLETE = "complete"


class SeverityLevel(Enum):
    """Enum for diagnosis severity"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ==================== HOSPITAL ====================
class Hospital:
    """Represents a hospital entity"""
    
    def __init__(self, hospital_id: str, name: str, address: str, phone: str, email: str):
        self.hospital_id = hospital_id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.departments: List['Department'] = []
        self.total_beds = 100
        self.available_beds = 100
    
    def add_department(self, department: 'Department') -> None:
        """Add a department to the hospital"""
        if department not in self.departments:
            self.departments.append(department)
    
    def get_department(self, dept_id: str) -> Optional['Department']:
        """Get department by ID"""
        for dept in self.departments:
            if dept.dept_id == dept_id:
                return dept
        return None
    
    def update_available_beds(self, delta: int) -> None:
        """Update available beds count"""
        self.available_beds += delta
        if self.available_beds > self.total_beds:
            self.available_beds = self.total_beds
        elif self.available_beds < 0:
            self.available_beds = 0
    
    def __str__(self):
        return f"Hospital({self.name}, Beds: {self.available_beds}/{self.total_beds})"


# ==================== DEPARTMENT ====================
class Department:
    """Represents a hospital department"""
    
    def __init__(self, dept_id: str, name: str, description: str):
        self.dept_id = dept_id
        self.name = name
        self.description = description
        self.doctors: List['Doctor'] = []
        self.head_doctor: Optional['Doctor'] = None
    
    def add_doctor(self, doctor: 'Doctor') -> None:
        """Add a doctor to the department"""
        if doctor not in self.doctors:
            self.doctors.append(doctor)
            doctor.department = self
    
    def get_doctors(self) -> List['Doctor']:
        """Get all doctors in the department"""
        return self.doctors
    
    def remove_doctor(self, doctor_id: str) -> bool:
        """Remove a doctor from the department"""
        for doctor in self.doctors:
            if doctor.doctor_id == doctor_id:
                self.doctors.remove(doctor)
                return True
        return False
    
    def set_head_doctor(self, doctor: 'Doctor') -> None:
        """Set the head/chief of the department"""
        if doctor in self.doctors:
            self.head_doctor = doctor
    
    def __str__(self):
        return f"Department({self.name}, Doctors: {len(self.doctors)})"


# ==================== DOCTOR ====================
class Doctor:
    """Represents a doctor entity"""
    
    def __init__(self, doctor_id: str, name: str, specialization: str, phone: str, email: str):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.phone = phone
        self.email = email
        self.department: Optional['Department'] = None
        self.availability_schedule: Dict[str, str] = {}  # {day: time_slot}
        self.patients: List['Patient'] = []
    
    def is_available(self, date_time: str) -> bool:
        """Check if doctor is available at given date/time"""
        # Simple implementation - can be enhanced with actual scheduling logic
        return True
    
    def add_patient(self, patient: 'Patient') -> None:
        """Add a patient to the doctor's patient list"""
        if patient not in self.patients:
            self.patients.append(patient)
    
    def get_patients(self) -> List['Patient']:
        """Get all patients assigned to this doctor"""
        return self.patients
    
    def set_availability(self, day: str, time_slot: str) -> None:
        """Set availability for a specific day"""
        self.availability_schedule[day] = time_slot
    
    def __str__(self):
        return f"Doctor({self.name}, {self.specialization}, Patients: {len(self.patients)})"


# ==================== PATIENT ====================
class Patient:
    """Represents a patient entity"""
    
    def __init__(self, patient_id: str, name: str, age: int, gender: str, phone: str, email: str, address: str):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address
        self.medical_history: List[str] = []
        self.admission_date: Optional[datetime] = None
        self.discharge_date: Optional[datetime] = None
        self.status = PatientStatus.OUTPATIENT
        self.assigned_doctor: Optional['Doctor'] = None
        self.diagnoses: List['Diagnosis'] = []
        self.prescriptions: List['Prescription'] = []
    
    def admit(self, assigned_doctor: 'Doctor') -> None:
        """Admit patient to the hospital"""
        self.status = PatientStatus.ADMITTED
        self.admission_date = datetime.now()
        self.assigned_doctor = assigned_doctor
        assigned_doctor.add_patient(self)
    
    def discharge(self) -> None:
        """Discharge patient from the hospital"""
        self.status = PatientStatus.DISCHARGED
        self.discharge_date = datetime.now()
    
    def add_diagnosis(self, diagnosis: 'Diagnosis') -> None:
        """Add a diagnosis record"""
        if diagnosis not in self.diagnoses:
            self.diagnoses.append(diagnosis)
    
    def add_prescription(self, prescription: 'Prescription') -> None:
        """Add a prescription"""
        if prescription not in self.prescriptions:
            self.prescriptions.append(prescription)
    
    def get_medical_history(self) -> List[str]:
        """Get patient's medical history"""
        return self.medical_history
    
    def add_medical_history(self, entry: str) -> None:
        """Add an entry to medical history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.medical_history.append(f"[{timestamp}] {entry}")
    
    def __str__(self):
        return f"Patient({self.name}, Age: {self.age}, Status: {self.status.value})"


# ==================== APPOINTMENT ====================
class Appointment:
    """Represents an appointment between patient and doctor"""
    
    counter = 1000
    
    def __init__(self, patient: 'Patient', doctor: 'Doctor', appointment_date_time: str, reason: str):
        self.appointment_id = f"APT{Appointment.counter}"
        Appointment.counter += 1
        self.patient = patient
        self.doctor = doctor
        self.appointment_date_time = appointment_date_time
        self.reason = reason
        self.status = AppointmentStatus.SCHEDULED
        self.notes = ""
    
    def reschedule(self, new_date_time: str) -> None:
        """Reschedule the appointment"""
        self.appointment_date_time = new_date_time
        self.status = AppointmentStatus.RESCHEDULED
    
    def cancel(self) -> None:
        """Cancel the appointment"""
        self.status = AppointmentStatus.CANCELLED
    
    def mark_completed(self) -> None:
        """Mark appointment as completed"""
        self.status = AppointmentStatus.COMPLETED
    
    def add_notes(self, notes: str) -> None:
        """Add notes to the appointment"""
        self.notes = notes
    
    def __str__(self):
        return f"Appointment({self.appointment_id}, {self.patient.name} with Dr. {self.doctor.name}, {self.appointment_date_time})"


# ==================== DIAGNOSIS ====================
class Diagnosis:
    """Represents a diagnosis record"""
    
    counter = 5000
    
    def __init__(self, patient: 'Patient', doctor: 'Doctor', diagnosis_name: str, 
                 description: str, severity_level: SeverityLevel):
        self.diagnosis_id = f"DIG{Diagnosis.counter}"
        Diagnosis.counter += 1
        self.patient = patient
        self.doctor = doctor
        self.diagnosis_name = diagnosis_name
        self.description = description
        self.severity_level = severity_level
        self.diagnosis_date = datetime.now()
    
    def update_diagnosis(self, diagnosis_name: str, description: str, severity_level: SeverityLevel) -> None:
        """Update diagnosis information"""
        self.diagnosis_name = diagnosis_name
        self.description = description
        self.severity_level = severity_level
    
    def get_severity(self) -> str:
        """Get severity level as string"""
        return self.severity_level.value
    
    def __str__(self):
        return f"Diagnosis({self.diagnosis_id}, {self.diagnosis_name}, Severity: {self.severity_level.value})"


# ==================== PRESCRIPTION ====================
class Prescription:
    """Represents a prescription for medicines"""
    
    counter = 8000
    
    def __init__(self, patient: 'Patient', doctor: 'Doctor', diagnosis: 'Diagnosis'):
        self.prescription_id = f"PRE{Prescription.counter}"
        Prescription.counter += 1
        self.patient = patient
        self.doctor = doctor
        self.diagnosis = diagnosis
        self.medicines: List[Dict[str, str]] = []  # List of {medicine_name, dosage, frequency, duration}
        self.issued_date = datetime.now()
        self.expiry_date: Optional[datetime] = None
    
    def add_medicine(self, medicine_name: str, dosage: str, frequency: str, duration: str) -> None:
        """Add a medicine to the prescription"""
        medicine = {
            "name": medicine_name,
            "dosage": dosage,
            "frequency": frequency,
            "duration": duration
        }
        self.medicines.append(medicine)
    
    def remove_medicine(self, medicine_name: str) -> bool:
        """Remove a medicine from the prescription"""
        for medicine in self.medicines:
            if medicine["name"] == medicine_name:
                self.medicines.remove(medicine)
                return True
        return False
    
    def get_medicines(self) -> List[Dict[str, str]]:
        """Get all medicines in the prescription"""
        return self.medicines
    
    def is_valid(self) -> bool:
        """Check if prescription is still valid"""
        if self.expiry_date is None:
            return True
        return datetime.now() <= self.expiry_date
    
    def set_expiry_date(self, expiry_date: datetime) -> None:
        """Set prescription expiry date"""
        self.expiry_date = expiry_date
    
    def __str__(self):
        return f"Prescription({self.prescription_id}, {len(self.medicines)} medicines)"


# ==================== BILLING ====================
class Billing:
    """Represents a billing record for a patient"""
    
    counter = 9000
    
    def __init__(self, patient: 'Patient', bill_date: datetime = None):
        self.bill_id = f"BIL{Billing.counter}"
        Billing.counter += 1
        self.patient = patient
        self.bill_date = bill_date or datetime.now()
        self.services: List[Dict[str, float]] = []  # List of {service_name, cost}
        self.medicines_cost = 0.0
        self.consultation_fee = 500.0
        self.room_charges = 0.0
        self.total_amount = 0.0
        self.paid_amount = 0.0
        self.pending_amount = 0.0
        self.payment_status = PaymentStatus.PENDING
    
    def add_service(self, service_name: str, cost: float) -> None:
        """Add a service to the bill"""
        service = {"service": service_name, "cost": cost}
        self.services.append(service)
        self.calculate_total()
    
    def add_medicine_cost(self, cost: float) -> None:
        """Add medicine cost to the bill"""
        self.medicines_cost += cost
        self.calculate_total()
    
    def add_room_charges(self, cost: float) -> None:
        """Add room charges to the bill"""
        self.room_charges += cost
        self.calculate_total()
    
    def calculate_total(self) -> float:
        """Calculate total bill amount"""
        services_total = sum(service["cost"] for service in self.services)
        self.total_amount = services_total + self.medicines_cost + self.consultation_fee + self.room_charges
        self.pending_amount = self.total_amount - self.paid_amount
        
        if self.pending_amount == 0:
            self.payment_status = PaymentStatus.COMPLETE
        elif self.paid_amount > 0:
            self.payment_status = PaymentStatus.PARTIAL
        else:
            self.payment_status = PaymentStatus.PENDING
        
        return self.total_amount
    
    def process_payment(self, amount: float) -> bool:
        """Process a payment"""
        if amount > 0:
            self.paid_amount += amount
            self.calculate_total()
            return True
        return False
    
    def generate_receipt(self) -> str:
        """Generate a bill receipt"""
        receipt = f"""
        ========== HOSPITAL BILL RECEIPT ==========
        Bill ID: {self.bill_id}
        Patient: {self.patient.name}
        Bill Date: {self.bill_date.strftime("%Y-%m-%d %H:%M:%S")}
        
        ---- CHARGES BREAKDOWN ----
        Consultation Fee: Rs. {self.consultation_fee:.2f}
        Medicines Cost: Rs. {self.medicines_cost:.2f}
        Room Charges: Rs. {self.room_charges:.2f}
        """
        
        if self.services:
            receipt += "\nServices:\n"
            for service in self.services:
                receipt += f"  - {service['service']}: Rs. {service['cost']:.2f}\n"
        
        receipt += f"""
        ---- PAYMENT SUMMARY ----
        Total Amount: Rs. {self.total_amount:.2f}
        Paid Amount: Rs. {self.paid_amount:.2f}
        Pending Amount: Rs. {self.pending_amount:.2f}
        Payment Status: {self.payment_status.value.upper()}
        ==========================================
        """
        return receipt
    
    def __str__(self):
        return f"Billing({self.bill_id}, Total: Rs. {self.total_amount:.2f}, Status: {self.payment_status.value})"
