from fastapi import FastAPI, Request, Form, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
import urllib.parse

from app.database import get_db, init_db
from app.models import Centre, BookingRequest
from app.schemas import BookingRequestCreate, BookingRequestResponse
from app.seed_data import seed_centres

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup"""
    init_db()
    seed_centres()


# ==================== HTML Routes ====================

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Landing page"""
    return templates.TemplateResponse("landing.html", {"request": request})


@app.get("/location", response_class=HTMLResponse)
async def location_page_get(
    request: Request, 
    service_type: str = Query(...),
    error: Optional[str] = None
):
    """Location entry page (GET) - now second step after service"""
    return templates.TemplateResponse("location.html", {
        "request": request,
        "service_type": service_type,
        "error": error
    })


@app.post("/location")
async def location_page_post(
    request: Request,
    service_type: str = Form(...),
    location_input: str = Form(...)
):
    """Location entry page (POST) - redirects to centres"""
    if not location_input or not location_input.strip():
        return templates.TemplateResponse("location.html", {
            "request": request,
            "service_type": service_type,
            "error": "Please enter your address (location)."
        })
    
    # Redirect to centres list with both params
    encoded_location = urllib.parse.quote(location_input.strip())
    encoded_service = urllib.parse.quote(service_type)
    return RedirectResponse(
        url=f"/centres?location_input={encoded_location}&service_type={encoded_service}",
        status_code=303
    )


@app.get("/service", response_class=HTMLResponse)
async def service_page(request: Request, error: Optional[str] = None):
    """Service selection page - now first step after landing"""
    return templates.TemplateResponse("service.html", {
        "request": request,
        "error": error
    })


@app.post("/service")
async def service_page_post(
    request: Request,
    service_type: str = Form(...)
):
    """Service selection page (POST) - redirects to location"""
    if not service_type or not service_type.strip():
        return templates.TemplateResponse("service.html", {
            "request": request,
            "error": "Please choose a service."
        })
    
    # Redirect to location with service_type
    encoded_service = urllib.parse.quote(service_type.strip())
    return RedirectResponse(
        url=f"/location?service_type={encoded_service}",
        status_code=303
    )


@app.get("/centres", response_class=HTMLResponse)
async def centres_page(
    request: Request,
    location_input: str = Query(...),
    service_type: str = Query(...),
    db: Session = Depends(get_db)
):
    """Centres list page"""
    # Query centres matching location
    all_centres = db.query(Centre).filter(
        Centre.city.ilike(f"%{location_input}%")
    ).all()
    
    # Filter by service type (check if service_type is in services list)
    centres = [
        centre for centre in all_centres
        if centre.services and service_type in centre.services
    ]
    
    return templates.TemplateResponse("centres.html", {
        "request": request,
        "centres": centres,
        "location_input": location_input,
        "service_type": service_type
    })


@app.get("/book", response_class=HTMLResponse)
async def book_page_get(
    request: Request,
    centre_id: int = Query(...),
    location_input: str = Query(...),
    service_type: str = Query(...),
    db: Session = Depends(get_db),
    error: Optional[str] = None
):
    """Booking form page (GET)"""
    centre = db.query(Centre).filter(Centre.id == centre_id).first()
    if not centre:
        raise HTTPException(status_code=404, detail="Centre not found")
    
    return templates.TemplateResponse("book.html", {
        "request": request,
        "centre": centre,
        "centre_id": centre_id,
        "location_input": location_input,
        "service_type": service_type,
        "error": error
    })


