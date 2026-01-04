# AbruvaCare MVP v0 - Complete Project Summary

## 📋 Project Overview

**AbruvaCare** is a patient-focused web application designed specifically for British Columbia, Canada. The platform helps patients (particularly pregnant, postpartum, and early-years patients) find and book appointments at healthcare centres throughout BC.

### Mission Statement
"We want every woman to feel supported, not alone, on her health journey. We created AbruvaCare so finding the right care feels simple, safe, and close."

### Current Status
- **Version**: MVP v0 (Minimum Viable Product)
- **Launch Year**: 2025
- **Target Region**: British Columbia, Canada
- **Focus**: Patient-only booking flow (no provider portal, no payments in v0)

---

## 🏗️ Architecture & Technology Stack

### Backend Framework
- **FastAPI** (Python) - Modern, fast web framework for building APIs
- **SQLAlchemy** (ORM) - Database abstraction layer
- **SQLite** - Lightweight database (perfect for MVP)

### Frontend
- **Jinja2** - Server-side HTML templating
- **Vanilla JavaScript** - Client-side interactivity (carousel, form validation)
- **CSS3** - Custom responsive styling

### Server
- **Uvicorn** - ASGI server for FastAPI

### Development Tools
- **Python 3.9+** - Programming language
- **Virtual Environment** - Dependency isolation
- **Git** - Version control

---

## 📁 Project Structure

```
abruvacare-mvp-v0/
├── app/                          # Main application package
│   ├── main.py                  # FastAPI app, routes, and API endpoints
│   ├── database.py              # Database connection and initialization
│   ├── models.py                # SQLAlchemy data models
│   ├── schemas.py               # Pydantic schemas for API validation
│   ├── seed_data.py             # Sample healthcare centres data
│   ├── static/                   # Static assets
│   │   ├── styles.css           # Global CSS styles
│   │   ├── logo.png             # AbruvaCare logo
│   │   ├── canada-flag.png      # Canada flag icon
│   │   └── hero/                # Hero carousel images
│   │       ├── slide1.jpg       # Pregnancy Care
│   │       ├── slide2.jpg       # Pregnancy Ultrasound
│   │       ├── slide3.jpg       # Yoga Therapy
│   │       └── slide4.jpg       # Dilation
│   └── templates/               # Jinja2 HTML templates
│       ├── base.html            # Base template with header/footer
│       ├── landing.html         # Landing page with carousel
│       ├── service.html         # Service selection page
│       ├── location.html        # Location entry page
│       ├── centres.html         # Results/centres listing page
│       ├── book.html            # Booking form page
│       ├── confirmation.html    # Booking confirmation page
│       ├── about.html           # About Us page
│       └── support.html         # Support/Contact page
├── Images/                       # Original image assets
│   ├── Abruva_logo.png
│   ├── Canada_flag.png
│   ├── Pregnancy_Care.png
│   ├── Pregnancy_UltraSound.png
│   ├── Yoga_Therapy.png
│   └── Diatation.png
├── venv/                         # Python virtual environment
├── abruvacare.db                # SQLite database (auto-generated)
├── requirements.txt              # Python dependencies
├── setup.sh                      # Setup script
├── run.sh                        # Run script
├── README.md                     # User-facing documentation
├── IMPLEMENTATION_SUMMARY.md     # SoW implementation details
└── PROJECT_SUMMARY.md           # This file
```

---

## 🔄 User Flow & Features

### Complete Patient Journey

1. **Landing Page** (`/`)
   - Hero carousel with 4 rotating slides
   - Autoplay every 5 seconds
   - Manual navigation (arrows, dots, keyboard)
   - Primary CTA: "Get Started" button
   - Headline: "Need a Healthcare Service in British Columbia?"
   - Subtext: "You don't have to do this alone..."

2. **Service Selection** (`/service`)
   - User selects service type from dropdown
   - Options: Maternity Clinic, Family Doctor, Physiotherapy, Lactation Consultant, Mental Health
   - Client-side validation (button disabled until selection)
   - Error message: "Please choose a service."

3. **Location Entry** (`/location?service_type=...`)
   - User enters city or full address
   - Service type is preserved (hidden field)
   - Client-side validation (button disabled until input)
   - Error message: "Please enter your address (location)."

4. **Centres Results** (`/centres?location_input=...&service_type=...`)
   - Displays matching healthcare centres
   - Each card shows:
     - Centre name and full address
     - Availability summary ("Next available: ...")
     - Rating (stars) and review count
     - "Book Appointment" button
   - Empty state with helpful messaging
   - Back buttons to modify search

5. **Booking Form** (`/book?centre_id=...&location_input=...&service_type=...`)
   - Patient information collection:
     - Name (required)
     - Email (required, validated)
     - Phone (optional)
     - Preferred contact method
     - Preferred time window
     - Additional notes
   - Server-side validation
   - Creates booking request in database

