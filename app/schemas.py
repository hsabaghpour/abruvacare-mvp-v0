from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class CentreBase(BaseModel):
    name: str
    address: str
    city: str
    services: List[str]
    availability_summary: Optional[str] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None


class Centre(CentreBase):
    id: int

    class Config:
        orm_mode = True


class BookingRequestBase(BaseModel):
    patient_name: str
    email: EmailStr
    phone: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    preferred_time_window: Optional[str] = None
    notes: Optional[str] = None
    location_input: Optional[str] = None
    service_type: Optional[str] = None
    centre_id: int


class BookingRequestCreate(BookingRequestBase):
    pass


class BookingRequestResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

