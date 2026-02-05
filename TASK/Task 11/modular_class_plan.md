# Modular Class-Based Hospital Management System - Implementation Plan

## Project Architecture Overview

This document outlines a **modular, class-based architecture** for the Hospital Management System, emphasizing separation of concerns, reusability, and maintainability.

---

## 1. Project Structure

```
hospital_management/
├── models/
│   ├── __init__.py
│   ├── hospital.py
│   ├── department.py
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   ├── prescription.py
│   ├── billing.py
│   └── diagnosis.py
│
├── services/
│   ├── __init__.py
│   ├── patient_service.py
│   ├── appointment_service.py
│   ├── diagnosis_service.py
│   ├── prescription_service.py
│   ├── billing_service.py
│   └── discharge_service.py
│
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py
│   ├── patient_repository.py
│   ├── doctor_repository.py
│   ├── appointment_repository.py
│   └── billing_repository.py
│
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   ├── constants.py
│   └── exceptions.py
│
├── ui/
│   ├── __init__.py
│   └── cli_interface.py
│
├── main.py
├── config.py
└── README.md
```

---

## 2. Core Classes & Responsibilities

### 2.1 Model Classes (`models/`)

#### **Hospital** (`hospital.py`)
- **Attributes**: 
  - `hospital_id`, `name`, `address`, `phone`, `email`
  - `departments` (list of Department objects)
  - `total_beds`, `available_beds`
- **Methods**:
  - `add_department(department)`
  - `get_department(dept_id)`
  - `update_available_beds(delta)`

#### **Department** (`department.py`)
- **Attributes**: 
  - `dept_id`, `name`, `description`
  - `doctors` (list of Doctor objects)
  - `head_doctor` (Doctor object)
- **Methods**:
  - `add_doctor(doctor)`
  - `get_doctors()`
  - `remove_doctor(doctor_id)`

#### **Doctor** (`doctor.py`)
- **Attributes**: 
  - `doctor_id`, `name`, `specialization`, `phone`, `email`
  - `department` (Department object)
  - `availability_schedule`
  - `patients` (list of Patient objects)
- **Methods**:
  - `is_available(date_time)`
  - `add_patient(patient)`
  - `get_patients()`

#### **Patient** (`patient.py`)
- **Attributes**: 
  - `patient_id`, `name`, `age`, `gender`, `phone`, `email`
  - `address`, `medical_history`
  - `admission_date`, `discharge_date`, `status` (admitted/discharged)
  - `assigned_doctor` (Doctor object)
  - `diagnoses` (list of Diagnosis objects)
  - `prescriptions` (list of Prescription objects)
- **Methods**:
  - `admit(assigned_doctor)`
  - `discharge()`
  - `add_diagnosis(diagnosis)`
  - `add_prescription(prescription)`
  - `get_medical_history()`

#### **Appointment** (`appointment.py`)
- **Attributes**: 
  - `appointment_id`, `patient` (Patient), `doctor` (Doctor)
  - `appointment_date_time`, `reason`, `status` (scheduled/completed/cancelled)
  - `notes`
- **Methods**:
  - `reschedule(new_date_time)`
  - `cancel()`
  - `mark_completed()`

#### **Diagnosis** (`diagnosis.py`)
- **Attributes**: 
  - `diagnosis_id`, `patient` (Patient), `doctor` (Doctor)
  - `diagnosis_name`, `description`, `severity_level`
  - `diagnosis_date`
- **Methods**:
  - `update_diagnosis(new_info)`
  - `get_severity()`

#### **Prescription** (`prescription.py`)
- **Attributes**: 
  - `prescription_id`, `patient` (Patient), `doctor` (Doctor)
  - `medicines` (list of {medicine_name, dosage, frequency, duration})
  - `diagnosis` (Diagnosis object)
  - `issued_date`, `expiry_date`
- **Methods**:
  - `add_medicine(medicine_name, dosage, frequency, duration)`
  - `remove_medicine(medicine_name)`
  - `is_valid()`
  - `get_medicines()`

#### **Billing** (`billing.py`)
- **Attributes**: 
  - `bill_id`, `patient` (Patient), `bill_date`
  - `services` (list of {service_name, cost})
  - `medicines_cost`, `consultation_fee`, `room_charges`
  - `total_amount`, `paid_amount`, `pending_amount`
  - `payment_status` (pending/partial/complete)
- **Methods**:
  - `add_service(service_name, cost)`
  - `calculate_total()`
  - `process_payment(amount)`
  - `generate_receipt()`

---

## 3. Service Layer (`services/`)

The service layer contains business logic and orchestrates interactions between models.

#### **PatientService** (`patient_service.py`)
- `admit_patient(patient_data, doctor_id)`
- `discharge_patient(patient_id)`
- `get_patient_details(patient_id)`
- `update_patient_info(patient_id, new_data)`