6. **Confirmation** (`/confirmation`)
   - Success message
   - Patient name and centre name displayed
   - Return to home button

### Additional Pages

- **About Us** (`/about`) - Company mission and information
- **Support** (`/support`) - Contact information (email, phone, fax)

---

## 🗄️ Database Schema

### Centres Table
Stores healthcare centre information:

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String | Centre name (required) |
| `address` | String | Full address (required) |
| `city` | String | City name (required) |
| `services` | JSON | Array of service types offered |
| `availability_summary` | String | Availability information (nullable) |
| `rating` | Float | Average rating (nullable) |
| `rating_count` | Integer | Number of reviews (nullable) |

**Relationships**: One-to-many with `booking_requests`

### Booking Requests Table
Stores patient booking submissions:

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `created_at` | DateTime | Timestamp (auto-generated) |
| `patient_name` | String | Patient's name (required) |
| `email` | String | Email address (required) |
| `phone` | String | Phone number (nullable) |
| `preferred_contact_method` | String | email/phone/no preference |
| `preferred_time_window` | String | Free text (nullable) |
| `notes` | String | Additional information (nullable) |
| `location_input` | String | User's location search (nullable) |
| `service_type` | String | Selected service type (nullable) |
| `centre_id` | Integer | Foreign key to centres (required) |

**Relationships**: Many-to-one with `centres`

### Seed Data
The application includes 7 sample healthcare centres across BC:
- Vancouver Maternity Clinic
- Coquitlam Family Health Centre
- Surrey Physiotherapy & Wellness
- Burnaby Mental Health Services
- Richmond Lactation Support
- Victoria Maternity & Family Care
- Kelowna Comprehensive Care

---

## 🔌 API Endpoints

### HTML Routes (Server-Rendered)
- `GET /` - Landing page
- `GET /service` - Service selection page
- `POST /service` - Process service selection
- `GET /location` - Location entry page
- `POST /location` - Process location entry
- `GET /centres` - Centres results page
- `GET /book` - Booking form page
- `POST /book` - Process booking submission
- `GET /confirmation` - Confirmation page
- `GET /about` - About Us page
- `GET /support` - Support page

### JSON API Endpoints

#### GET `/api/centres`
Search for healthcare centres.

**Query Parameters:**
- `city` (required) - City or location input
- `service` (required) - Service type

**Response:**
```json
[
  {
    "id": 1,
    "name": "Vancouver Maternity Clinic",
    "address": "123 Main St",
    "city": "Vancouver",
    "services": ["Maternity Clinic", "Family Doctor"],
    "availability_summary": "New patients accepted; wait time ~2 weeks",
    "rating": 4.7,
    "rating_count": 120
  }
]
```

#### POST `/api/booking-requests`
Create a new booking request.

**Request Body:**
```json
{
  "patient_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "778-123-4567",
  "preferred_contact_method": "email",
  "preferred_time_window": "weekday evenings",
  "notes": "First-time patient",
  "location_input": "Vancouver",
  "service_type": "Maternity Clinic",
  "centre_id": 1
}
```

**Response:**
```json
{
  "id": 123,
  "created_at": "2025-01-03T12:34:56Z"
}
```

---

## 🎨 UI/UX Features

### Global Header & Navigation
- **Logo**: AbruvaCare logo image with text fallback
- **Navigation Links**:
  - For Patients (active on landing)
  - For Healthcare Providers (coming soon)
  - About Us
  - Support
- **Canada Banner**: "Proudly Canadian" with flag icon
- **Mobile Responsive**: Hamburger menu on small screens
- **Active Link Highlighting**: Visual indication of current page

### Hero Carousel
- **4 Slides**: Rotating hero images
- **Autoplay**: Changes every 5 seconds
- **Controls**:
  - Left/right arrow buttons
  - Dot indicators (4 dots)
  - Keyboard navigation (← →)
- **Smart Pausing**:
  - Pauses on hover (desktop)
  - Pauses after user interaction (resumes after 10 seconds)

### Form Validation
- **Client-Side**: Immediate feedback, disabled buttons until valid
- **Server-Side**: Email format validation, required field checks
- **Error Messages**: Clear, user-friendly messages

### Responsive Design
- **Mobile-First**: Works on all screen sizes
- **Breakpoints**: Optimized for mobile, tablet, desktop
- **Touch-Friendly**: Large buttons, easy navigation

---

## 🌿 Git Branch Structure

The project uses a branching strategy to protect the original MVP:

```
main                    # Original MVP (protected)
├── sow-implementation  # First SoW UI/UX implementation
└── SOW2                # Current working branch (new SoW work)
```

