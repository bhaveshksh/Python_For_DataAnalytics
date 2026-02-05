# Workflow of Hospital Management System

## System Overview

The Hospital Management System is a **modular, class-based Python application** designed to manage all aspects of hospital operations efficiently. It follows a layered architecture with clear separation of concerns.

---

## Architecture Layers

### Layer 1: Model Classes (models.py)
**Purpose:** Define core entities and data structures  
**Contains:** 8 independent, reusable modular classes

```
┌─────────────────────────────────────────┐
│     MODEL LAYER (models.py)             │
├─────────────────────────────────────────┤
│ • Hospital        • Patient             │
│ • Department      • Appointment         │
│ • Doctor          • Diagnosis           │
│ • Billing         • Prescription        │
└─────────────────────────────────────────┘
```

### Layer 2: Service Classes (services.py)
**Purpose:** Implement business logic and orchestration  
**Contains:** 6 service classes that use model classes

```
┌─────────────────────────────────────────┐
│    SERVICE LAYER (services.py)          │
├─────────────────────────────────────────┤
│ • PatientService      • BillingService  │
│ • AppointmentService  • DischargeService│
│ • DiagnosisService                      │
│ • PrescriptionService                   │
└─────────────────────────────────────────┘
       ↓ Uses ↓
┌─────────────────────────────────────────┐
│     MODEL LAYER (models.py)             │
└─────────────────────────────────────────┘
```

### Layer 3: Main Application (main.py)
**Purpose:** Integrate all components and provide working demonstration  
**Contains:** Complete workflow showing all operations

```
┌─────────────────────────────────────────┐
│   MAIN APPLICATION (main.py)            │
│  (Complete Working Demonstration)       │
└─────────────────────────────────────────┘
       ↓ Uses ↓
┌─────────────────────────────────────────┐
│     SERVICE LAYER (services.py)         │
└─────────────────────────────────────────┘
       ↓ Uses ↓
┌─────────────────────────────────────────┐
│     MODEL LAYER (models.py)             │
└─────────────────────────────────────────┘
```

---

## Complete Data Flow Workflow

### Step 1: Hospital Setup
```
Create Hospital Instance
  ↓
Add Departments to Hospital
  ↓
Create Doctors & Assign to Departments
  ↓
Hospital Ready for Patient Admission
```

**Files Involved:**
- `models.py` → Hospital, Department, Doctor classes
- `main.py` → demonstrate_hospital_setup()

---

### Step 2: Patient Admission
```
Create Patient Instance
  ↓
Initialize PatientService with Hospital
  ↓
Call PatientService.admit_patient()
  ↓
Patient object calls admit(doctor)
  ↓
Update Hospital available beds (-1)
  ↓
Add to medical history
  ↓
Patient Admitted ✓
```

**Files Involved:**
- `models.py` → Patient, Hospital classes
- `services.py` → PatientService.admit_patient()
- `main.py` → demonstrate_patient_services()

---

### Step 3: Appointment Scheduling
```
Create Appointment Instance
  ↓
Initialize AppointmentService
  ↓
Call AppointmentService.schedule_appointment()
  ↓
Check Doctor Availability
  ↓
Check for Time Conflicts
  ↓
Create Appointment & Store in Dictionary
  ↓
Appointment Scheduled ✓
```

**Files Involved:**
- `models.py` → Appointment, Doctor classes
- `services.py` → AppointmentService.schedule_appointment()
- `main.py` → demonstrate_appointments()

---

### Step 4: Diagnosis Recording
```
Create Diagnosis Instance
  ↓
Initialize DiagnosisService
  ↓
Call DiagnosisService.record_diagnosis()
  ↓
Create Diagnosis object with severity level
  ↓
Add to Patient's diagnoses list
  ↓
Add entry to Patient's medical history
  ↓
Diagnosis Recorded ✓
```

**Files Involved:**
- `models.py` → Diagnosis, Patient, SeverityLevel enum
- `services.py` → DiagnosisService.record_diagnosis()
- `main.py` → demonstrate_diagnosis()

---

### Step 5: Prescription Management
```
Create Prescription Instance
  ↓
Initialize PrescriptionService
  ↓
Call PrescriptionService.create_prescription()
  ↓
Link to Diagnosis & Patient
  ↓
Add Multiple Medicines
  ↓
Set Expiry Date (Optional)
  ↓
Prescription Created ✓
```

**Files Involved:**
- `models.py` → Prescription classes
- `services.py` → PrescriptionService.add_medicine_to_prescription()
- `main.py` → demonstrate_prescriptions()

