"""
Centralized constants for AbruvaCare application.
This makes it easy to update service lists, timing, and other configurable values.
"""

# Service types available for selection
SERVICE_TYPES = [
    "Maternity Clinic",
    "Family Doctor",
    "Physiotherapy",
    "Lactation Consultant",
    "Mental Health"
]

# Carousel configuration
CAROUSEL_AUTOPLAY_DELAY = 5000  # 5 seconds (within 4-6s range per SoW)
CAROUSEL_PAUSE_RESUME_DELAY = 10000  # 10 seconds before resuming after user interaction

