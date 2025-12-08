AbruvaCare – MVP V0 (Patient Flow Only) – Implementation Brief

## Quick Start

### Setup

1. **Activate the virtual environment:**

   ```bash
   source venv/bin/activate
   ```

2. **Install/update dependencies (if needed):**

   ```bash
   pip install -r requirements.txt
   ```

   Or run the setup script:

   ```bash
   ./setup.sh
   ```

3. **Run the application:**

   ```bash
   uvicorn app.main:app --reload
   ```

   Or use the run script:

   ```bash
   ./run.sh
   ```

4. **Access the application:**
   - Open your browser to: `http://localhost:8000`
   - API docs available at: `http://localhost:8000/docs`

The database will be automatically initialized and seeded with sample centres on first startup.

---

You are helping implement a small web application called AbruvaCare – MVP V0.

The goal is to build a patient-only web app for British Columbia, Canada that allows patients to:

Start from a landing page.

Enter their location (city/address).

Choose the type of service they need.

See a list of matching centres.

Submit a simple booking request for a selected centre.

There is no login, no provider portal, and no payments in this version.

1. Tech Stack & Architecture

Use the following stack:

Backend framework: FastAPI (Python)

Templating: Jinja2 (server-rendered HTML pages)

Database: SQLite (via SQLAlchemy ORM)

Static files: basic CSS for styling

Server: uvicorn for local development

Architecture:

A single FastAPI app serves:

HTML pages (landing, forms, lists) using Jinja2 templates.

JSON APIs for /api/centres and /api/booking-requests.

A simple SQLite database stores:

A fixed list of centres (seeded at startup).

Patient booking requests.

The app should be implemented in a Python package called app inside the project folder, for example:

abruvacare-mvp-v0/
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── seed_data.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── landing.html
│ │ ├── location.html
│ │ ├── service.html
│ │ ├── centres.html
│ │ ├── book.html
│ │ └── confirmation.html
│ └── static/
│ └── styles.css
├── requirements.txt
└── README.md

2. User Flow & Routes
   2.1 / – Landing Page

Purpose: Explain what AbruvaCare is and send users into the booking flow.

Requirements:

Show a simple hero section with:

Title: something like “Find the right care in British Columbia”.

Short subtitle explaining that the app helps pregnant / postpartum / early-years patients find care centres.

A primary CTA button: “Book Appointment”.

Top navigation bar with:

Logo / brand name “AbruvaCare”.

Link “For Patients” (active, links to /).

