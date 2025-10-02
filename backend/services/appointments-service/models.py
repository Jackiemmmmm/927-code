import uuid

from sqlmodel import Field, Relationship, SQLModel


# Hospital models
class HospitalBase(SQLModel):
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)


class HospitalCreate(HospitalBase):
    pass


class Hospital(HospitalBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    doctors: list["Doctor"] = Relationship(back_populates="hospital", cascade_delete=True)


class HospitalPublic(HospitalBase):
    id: uuid.UUID


class HospitalsPublic(SQLModel):
    data: list[HospitalPublic]
    count: int


# Doctor models
class DoctorBase(SQLModel):
    name: str = Field(max_length=255)
    specialty: str = Field(max_length=255)
    rating: float = Field(default=0.0, ge=0.0, le=5.0)


class DoctorCreate(DoctorBase):
    hospital_id: uuid.UUID


class Doctor(DoctorBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hospital_id: uuid.UUID = Field(
        foreign_key="hospital.id", nullable=False, ondelete="CASCADE"
    )
    hospital: Hospital | None = Relationship(back_populates="doctors")
    time_slots: list["DoctorTimeSlot"] = Relationship(back_populates="doctor", cascade_delete=True)
    appointments: list["Appointment"] = Relationship(back_populates="doctor", cascade_delete=True)


class DoctorPublic(DoctorBase):
    id: uuid.UUID
    hospital_id: uuid.UUID


class DoctorsPublic(SQLModel):
    data: list[DoctorPublic]
    count: int


# Doctor time slot models
class DoctorTimeSlotBase(SQLModel):
    time_slot: str = Field(max_length=50)
    is_available: bool = Field(default=True)


class DoctorTimeSlotCreate(DoctorTimeSlotBase):
    doctor_id: uuid.UUID


class DoctorTimeSlot(DoctorTimeSlotBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    doctor_id: uuid.UUID = Field(
        foreign_key="doctor.id", nullable=False, ondelete="CASCADE"
    )
    doctor: Doctor | None = Relationship(back_populates="time_slots")


class DoctorTimeSlotPublic(DoctorTimeSlotBase):
    id: uuid.UUID
    doctor_id: uuid.UUID


# Appointment models
class AppointmentBase(SQLModel):
    patient_name: str = Field(max_length=255)
    patient_id_number: str = Field(max_length=100)
    patient_phone: str = Field(max_length=50)
    patient_email: str | None = Field(default=None, max_length=255)
    appointment_time: str = Field(max_length=50)
    status: str = Field(default="pending", max_length=50)


class AppointmentCreate(AppointmentBase):
    hospital_id: uuid.UUID
    doctor_id: uuid.UUID
    user_id: uuid.UUID


class AppointmentUpdate(SQLModel):
    status: str | None = Field(default=None, max_length=50)


class Appointment(AppointmentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    hospital_id: uuid.UUID = Field(
        foreign_key="hospital.id", nullable=False, ondelete="CASCADE"
    )
    doctor_id: uuid.UUID = Field(
        foreign_key="doctor.id", nullable=False, ondelete="CASCADE"
    )
    doctor: Doctor | None = Relationship(back_populates="appointments")


class AppointmentPublic(AppointmentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    hospital_id: uuid.UUID
    doctor_id: uuid.UUID


class AppointmentsPublic(SQLModel):
    data: list[AppointmentPublic]
    count: int


# User validation request
class UserValidation(SQLModel):
    name: str = Field(max_length=255)
    id_number: str = Field(max_length=100, alias="idNumber")
    phone: str = Field(max_length=50)
    email: str | None = Field(default=None, max_length=255)


# Generic message
class Message(SQLModel):
    message: str