#### **AppointmentService** (`appointment_service.py`)
- `schedule_appointment(patient_id, doctor_id, date_time, reason)`
- `reschedule_appointment(appointment_id, new_date_time)`
- `cancel_appointment(appointment_id)`
- `get_doctor_appointments(doctor_id, date)`

#### **DiagnosisService** (`diagnosis_service.py`)
- `record_diagnosis(patient_id, doctor_id, diagnosis_data)`
- `get_patient_diagnoses(patient_id)`
- `update_diagnosis(diagnosis_id, new_info)`

#### **PrescriptionService** (`prescription_service.py`)
- `create_prescription(patient_id, doctor_id, diagnosis_id, medicines)`
- `get_patient_prescriptions(patient_id)`
- `add_medicine_to_prescription(prescription_id, medicine_data)`

#### **BillingService** (`billing_service.py`)
- `generate_bill(patient_id)`
- `add_charges(bill_id, service_name, cost)`
- `process_payment(bill_id, amount)`
- `get_billing_report(patient_id)`

#### **DischargeService** (`discharge_service.py`)
- `initiate_discharge(patient_id)`
- `generate_discharge_summary(patient_id)`
- `schedule_follow_up(patient_id, follow_up_date)`

---

## 4. Repository Layer (`repositories/`)

Handles data persistence and retrieval (in-memory or database).

#### **BaseRepository** (`base_repository.py`)
- Abstract base class with CRUD operations:
  - `create(entity)`
  - `read(entity_id)`
  - `update(entity_id, data)`
  - `delete(entity_id)`
  - `get_all()`

#### **Specialized Repositories**
- `PatientRepository` - Manage patient data
- `DoctorRepository` - Manage doctor data
- `AppointmentRepository` - Manage appointments
- `BillingRepository` - Manage billing records

---

## 5. Utilities & Helpers (`utils/`)

#### **Exceptions** (`exceptions.py`)
- `PatientNotFoundException`
- `DoctorNotFoundException`
- `AppointmentConflictException`
- `InvalidPrescriptionException`
- `BillingException`

#### **Validators** (`validators.py`)
- `validate_email(email)`
- `validate_phone(phone)`
- `validate_age(age)`
- `validate_date_format(date_string)`

#### **Constants** (`constants.py`)
- `HOSPITAL_NAME`, `MAX_BEDS`, `CONSULTATION_FEE`
- `APPOINTMENT_DURATION`, `PRESCRIPTION_VALIDITY_DAYS`
- `SEVERITY_LEVELS = ['Low', 'Medium', 'High', 'Critical']`

---

## 6. User Interface (`ui/`)

#### **CLI Interface** (`cli_interface.py`)
- Menu-driven interface for:
  - Patient admission and discharge
  - Appointment scheduling
  - Diagnosis and prescription management
  - Billing operations
  - Reporting and queries

---

## 7. Implementation Workflow

### Phase 1: Core Models
1. Implement all model classes with attributes and basic methods
2. Define class relationships and dependencies
3. Add data validation in model constructors

### Phase 2: Repository Layer
1. Create base repository with CRUD operations
2. Implement specialized repositories for each model
3. Add in-memory data storage (can upgrade to database later)

### Phase 3: Service Layer
1. Implement business logic services
2. Add error handling and validation
3. Orchestrate cross-model operations

### Phase 4: User Interface
1. Build CLI menu system
2. Connect services to UI
3. Add input validation and error messages

### Phase 5: Testing & Documentation
1. Unit tests for each class
2. Integration tests for workflows
3. Code documentation and usage examples

---

## 8. Design Principles Applied

- **Separation of Concerns**: Models, Services, and Repositories are distinct
- **DRY (Don't Repeat Yourself)**: BaseRepository for common operations
- **Single Responsibility**: Each class has one primary responsibility
- **Modularity**: Easy to extend and modify individual components
- **Error Handling**: Custom exceptions for specific scenarios
- **Reusability**: Services can be used by CLI, API, or GUI

---

## 9. Data Flow Example: Patient Admission

```
User Input (CLI)
    ↓
PatientService.admit_patient()
    ↓
Create Patient Model
    ↓
PatientRepository.create()
    ↓
Update Doctor's patient list
    ↓
Update Hospital's available beds
    ↓
Return success/confirmation to UI
```

---

## 10. Future Enhancements

- Database integration (SQLite, MySQL, PostgreSQL)
- RESTful API layer
- Web-based GUI (Flask/Django)
- Automated email/SMS notifications
- Advanced reporting and analytics
- Multi-user authentication and authorization

---

**Status**: Ready for Implementation
**Next Step**: Start with Phase 1 - Core Models Implementation