Link “For Healthcare Providers” (links to a simple “coming soon” static page or just # for now).

Link “Support” (mailto link, e.g. mailto:hello@example.com).

A secondary “Book Appointment” button linking to /location.

Behavior:

Clicking “Book Appointment” navigates to /location (GET).

2.2 /location – Enter Location

Purpose: Capture the patient’s location so we can filter centres.

Requirements:

Render a simple form with:

Label: “Where are you located?” or “Enter your city or address”.

Single text input: name="location_input", required.

A “Continue” button.

Behavior:

Method: POST /location when form is submitted.

Validate that location_input is non-empty. If empty:

Re-render the same page with an error message.

On success:

Redirect (HTTP 303) to /service, passing location_input as a query parameter:

Example redirect:

/service?location_input=Coquitlam

We are not doing any advanced geocoding in V0; treat this field as a free-text city/location string.

2.3 /service – Pick Service/Centre Type

Purpose: Let the user indicate the kind of service they need.

Requirements:

Read location_input from the query string.

Render a form with:

A dropdown <select name="service_type"> with options like:

“Maternity Clinic”

“Family Doctor”

“Physiotherapy”

“Lactation Consultant”

“Mental Health”

Hidden input for location_input so it can be posted.

“Find Centres” button.

Behavior:

Method: POST /service when form is submitted.

On submit:

Read location_input (hidden) and service_type from the form.

Redirect (HTTP 303) to /centres with both as query parameters:

Example:

/centres?location_input=Coquitlam&service_type=Maternity+Clinic

2.4 /centres – Centres List (Search Results)

Purpose: Display matching centres and let the user choose one to book.

Inputs:

Query parameters:

location_input (e.g. “Coquitlam”).

service_type (e.g. “Maternity Clinic”).

Data source:

Query the centres table using:

City filter: city LIKE %location_input% (case-insensitive).

Service filter: service_type should be present in the services list/JSON column.

Requirements:

Render a list of centres as “cards”.

For each centre, display:

name

address

city

availability_summary if present

rating and rating_count if present

A “Book Appointment” button.

Behavior:

If no centres match:

Show a friendly “No centres found” message.

“Book Appointment” button navigates to /book and passes:

centre_id

location_input

service_type

Example link:

/book?centre_id=1&location_input=Coquitlam&service_type=Maternity+Clinic

2.5 /book – Booking Request Form

Purpose: Collect patient information and submit a booking request for a specific centre.

Inputs:

Query params:

centre_id

location_input

service_type

Behavior on GET:

Look up the centre by centre_id in the database.

Render a form with:

Heading like: “Request an appointment at {centre.name}”.

Visible fields:

patient_name (required)

email (required, basic email format)

phone (optional)

preferred_contact_method (select: “email”, “phone”, “no preference”)

preferred_time_window (free text, e.g. “weekday evenings”)

notes (textarea for reason/extra info)

Hidden or pre-filled fields:

centre_id

location_input

service_type

Submit button: “Submit Request”.

Behavior on POST:

Endpoint: POST /book.

Validate patient_name and email.

Insert a new row in booking_requests table with:

created_at (current timestamp)

patient_name

email

phone

preferred_contact_method

preferred_time_window

notes

location_input

service_type

centre_id

After successful insert:

Render a simple confirmation page /confirmation or directly render confirmation.html:

“Thank you, {patient_name}! Your request for {centre.name} has been received.”

A button linking back to /.

3. API Endpoints (JSON)

Even though the app is mostly server-rendered HTML, also expose JSON endpoints for future use.

3.1 GET /api/centres

Purpose:

Return a JSON list of centres matching the filters.

Query parameters:

city (string, required) – city or location input, same as location_input.

service (string, required) – service type.

Response:

HTTP 200 OK.

JSON array of centre objects, where each object has:

{
"id": 1,
"name": "Vancouver Maternity Clinic",
"address": "123 Main St, Vancouver, BC",
"city": "Vancouver",
"services": ["Maternity Clinic", "Family Doctor"],
"availability_summary": "New patients accepted; wait time ~2 weeks",
"rating": 4.7,
"rating_count": 120
}

Filtering logic:

Similar to /centres page: filter by city (case-insensitive LIKE) and by membership of service in services list.

3.2 POST /api/booking-requests

Purpose:

Create a new booking request from a JSON payload.

Request body (JSON):

{
"patient_name": "string",
"email": "string",
"phone": "string or null",
"preferred_contact_method": "email | phone | null",
"preferred_time_window": "string or null",
"notes": "string or null",
"location_input": "string or null",
"service_type": "string or null",
"centre_id": 1
}

Behavior:

Validate that centre_id refers to an existing centre.

Insert into booking_requests table.

Return:

{
"id": 123,
"created_at": "2025-01-03T12:34:56Z"
}

Use HTTP status 201 Created.

4. Data Model

Use SQLAlchemy models for the following tables.

4.1 centres table

Columns:

id – integer primary key

name – string, required

address – string, required

city – string, required

services – JSON or equivalent type representing a list of strings

availability_summary – string, nullable

rating – float, nullable

rating_count – integer, nullable

4.2 booking_requests table

Columns:

id – integer primary key

created_at – datetime, default = current UTC time

patient_name – string, required

email – string, required

phone – string, nullable

preferred_contact_method – string, nullable

preferred_time_window – string, nullable

notes – string, nullable

location_input – string, nullable

service_type – string, nullable

centre_id – integer, foreign key referencing centres.id

Relationship:

BookingRequest.centre → relationship to Centre

Centre.booking_requests → relationship back to BookingRequest

5. Seeding Centres Data

Implement a seed_data.py module that:

Contains a small list of dictionaries defining sample centres.

On startup, checks if centres table is empty.

If empty, inserts the sample centres.

If not empty, do nothing.