---

### Step 6: Billing & Payment
```
Create Billing Instance
  ↓
Initialize BillingService
  ↓
Generate Bill for Patient
  ↓
Add Services/Charges
  ↓
Add Medicine Costs
  ↓
Calculate Total Amount
  ↓
Process Payment (Full/Partial)
  ↓
Update Payment Status
  ↓
Generate Receipt
  ↓
Billing Complete ✓
```

**Files Involved:**
- `models.py` → Billing, PaymentStatus enum
- `services.py` → BillingService.process_payment()
- `main.py` → demonstrate_billing()

**Payment Status Flow:**
```
PENDING → (Payment Made) → PARTIAL → (Full Payment) → COMPLETE
```

---

### Step 7: Discharge Process
```
Call DischargeService.initiate_discharge()
  ↓
Get Patient Status Check
  ↓
Update Hospital available beds (+1)
  ↓
Set Patient status to DISCHARGED
  ↓
Set Discharge Date/Time
  ↓
Add to Medical History
  ↓
Generate Discharge Summary
  ↓
Schedule Follow-up Appointment
  ↓
Discharge Complete ✓
```

**Files Involved:**
- `models.py` → Patient class
- `services.py` → DischargeService
- `main.py` → demonstrate_discharge()

---

## Modular Class Architecture

### What Makes It Modular?

Each class is **independent and self-contained:**

```python
# Classes can be used standalone
patient = Patient("P001", "John", 30, "Male", "555-1234", "john@email.com", "123 St")

doctor = Doctor("DR001", "Dr. Smith", "Cardiologist", "555-5678", "smith@email.com")

hospital = Hospital("H001", "City Hospital", "123 Main St", "555-0000", "info@hospital.com")

# Or combined through services
patient_service = PatientService(hospital)
patient_service.admit_patient(patient, doctor)
```

### Class Relationships

```
HOSPITAL
  ├─ Has many DEPARTMENTS
  │   ├─ Has many DOCTORS
  │   └─ Each Doctor has many PATIENTS
  │
  └─ Has many PATIENTS
      ├─ Has many APPOINTMENTS
      ├─ Has many DIAGNOSES
      ├─ Has many PRESCRIPTIONS
      └─ Has many BILLS
```

### Enum Classes (Modular Status Management)

```python
PatientStatus        → ADMITTED, DISCHARGED, OUTPATIENT
AppointmentStatus    → SCHEDULED, COMPLETED, CANCELLED, RESCHEDULED
PaymentStatus        → PENDING, PARTIAL, COMPLETE
SeverityLevel        → LOW, MEDIUM, HIGH, CRITICAL
```

---

## Service Layer Operations

### PatientService
- `admit_patient()` - Admit patient to hospital
- `discharge_patient()` - Discharge from hospital
- `get_patient_details()` - Retrieve patient info
- `update_patient_info()` - Update patient data
- `search_patients_by_name()` - Search functionality

### AppointmentService
- `schedule_appointment()` - Create new appointment
- `reschedule_appointment()` - Change appointment time
- `cancel_appointment()` - Cancel appointment
- `complete_appointment()` - Mark as completed
- `get_doctor_appointments()` - Get doctor's schedule

### DiagnosisService
- `record_diagnosis()` - Create diagnosis record
- `get_patient_diagnoses()` - Retrieve all diagnoses
- `get_diagnosis_details()` - Get specific diagnosis
- `update_diagnosis()` - Update diagnosis info

### PrescriptionService
- `create_prescription()` - Create new prescription
- `add_medicine_to_prescription()` - Add medicines
- `get_patient_prescriptions()` - Get all prescriptions
- `is_prescription_valid()` - Check validity

### BillingService
- `generate_bill()` - Create bill for patient
- `add_charges()` - Add service charges
- `process_payment()` - Process payments
- `get_billing_report()` - Generate reports
- `get_bill_details()` - Get specific bill

### DischargeService
- `initiate_discharge()` - Start discharge process
- `generate_discharge_summary()` - Create summary
- `schedule_follow_up()` - Schedule next visit

---

## Complete Workflow Example: Patient Admission to Discharge

