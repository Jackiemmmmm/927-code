import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from models import (
    Appointment,
    AppointmentCreate,
    AppointmentPublic,
    AppointmentsPublic,
    AppointmentUpdate,
    Doctor,
    DoctorsPublic,
    DoctorTimeSlot,
    DoctorTimeSlotPublic,
    Hospital,
    HospitalsPublic,
    Message,
    UserValidation,
)

import sys
sys.path.append('..')
from shared.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/v1/appointments", tags=["appointments"])


@router.post("/validate-user")
def validate_user(*, user_info: UserValidation) -> Message:
    """
    Validate user information before booking.
    """
    if len(user_info.name) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
    if len(user_info.id_number) < 10:
        raise HTTPException(
            status_code=400, detail="ID number must be at least 10 characters"
        )
    if len(user_info.phone) < 10:
        raise HTTPException(
            status_code=400, detail="Phone number must be at least 10 characters"
        )
    return Message(message="User validation successful")


@router.get("/hospitals", response_model=HospitalsPublic)
def get_hospitals(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get list of all hospitals.
    """
    count_statement = select(func.count()).select_from(Hospital)
    count = session.exec(count_statement).one()
    statement = select(Hospital).offset(skip).limit(limit)
    hospitals = session.exec(statement).all()
    return HospitalsPublic(data=hospitals, count=count)


@router.get("/hospitals/{hospital_id}/doctors", response_model=DoctorsPublic)
def get_hospital_doctors(
    session: SessionDep, hospital_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get list of doctors for a specific hospital.
    """
    hospital = session.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    count_statement = (
        select(func.count()).select_from(Doctor).where(Doctor.hospital_id == hospital_id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Doctor)
        .where(Doctor.hospital_id == hospital_id)
        .offset(skip)
        .limit(limit)
    )
    doctors = session.exec(statement).all()
    return DoctorsPublic(data=doctors, count=count)


@router.get("/doctors/{doctor_id}/time-slots")
def get_doctor_time_slots(
    session: SessionDep, doctor_id: uuid.UUID
) -> list[DoctorTimeSlotPublic]:
    """
    Get available time slots for a specific doctor.
    """
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    statement = select(DoctorTimeSlot).where(
        DoctorTimeSlot.doctor_id == doctor_id,
        DoctorTimeSlot.is_available == True,  # noqa: E712
    )
    time_slots = session.exec(statement).all()
    return [DoctorTimeSlotPublic.model_validate(slot) for slot in time_slots]


@router.post("/", response_model=AppointmentPublic)
def create_appointment(
    *, session: SessionDep, appointment_in: AppointmentCreate
) -> Any:
    """
    Create a new appointment.
    """
    hospital = session.get(Hospital, appointment_in.hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    doctor = session.get(Doctor, appointment_in.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if doctor.hospital_id != appointment_in.hospital_id:
        raise HTTPException(
            status_code=400, detail="Doctor does not belong to the selected hospital"
        )

    time_slot_statement = select(DoctorTimeSlot).where(
        DoctorTimeSlot.doctor_id == appointment_in.doctor_id,
        DoctorTimeSlot.time_slot == appointment_in.appointment_time,
        DoctorTimeSlot.is_available == True,  # noqa: E712
    )
    time_slot = session.exec(time_slot_statement).first()
    if not time_slot:
        raise HTTPException(
            status_code=400, detail="Selected time slot is not available"
        )

    appointment = Appointment.model_validate(appointment_in)
    session.add(appointment)

    time_slot.is_available = False
    session.add(time_slot)

    session.commit()
    session.refresh(appointment)
    return appointment


@router.get("/", response_model=AppointmentsPublic)
def get_appointments(
    session: SessionDep, user_id: uuid.UUID | None = None, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get list of appointments.
    """
    if user_id:
        count_statement = (
            select(func.count())
            .select_from(Appointment)
            .where(Appointment.user_id == user_id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Appointment)
            .where(Appointment.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
    else:
        count_statement = select(func.count()).select_from(Appointment)
        count = session.exec(count_statement).one()
        statement = select(Appointment).offset(skip).limit(limit)

    appointments = session.exec(statement).all()
    return AppointmentsPublic(data=appointments, count=count)


@router.get("/{appointment_id}", response_model=AppointmentPublic)
def get_appointment(session: SessionDep, appointment_id: uuid.UUID) -> Any:
    """
    Get appointment details by ID.
    """
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentPublic)
def update_appointment(
    *,
    session: SessionDep,
    appointment_id: uuid.UUID,
    appointment_in: AppointmentUpdate,
) -> Any:
    """
    Update an appointment.
    """
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment_in.status == "cancelled":
        time_slot_statement = select(DoctorTimeSlot).where(
            DoctorTimeSlot.doctor_id == appointment.doctor_id,
            DoctorTimeSlot.time_slot == appointment.appointment_time,
        )
        time_slot = session.exec(time_slot_statement).first()
        if time_slot:
            time_slot.is_available = True
            session.add(time_slot)

    update_dict = appointment_in.model_dump(exclude_unset=True)
    appointment.sqlmodel_update(update_dict)
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(session: SessionDep, appointment_id: uuid.UUID) -> Message:
    """
    Delete an appointment.
    """
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    time_slot_statement = select(DoctorTimeSlot).where(
        DoctorTimeSlot.doctor_id == appointment.doctor_id,
        DoctorTimeSlot.time_slot == appointment.appointment_time,
    )
    time_slot = session.exec(time_slot_statement).first()
    if time_slot:
        time_slot.is_available = True
        session.add(time_slot)

    session.delete(appointment)
    session.commit()
    return Message(message="Appointment deleted successfully")