@app.post("/book")
async def book_page_post(
    request: Request,
    centre_id: int = Form(...),
    location_input: str = Form(...),
    service_type: str = Form(...),
    patient_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    preferred_contact_method: Optional[str] = Form(None),
    preferred_time_window: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Booking form submission (POST)"""
    # Validate required fields
    if not patient_name or not patient_name.strip():
        centre = db.query(Centre).filter(Centre.id == centre_id).first()
        return templates.TemplateResponse("book.html", {
            "request": request,
            "centre": centre,
            "centre_id": centre_id,
            "location_input": location_input,
            "service_type": service_type,
            "error": "Patient name is required",
            "patient_name": patient_name,
            "email": email,
            "phone": phone,
            "preferred_contact_method": preferred_contact_method,
            "preferred_time_window": preferred_time_window,
            "notes": notes
        })
    
    # Basic email validation
    if "@" not in email or "." not in email.split("@")[1]:
        centre = db.query(Centre).filter(Centre.id == centre_id).first()
        return templates.TemplateResponse("book.html", {
            "request": request,
            "centre": centre,
            "centre_id": centre_id,
            "location_input": location_input,
            "service_type": service_type,
            "error": "Please enter a valid email address",
            "patient_name": patient_name,
            "email": email,
            "phone": phone,
            "preferred_contact_method": preferred_contact_method,
            "preferred_time_window": preferred_time_window,
            "notes": notes
        })
    
    # Verify centre exists
    centre = db.query(Centre).filter(Centre.id == centre_id).first()
    if not centre:
        raise HTTPException(status_code=404, detail="Centre not found")
    
    # Create booking request
    booking_request = BookingRequest(
        patient_name=patient_name.strip(),
        email=email.strip(),
        phone=phone.strip() if phone else None,
        preferred_contact_method=preferred_contact_method if preferred_contact_method else None,
        preferred_time_window=preferred_time_window.strip() if preferred_time_window else None,
        notes=notes.strip() if notes else None,
        location_input=location_input,
        service_type=service_type,
        centre_id=centre_id
    )
    
    db.add(booking_request)
    db.commit()
    db.refresh(booking_request)
    
    # Redirect to confirmation page
    return templates.TemplateResponse("confirmation.html", {
        "request": request,
        "patient_name": patient_name,
        "centre_name": centre.name
    })


@app.get("/confirmation", response_class=HTMLResponse)
async def confirmation_page(request: Request):
    """Confirmation page (direct access)"""
    return templates.TemplateResponse("confirmation.html", {
        "request": request,
        "patient_name": "there",
        "centre_name": "your selected centre"
    })


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About Us page"""
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/support", response_class=HTMLResponse)
async def support_page(request: Request):
    """Support page"""
    return templates.TemplateResponse("support.html", {"request": request})


# ==================== API Endpoints ====================

@app.get("/api/centres")
async def api_centres(
    city: str = Query(..., description="City or location input"),
    service: str = Query(..., description="Service type"),
    db: Session = Depends(get_db)
):
    """API endpoint to get matching centres"""
    # Query centres matching location
    all_centres = db.query(Centre).filter(
        Centre.city.ilike(f"%{city}%")
    ).all()
    
    # Filter by service type (check if service is in services list)
    centres = [
        centre for centre in all_centres
        if centre.services and service in centre.services
    ]
    
    return [
        {
            "id": centre.id,
            "name": centre.name,
            "address": centre.address,
            "city": centre.city,
            "services": centre.services,
            "availability_summary": centre.availability_summary,
            "rating": centre.rating,
            "rating_count": centre.rating_count
        }
        for centre in centres
    ]


@app.post("/api/booking-requests", response_model=BookingRequestResponse, status_code=201)
async def api_create_booking_request(
    booking_request: BookingRequestCreate,
    db: Session = Depends(get_db)
):
    """API endpoint to create a booking request"""
    # Verify centre exists
    centre = db.query(Centre).filter(Centre.id == booking_request.centre_id).first()
    if not centre:
        raise HTTPException(status_code=404, detail="Centre not found")
    
    # Create booking request
    db_booking_request = BookingRequest(
        patient_name=booking_request.patient_name,
        email=booking_request.email,
        phone=booking_request.phone,
        preferred_contact_method=booking_request.preferred_contact_method,
        preferred_time_window=booking_request.preferred_time_window,
        notes=booking_request.notes,
        location_input=booking_request.location_input,
        service_type=booking_request.service_type,
        centre_id=booking_request.centre_id
    )
    
    db.add(db_booking_request)
    db.commit()
    db.refresh(db_booking_request)
    
    return BookingRequestResponse(
        id=db_booking_request.id,
        created_at=db_booking_request.created_at
    )