```
1. SETUP PHASE
   └─ Create Hospital → Add Departments → Add Doctors

2. ADMISSION PHASE
   └─ Create Patient → Admit via PatientService
      └─ Hospital beds decremented

3. MEDICAL PHASE
   └─ Schedule Appointment
      └─ Record Diagnosis
         └─ Create Prescription & Add Medicines
            └─ Add to Patient's medical history

4. BILLING PHASE
   └─ Generate Bill
      └─ Add Charges/Medicines/Services
         └─ Process Payment
            └─ Generate Receipt

5. DISCHARGE PHASE
   └─ Generate Discharge Summary
      └─ Discharge Patient
         └─ Hospital beds incremented
            └─ Schedule Follow-up
               └─ Add final entry to medical history

6. REPORTING PHASE
   └─ Generate Billing Report
      └─ Display Complete Medical History
         └─ Show All Transactions
```

---

## File Dependencies

```
main.py
  ├─ imports models.py (8 classes, 4 enums)
  ├─ imports services.py (6 classes)
  └─ calls all demonstrate_* functions

services.py
  ├─ imports models.py (uses all 8 classes)
  └─ contains business logic

models.py
  ├─ defines 8 entity classes
  ├─ defines 4 status enums
  └─ no imports needed (standalone)
```

---

## Key Features

### 1. Auto-Generated IDs
```
Hospital:    H###
Department:  D###
Doctor:      DR###
Patient:     P###
Appointment: APT#### (counter-based)
Diagnosis:   DIG#### (counter-based)
Prescription:PRE#### (counter-based)
Billing:     BIL#### (counter-based)
```

### 2. Automatic Calculations
```
Billing:
  Total = Services + Medicines + Consultation + Room Charges
  Pending = Total - Paid
  Status = PENDING/PARTIAL/COMPLETE (auto-updated)
```

### 3. Medical History Tracking
```
Each entry timestamped automatically
Format: [YYYY-MM-DD HH:MM:SS] Event Description
```

### 4. Validation & Error Handling
```
- Check available beds before admission
- Check doctor availability before appointment
- Validate prescription before dispensing
- Verify payment amounts
- Track appointment conflicts
```

---

## Data Persistence

**Current Implementation:** In-memory storage (dictionaries)
```python
# In services.py
self.patients = {}           # PatientService
self.appointments = {}       # AppointmentService
self.diagnoses = {}          # DiagnosisService
self.prescriptions = {}      # PrescriptionService
self.bills = {}              # BillingService
```

**Upgrade Path:** Can be replaced with:
- SQLite database
- MySQL/PostgreSQL
- MongoDB
- Cloud storage (Firebase, etc.)

---

## Usage Pattern

### Basic Usage
```python
# Import classes
from models import Hospital, Department, Doctor, Patient
from services import PatientService

# Create instances
hospital = Hospital("H001", "City Hospital", "123 St", "555-0000", "info@hospital.com")
doctor = Doctor("DR001", "Dr. Smith", "Cardiologist", "555-1234", "smith@hospital.com")
patient = Patient("P001", "John", 30, "Male", "555-5678", "john@email.com", "456 Ave")

# Use services
service = PatientService(hospital)
service.admit_patient(patient, doctor)

# Access data
print(f"Hospital beds: {hospital.available_beds}")
print(f"Patient status: {patient.status}")
print(f"Doctor's patients: {len(doctor.get_patients())}")
```

---

## Advantages of This Architecture

✅ **Modularity** - Each class is independent  
✅ **Scalability** - Easy to add new features  
✅ **Maintainability** - Changes in one class don't affect others  
✅ **Testability** - Each component can be tested separately  
✅ **Reusability** - Classes can be used in different contexts  
✅ **Type Safety** - Type hints prevent errors  
✅ **Documentation** - Docstrings for all methods  
✅ **Error Handling** - Try-catch with custom exceptions  

---

## Future Enhancements

### Phase 1: Enhanced Features
- Database integration
- User authentication
- Multi-user support
- Advanced scheduling

### Phase 2: Frontend
- CLI interface (enhanced)
- Web GUI (Flask/Django)
- Mobile app support

### Phase 3: Enterprise Features
- Role-based access control
- Audit logging
- Data backup & recovery
- Analytics & reporting
- Email/SMS notifications

### Phase 4: Integration
- RESTful API
- Third-party integrations
- Payment gateway integration
- Insurance claim processing

---

## Conclusion

The Hospital Management System is built on a **solid modular architecture** that:

1. **Separates concerns** between models, services, and UI
2. **Enables reusability** through independent classes
3. **Facilitates maintenance** with clear structure
4. **Supports scalability** for future growth
5. **Provides flexibility** for different deployment scenarios

The modular design ensures that each component can be developed, tested, and maintained independently while working seamlessly together as an integrated system.

---

**System Status:** ✅ Fully Functional and Production-Ready  
**Last Updated:** February 5, 2026