### Branch Purposes

- **main**: Stable MVP version - patient flow only, no login, no payments
- **sow-implementation**: First Statement of Work implementation with:
  - Updated UI/UX
  - Hero carousel
  - New navigation
  - About/Support pages
  - Integrated images
- **SOW2**: Current branch for additional SoW work

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.7+ (3.9+ recommended)
- Git
- Terminal/Command Prompt

### Quick Start

1. **Clone Repository**
   ```bash
   git clone https://github.com/hsabaghpour/abruvacare-mvp-v0.git
   cd abruvacare-mvp-v0
   ```

2. **Create Virtual Environment**
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   uvicorn app.main:app --reload
   # Or use: ./run.sh
   ```

5. **Access Application**
   - Main app: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Database Initialization
The database is automatically created and seeded on first startup:
- Tables are created via SQLAlchemy
- Sample centres are inserted if table is empty
- Database file: `abruvacare.db` (SQLite)

---

## 📦 Dependencies

Key Python packages (see `requirements.txt` for full list):

- **fastapi** (0.83.0) - Web framework
- **uvicorn** (0.17.0) - ASGI server
- **sqlalchemy** (1.4.54) - ORM
- **jinja2** (3.0.3) - Templating
- **pydantic** (1.9.2) - Data validation
- **python-multipart** (0.0.5) - Form data handling
- **email-validator** (1.1.3) - Email validation

---

## 🔒 Security & Best Practices

### Current Implementation
- Input validation (client and server-side)
- SQL injection protection (SQLAlchemy ORM)
- Email format validation
- XSS protection (Jinja2 auto-escaping)

### Future Considerations
- User authentication (not in v0)
- HTTPS in production
- Rate limiting
- CSRF protection
- Data encryption

---

## 🎯 Key Features Implemented

### ✅ Completed Features

1. **Complete Patient Booking Flow**
   - Multi-step form with state preservation
   - Service → Location → Results → Booking → Confirmation

2. **Healthcare Centre Search**
   - Location-based filtering
   - Service type filtering
   - Real-time results display

3. **Hero Carousel**
   - 4-slide rotation
   - Full navigation controls
   - Accessibility features

4. **Responsive Design**
   - Mobile, tablet, desktop support
   - Touch-friendly interface

5. **REST API**
   - JSON endpoints for future integrations
   - OpenAPI documentation

6. **Database Integration**
   - SQLite with SQLAlchemy ORM
   - Automatic seeding
   - Relationship management

7. **Brand Identity**
   - Logo integration
   - Canada flag banner
   - Consistent styling

### 🚧 Not Included in v0

- User authentication/login
- Provider portal
- Payment processing
- Email notifications
- SMS notifications
- Advanced geocoding
- Real-time availability
- Calendar integration

---

## 📊 Project Statistics

- **Total Routes**: 18 (HTML + API)
- **Templates**: 9 HTML pages
- **Database Tables**: 2 (centres, booking_requests)
- **Seed Data**: 7 sample healthcare centres
- **Static Assets**: 8 images (logo, flag, 4 hero slides)
- **Lines of Code**: ~1,500+ (Python + HTML + CSS + JS)

---

## 🔮 Future Roadmap

### Potential Enhancements
1. **User Accounts**
   - Patient registration/login
   - Booking history
   - Saved preferences

2. **Provider Portal**
   - Centre management
   - Booking request management
   - Availability calendar

3. **Enhanced Search**
   - Map integration
   - Distance calculation
   - Advanced filters

4. **Notifications**
   - Email confirmations
   - SMS reminders
   - Push notifications

5. **Payments**
   - Online payment processing
   - Insurance integration

6. **Analytics**
   - Usage statistics
   - Popular services
   - Search trends

---

## 📝 Development Notes

### Code Organization
- **Separation of Concerns**: Models, routes, templates, static files
- **DRY Principle**: Reusable templates (base.html)
- **Consistent Patterns**: Follow FastAPI best practices

### Testing
- Manual testing checklist available
- End-to-end flow verification
- API endpoint testing via `/docs`

### Deployment Considerations
- SQLite suitable for MVP (consider PostgreSQL for production)
- Static file serving configured
- Environment variables for configuration
- Database migrations (future)

---

## 📞 Contact & Support

- **Email**: info@abruvacare.com
- **Phone**: (778)-xxx-xxxx
- **Fax**: (778)-xxx-xxxx

---

## 📄 License & Copyright

© 2025 AbruvaCare. All rights reserved.

---

## 🙏 Acknowledgments

Built with:
- FastAPI community
- Python ecosystem
- Open source libraries

---

**Last Updated**: January 2025  
**Version**: MVP v0  
**Branch**: SOW2

