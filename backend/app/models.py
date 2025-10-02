import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Hospital models
class HospitalBase(SQLModel):
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)


class HospitalCreate(HospitalBase):
    pass


class HospitalUpdate(HospitalBase):
    name: str | None = Field(default=None, max_length=255)  # type: ignore
    address: str | None = Field(default=None, max_length=255)  # type: ignore


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


class DoctorUpdate(DoctorBase):
    name: str | None = Field(default=None, max_length=255)  # type: ignore
    specialty: str | None = Field(default=None, max_length=255)  # type: ignore
    rating: float | None = Field(default=None, ge=0.0, le=5.0)  # type: ignore
    hospital_id: uuid.UUID | None = None  # type: ignore


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
    time_slot: str = Field(max_length=50)  # e.g., "09:00 AM"
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
    status: str = Field(default="pending", max_length=50)  # pending, confirmed, cancelled


class AppointmentCreate(AppointmentBase):
    hospital_id: uuid.UUID
    doctor_id: uuid.UUID


class AppointmentUpdate(SQLModel):
    status: str | None = Field(default=None, max_length=50)  # type: ignore


class Appointment(AppointmentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    hospital_id: uuid.UUID = Field(
        foreign_key="hospital.id", nullable=False, ondelete="CASCADE"
    )
    doctor_id: uuid.UUID = Field(
        foreign_key="doctor.id", nullable=False, ondelete="CASCADE"
    )
    user: User | None = Relationship()
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
