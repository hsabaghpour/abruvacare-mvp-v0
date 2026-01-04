# SoW Alignment Gap Report

## Executive Summary
This document identifies gaps between the current AbruvaCare MVP implementation and the SoW requirements, and outlines the implementation plan to align them.

---

## 1. ROUTE STRUCTURE GAPS

### Current Routes
- `/` - Landing
- `/service` - Service selection
- `/location` - Location entry
- `/centres` - Results
- `/book` - Booking form
- `/confirmation` - Confirmation
- `/about` - About Us
- `/support` - Support

### SoW Required Routes
- `/patients` - Landing (alias for `/`)
- `/patients/service` - Service selection (alias for `/service`)
- `/patients/location` - Location entry (alias for `/location`)
- `/patients/results` - Results (alias for `/centres`)
- `/about` - About Us ✅ (already exists)
- `/support` - Support ✅ (already exists)

### Gap
- Missing `/patients/*` route aliases
- Landing CTA currently goes to `/service`, should go to `/patients/service`

### Resolution
- Add alias routes in `main.py` that render same templates
- Update landing.html CTA to use `/patients/service`
- Keep old routes working for backward compatibility

---

## 2. CAROUSEL BEHAVIOR GAPS

### Current Implementation
- ✅ 4 slides (correct)
- ✅ Autoplay: 5 seconds (within 4-6s range)
- ✅ Left/right arrows
- ✅ 4 dot indicators
- ✅ Pause on hover
- ✅ Pause after user interaction (10s resume)
- ✅ Keyboard support (← →)
- ✅ aria-labels on controls

### SoW Requirements
- Autoplay: 4-6 seconds ✅ (current: 5s)
- All other features ✅

### Gap
- None - carousel already meets requirements

### Resolution
- No changes needed, but will make timing configurable (4-6s range)

---

## 3. COPY/TEXT GAPS

### Landing Page
- ✅ Headline: "Need a Healthcare Service in British Columbia?"
- ✅ Subtext: "You don't have to do this alone. Find nearby care with real availability and book sooner - without the endless searching."
- ⚠️ CTA: Currently says "Get Started", should verify matches PDF
- ⚠️ CTA route: Currently `/service`, should be `/patients/service`

### Service Page
- ✅ Title: "Please choose the service"
- ✅ Error: "Please choose a service."

### Location Page
- ✅ Title: "Please enter your Address (Location)"
- ✅ Error: "Please enter your address (location)."

### Results Page
- ✅ Title: "List of Centres - Healthcare Providers"
- ✅ Empty state: "No centres found for this service near your location."

### About Page
- ✅ All copy matches SoW exactly

### Support Page
- ✅ Email: info@abruvacare.com
- ✅ Phone: (778)-xxx-xxxx
- ✅ Fax: (778)-xxx-xxxx

### Gap
- Landing CTA route needs update
- CTA button text may need verification against PDF

---

## 4. HEADER/NAVIGATION GAPS

### Current Implementation
- ✅ Logo + brand name on left
- ✅ Nav links: For Patients, For Healthcare Providers, About Us, Support
- ✅ "Proudly Canadian" banner with flag
- ✅ Active state highlighting (based on `request.url.path`)

### SoW Requirements
- ✅ All elements present
- ⚠️ Active state needs to handle `/patients/*` routes

### Gap
- Active state logic may not highlight correctly for `/patients/*` routes
- Need to ensure "For Patients" is active on `/patients/*` routes

### Resolution
- Update active state logic in base.html to handle both `/` and `/patients/*` routes

---

## 5. SERVICE LIST GAPS

### Current Services
- Maternity Clinic
- Family Doctor
- Physiotherapy
- Lactation Consultant
- Mental Health

### SoW Mentioned Services
- Midwife
- Doula
- Dietitian
- (These are examples, not requirements)

### Gap
- SoW doesn't mandate specific services, just structure
- Current services are fine, but should be centralized

### Resolution
- Create centralized service list constant
- Keep current services (they match healthcare needs)
- Make it easy to update later if needed

---

## 6. RESULTS PAGE GAPS

### Current Implementation
- ✅ Centre name
- ✅ Full address
- ✅ Availability summary
- ✅ Rating
- ✅ Booking CTA
- ✅ Empty state with back buttons

### SoW Requirements
- ✅ All fields present
- ✅ Empty state message correct

### Gap
- None identified

---

## 7. CSS/STYLING GAPS

### Current Implementation
- Custom CSS with consistent styling
- Responsive design
- Color scheme defined

### SoW Requirements
- Match UI/UX PDF exactly (visual source of truth)

### Gap
- Cannot verify exact colors/fonts without PDF
- Current styling appears professional and consistent

### Resolution
- Add CSS variables for easy theming
- Add TODO comments for PDF verification
- Keep existing styles (they appear to match intent)

---

## IMPLEMENTATION PRIORITY

### High Priority (Must Fix)
1. ✅ Add `/patients/*` route aliases
2. ✅ Update landing CTA to `/patients/service`
3. ✅ Fix active nav state for `/patients/*` routes

### Medium Priority (Should Fix)
4. ✅ Centralize service list
5. ✅ Make carousel timing configurable (4-6s)
6. ✅ Add CSS variables for theming

### Low Priority (Nice to Have)
7. ✅ Add TODO comments for PDF color verification
8. ✅ Update documentation

---

## TESTING CHECKLIST

After implementation, verify:

- [ ] `/patients` renders same as `/`
- [ ] `/patients/service` renders same as `/service`
- [ ] `/patients/location` renders same as `/location`
- [ ] `/patients/results` renders same as `/centres`
- [ ] Landing CTA goes to `/patients/service`
- [ ] Old routes still work (`/`, `/service`, etc.)
- [ ] Active nav state works on all routes
- [ ] Carousel timing is 4-6 seconds
- [ ] All copy matches SoW
- [ ] Responsive design works
- [ ] End-to-end flow works on both route sets

---

## NOTES

- All existing functionality must be preserved
- Backward compatibility is critical
- No breaking changes allowed
- Work only on SOW2 branch

