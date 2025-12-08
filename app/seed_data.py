from app.database import SessionLocal
from app.models import Centre


SAMPLE_CENTRES = [
    {
        "name": "Vancouver Maternity Clinic",
        "address": "123 Main St",
        "city": "Vancouver",
        "services": ["Maternity Clinic", "Family Doctor"],
        "availability_summary": "New patients accepted; wait time ~2 weeks",
        "rating": 4.7,
        "rating_count": 120
    },
    {
        "name": "Coquitlam Family Health Centre",
        "address": "456 Oak Avenue",
        "city": "Coquitlam",
        "services": ["Family Doctor", "Maternity Clinic"],
        "availability_summary": "Accepting new patients",
        "rating": 4.5,
        "rating_count": 85
    },
    {
        "name": "Surrey Physiotherapy & Wellness",
        "address": "789 King Street",
        "city": "Surrey",
        "services": ["Physiotherapy", "Lactation Consultant"],
        "availability_summary": "Same-week appointments available",
        "rating": 4.8,
        "rating_count": 200
    },
    {
        "name": "Burnaby Mental Health Services",
        "address": "321 Pine Road",
        "city": "Burnaby",
        "services": ["Mental Health"],
        "availability_summary": "Wait time ~3-4 weeks",
        "rating": 4.6,
        "rating_count": 95
    },
    {
        "name": "Richmond Lactation Support",
        "address": "654 Maple Drive",
        "city": "Richmond",
        "services": ["Lactation Consultant"],
        "availability_summary": "Next-day appointments available",
        "rating": 4.9,
        "rating_count": 150
    },
    {
        "name": "Victoria Maternity & Family Care",
        "address": "987 Cedar Lane",
        "city": "Victoria",
        "services": ["Maternity Clinic", "Family Doctor", "Mental Health"],
        "availability_summary": "New patients welcome",
        "rating": 4.4,
        "rating_count": 110
    },
    {
        "name": "Kelowna Comprehensive Care",
        "address": "147 Elm Street",
        "city": "Kelowna",
        "services": ["Family Doctor", "Physiotherapy", "Mental Health"],
        "availability_summary": "Limited availability",
        "rating": 4.3,
        "rating_count": 75
    }
]


def seed_centres():
    """Seed the centres table if it's empty"""
    db = SessionLocal()
    try:
        # Check if centres table is empty
        count = db.query(Centre).count()
        if count == 0:
            print("Seeding centres table...")
            for centre_data in SAMPLE_CENTRES:
                centre = Centre(**centre_data)
                db.add(centre)
            db.commit()
            print(f"Seeded {len(SAMPLE_CENTRES)} centres")
        else:
            print(f"Centres table already has {count} entries, skipping seed")
    except Exception as e:
        print(f"Error seeding centres: {e}")
        db.rollback()
    finally:
        db.close()

