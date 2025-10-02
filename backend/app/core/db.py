from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import (
    Doctor,
    DoctorTimeSlot,
    Hospital,
    User,
    UserCreate,
)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

    # Create initial hospitals if they don't exist
    hospital_count = session.exec(select(Hospital)).first()
    if not hospital_count:
        # Create hospitals
        hospital1 = Hospital(name="City General Hospital", address="123 Main St")
        hospital2 = Hospital(name="St. Mary Medical Center", address="456 Oak Ave")
        hospital3 = Hospital(name="University Hospital", address="789 College Blvd")

        session.add(hospital1)
        session.add(hospital2)
        session.add(hospital3)
        session.commit()
        session.refresh(hospital1)
        session.refresh(hospital2)
        session.refresh(hospital3)

        # Create doctors for hospital 1
        doctor1 = Doctor(
            name="Dr. John Smith",
            specialty="Cardiology",
            rating=4.8,
            hospital_id=hospital1.id,
        )
        doctor2 = Doctor(
            name="Dr. Sarah Johnson",
            specialty="Internal Medicine",
            rating=4.9,
            hospital_id=hospital1.id,
        )
        session.add(doctor1)
        session.add(doctor2)
        session.commit()
        session.refresh(doctor1)
        session.refresh(doctor2)

        # Create time slots for doctor 1
        for time in ["09:00 AM", "10:30 AM", "02:00 PM", "03:30 PM"]:
            slot = DoctorTimeSlot(
                time_slot=time, is_available=True, doctor_id=doctor1.id
            )
            session.add(slot)

        # Create time slots for doctor 2
        for time in ["08:30 AM", "11:00 AM", "01:30 PM", "04:00 PM"]:
            slot = DoctorTimeSlot(
                time_slot=time, is_available=True, doctor_id=doctor2.id
            )
            session.add(slot)

        # Create doctors for hospital 2
        doctor3 = Doctor(
            name="Dr. Michael Brown",
            specialty="Orthopedics",
            rating=4.7,
            hospital_id=hospital2.id,
        )
        doctor4 = Doctor(
            name="Dr. Emily Davis",
            specialty="Pediatrics",
            rating=4.9,
            hospital_id=hospital2.id,
        )
        session.add(doctor3)
        session.add(doctor4)
        session.commit()
        session.refresh(doctor3)
        session.refresh(doctor4)

        # Create time slots for doctor 3
        for time in ["09:30 AM", "11:30 AM", "02:30 PM"]:
            slot = DoctorTimeSlot(
                time_slot=time, is_available=True, doctor_id=doctor3.id
            )
            session.add(slot)

        # Create time slots for doctor 4
        for time in ["08:00 AM", "10:00 AM", "01:00 PM", "03:00 PM"]:
            slot = DoctorTimeSlot(
                time_slot=time, is_available=True, doctor_id=doctor4.id
            )
            session.add(slot)

        # Create doctors for hospital 3
        doctor5 = Doctor(
            name="Dr. Robert Wilson",
            specialty="Neurology",
            rating=4.8,
            hospital_id=hospital3.id,
        )
        doctor6 = Doctor(
            name="Dr. Lisa Anderson",
            specialty="Dermatology",
            rating=4.6,
            hospital_id=hospital3.id,
        )
        session.add(doctor5)
        session.add(doctor6)
        session.commit()
        session.refresh(doctor5)
        session.refresh(doctor6)

        # Create time slots for doctor 5
        for time in ["09:00 AM", "02:00 PM", "04:30 PM"]:
            slot = DoctorTimeSlot(
                time_slot=time, is_available=True, doctor_id=doctor5.id
            )
            session.add(slot)

        # Create time slots for doctor 6
        for time in ["10:00 AM", "11:00 AM", "03:00 PM", "04:00 PM"]:
            slot = DoctorTimeSlot(
                time_slot=time, is_available=True, doctor_id=doctor6.id
            )
            session.add(slot)

        session.commit()
