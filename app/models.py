from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Centre(Base):
    __tablename__ = "centres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    services = Column(JSON)  # List of service types
    availability_summary = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    rating_count = Column(Integer, nullable=True)
    
    # Relationship
    booking_requests = relationship("BookingRequest", back_populates="centre")


class BookingRequest(Base):
    __tablename__ = "booking_requests"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    patient_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    preferred_contact_method = Column(String, nullable=True)
    preferred_time_window = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    location_input = Column(String, nullable=True)
    service_type = Column(String, nullable=True)
    centre_id = Column(Integer, ForeignKey("centres.id"), nullable=False)
    
    # Relationship
    centre = relationship("Centre", back_populates="booking_requests")