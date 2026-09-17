from datetime import date, timedelta
from pathlib import Path

from app import app
from models import db
from models.model import (
    User,
    AdminProfile,
    StaffProfile,
    TrekkerProfile,
    Trek,
    Booking,
)


# ============================================================
# DEMO DATA
# ============================================================

ADMIN_PASSWORD = "AdminDemo@2026"
STAFF_PASSWORD = "StaffDemo@2026"
TREKKER_PASSWORD = "TrekkerDemo@2026"

today = date.today()


# ============================================================
# HELPERS
# ============================================================

def get_or_create_user(
    first_name,
    last_name,
    email,
    password,
    role,
    contact=None,
    dob=None,
    bio=None,
):
    user = User.query.filter_by(email=email).first()

    if user is None:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=role,
            is_active=True,
            is_approved=True,
            is_blocked=False,
        )

        db.session.add(user)
        db.session.flush()

    else:
        # Keep demo accounts deterministic if seed.py is run again.
        user.first_name = first_name
        user.last_name = last_name
        user.password = password
        user.role = role
        user.is_active = True
        user.is_approved = True
        user.is_blocked = False

    # --------------------------------------------------------
    # Profile
    # --------------------------------------------------------

    if role == "admin":

        if user.admin_profile is None:
            user.admin_profile = AdminProfile()

        user.admin_profile.contact = contact
        user.admin_profile.dob = dob
        user.admin_profile.bio = bio

    elif role == "staff":

        if user.staff_profile is None:
            user.staff_profile = StaffProfile()

        user.staff_profile.contact = contact
        user.staff_profile.dob = dob
        user.staff_profile.bio = bio

    elif role == "trekker":

        if user.trekker_profile is None:
            user.trekker_profile = TrekkerProfile()

        user.trekker_profile.contact = contact
        user.trekker_profile.dob = dob
        user.trekker_profile.bio = bio

    return user


def get_or_create_trek(
    trek_code,
    trek_name,
    location,
    difficulty,
    duration,
    start_date,
    end_date,
    trek_status,
    slots,
    price,
    description,
    staff,
):
    trek = Trek.query.filter_by(trek_code=trek_code).first()

    if trek is None:
        trek = Trek(
            trek_code=trek_code,
            trek_name=trek_name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            start_date=start_date,
            end_date=end_date,
            trek_status=trek_status,
            slots=slots,
            booked_slots=0,
            price=price,
            description=description,
            staff_id=staff.id,
        )

        db.session.add(trek)

    else:
        trek.trek_name = trek_name
        trek.location = location
        trek.difficulty = difficulty
        trek.duration = duration
        trek.start_date = start_date
        trek.end_date = end_date
        trek.trek_status = trek_status
        trek.slots = slots
        trek.price = price
        trek.description = description
        trek.staff_id = staff.id

    return trek


def get_or_create_booking(trek, trekker, status, amount_paid=0):
    booking = Booking.query.filter_by(
        trek_id=trek.id,
        trekker_id=trekker.id,
    ).first()

    if booking is None:
        booking = Booking(
            trek_id=trek.id,
            trekker_id=trekker.id,
            booking_date=today,
            status=status,
            amount_paid=amount_paid,
        )

        db.session.add(booking)

    else:
        booking.status = status
        booking.amount_paid = amount_paid

    return booking


# ============================================================
# DATABASE
# ============================================================

with app.app_context():

    # Flask-SQLAlchemy places relative SQLite databases
    # inside the Flask instance directory.
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.create_all()

    # ========================================================
    # ADMIN
    # ========================================================

    admin = get_or_create_user(
        first_name="Demo",
        last_name="Admin",
        email="admin.demo@example.com",
        password=ADMIN_PASSWORD,
        role="admin",
        contact="0000111100",
        dob=date(1995, 4, 12),
        bio="AAA Street, BBB Nagar. Demo administrator account.",
    )

    # ========================================================
    # STAFF
    # ========================================================

    staff1 = get_or_create_user(
        first_name="Rahul",
        last_name="Sharma",
        email="staff1.demo@example.com",
        password=STAFF_PASSWORD,
        role="staff",
        contact="0000222200",
        dob=date(1998, 7, 19),
        bio="CCC Road, DDD Colony. Demo trekking staff member.",
    )

    staff2 = get_or_create_user(
        first_name="Amit",
        last_name="Kumar",
        email="staff2.demo@example.com",
        password=STAFF_PASSWORD,
        role="staff",
        contact="0000333300",
        dob=date(1997, 2, 8),
        bio="EEE Lane, FFF Town. Demo trekking staff member.",
    )

    staff3 = get_or_create_user(
        first_name="Priya",
        last_name="Singh",
        email="staff3.demo@example.com",
        password=STAFF_PASSWORD,
        role="staff",
        contact="0000444400",
        dob=date(2000, 11, 26),
        bio="GGG Avenue, HHH Nagar. Demo trekking staff member.",
    )

    # ========================================================
    # TREKKERS
    # ========================================================

    trekker1 = get_or_create_user(
        first_name="Rohan",
        last_name="Verma",
        email="trekker1.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000333399",
        dob=date(1999, 4, 17),
        bio="AAA Street, BBB Nagar. Weekend trekking enthusiast.",
    )

    trekker2 = get_or_create_user(
        first_name="Karan",
        last_name="Mehta",
        email="trekker2.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000444488",
        dob=date(2001, 11, 3),
        bio="CCC Road, DDD Colony. Interested in mountain trekking.",
    )

    trekker3 = get_or_create_user(
        first_name="Neha",
        last_name="Gupta",
        email="trekker3.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000555577",
        dob=date(1998, 8, 26),
        bio="EEE Lane, FFF Town. Outdoor activity enthusiast.",
    )

    trekker4 = get_or_create_user(
        first_name="Arjun",
        last_name="Patel",
        email="trekker4.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000666666",
        dob=date(2000, 1, 14),
        bio="GGG Street, HHH Colony. Loves weekend adventures.",
    )

    trekker5 = get_or_create_user(
        first_name="Ananya",
        last_name="Joshi",
        email="trekker5.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000777766",
        dob=date(1999, 6, 21),
        bio="III Road, JJJ Nagar. Interested in hiking and nature.",
    )

    trekker6 = get_or_create_user(
        first_name="Vikas",
        last_name="Mishra",
        email="trekker6.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000888855",
        dob=date(2002, 3, 9),
        bio="KKK Lane, LLL Town. Beginner trekking enthusiast.",
    )

    trekker7 = get_or_create_user(
        first_name="Simran",
        last_name="Yadav",
        email="trekker7.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000999944",
        dob=date(1997, 12, 5),
        bio="MMM Road, NNN Colony. Enjoys mountain trails.",
    )

    trekker8 = get_or_create_user(
        first_name="Aditya",
        last_name="Roy",
        email="trekker8.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000123456",
        dob=date(2001, 5, 28),
        bio="OOO Street, PPP Nagar. Adventure and travel enthusiast.",
    )

    trekker9 = get_or_create_user(
        first_name="Isha",
        last_name="Malhotra",
        email="trekker9.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000234567",
        dob=date(1998, 9, 16),
        bio="QQQ Road, RRR Town. Nature lover and trekker.",
    )

    trekker10 = get_or_create_user(
        first_name="Nikhil",
        last_name="Das",
        email="trekker10.demo@example.com",
        password=TREKKER_PASSWORD,
        role="trekker",
        contact="0000345678",
        dob=date(2000, 10, 30),
        bio="SSS Lane, TTT Colony. Interested in outdoor adventures.",
    )

    # ========================================================
    # TREKS
    # ========================================================

    trek1 = get_or_create_trek(
        "TRK001",
        "Kedarkantha Winter Trek",
        "Uttarakhand",
        "moderate",
        5,
        today + timedelta(days=20),
        today + timedelta(days=24),
        "open",
        20,
        7500,
        "A scenic Himalayan winter trek suitable for adventure enthusiasts.",
        staff1,
    )

    trek2 = get_or_create_trek(
        "TRK002",
        "Hampta Pass Trek",
        "Himachal Pradesh",
        "difficult",
        6,
        today + timedelta(days=35),
        today + timedelta(days=40),
        "approved",
        18,
        9000,
        "A high-altitude trek featuring dramatic mountain landscapes.",
        staff1,
    )

    trek3 = get_or_create_trek(
        "TRK003",
        "Rajmachi Fort Trek",
        "Maharashtra",
        "easy",
        2,
        today - timedelta(days=1),
        today + timedelta(days=0),
        "ongoing",
        25,
        3500,
        "A popular fort trek through scenic hills and forest trails.",
        staff2,
    )

    trek4 = get_or_create_trek(
        "TRK004",
        "Valley of Flowers Trek",
        "Uttarakhand",
        "moderate",
        6,
        today + timedelta(days=50),
        today + timedelta(days=55),
        "closed",
        15,
        8500,
        "A beautiful Himalayan trek through alpine meadows and valleys.",
        staff2,
    )

    trek5 = get_or_create_trek(
        "TRK005",
        "Sandakphu Trek",
        "West Bengal",
        "difficult",
        7,
        today - timedelta(days=20),
        today - timedelta(days=14),
        "completed",
        16,
        10500,
        "A challenging trek offering panoramic Himalayan views.",
        staff3,
    )

    trek6 = get_or_create_trek(
        "TRK006",
        "Tadiandamol Trek",
        "Karnataka",
        "moderate",
        3,
        today + timedelta(days=70),
        today + timedelta(days=72),
        "cancelled",
        20,
        4500,
        "A scenic Western Ghats trek surrounded by lush greenery.",
        staff3,
    )

    trek7 = get_or_create_trek(
        "TRK007",
        "Nag Tibba Trek",
        "Uttarakhand",
        "easy",
        2,
        today + timedelta(days=10),
        today + timedelta(days=11),
        "pending",
        25,
        3000,
        "A beginner-friendly weekend trek near the Himalayan foothills.",
        staff1,
    )

    trek8 = get_or_create_trek(
        "TRK008",
        "Brahmatal Trek",
        "Uttarakhand",
        "moderate",
        5,
        today + timedelta(days=80),
        today + timedelta(days=84),
        "open",
        20,
        7000,
        "A winter trek featuring mountain views and alpine landscapes.",
        staff2,
    )

    trek9 = get_or_create_trek(
        "TRK009",
        "Kheerganga Trek",
        "Himachal Pradesh",
        "easy",
        2,
        today + timedelta(days=28),
        today + timedelta(days=29),
        "approved",
        30,
        4000,
        "A short Himalayan trek through forests and mountain villages.",
        staff3,
    )

    # ========================================================
    # BOOKINGS
    # ========================================================

    # TRK001 - OPEN
    get_or_create_booking(
        trek1,
        trekker1,
        "approved",
        7500,
    )

    get_or_create_booking(
        trek1,
        trekker2,
        "pending",
        0,
    )

    get_or_create_booking(
        trek1,
        trekker3,
        "requested",
        0,
    )

    # TRK002 - APPROVED
    get_or_create_booking(
        trek2,
        trekker4,
        "approved",
        9000,
    )

    get_or_create_booking(
        trek2,
        trekker5,
        "rejected",
        0,
    )

    # TRK003 - ONGOING
    get_or_create_booking(
        trek3,
        trekker6,
        "approved",
        3500,
    )

    get_or_create_booking(
        trek3,
        trekker7,
        "cancelled",
        0,
    )

    # TRK004 - CLOSED
    get_or_create_booking(
        trek4,
        trekker8,
        "approved",
        8500,
    )

    # TRK005 - COMPLETED
    get_or_create_booking(
        trek5,
        trekker9,
        "completed",
        10500,
    )

    get_or_create_booking(
        trek5,
        trekker10,
        "completed",
        10500,
    )

    # TRK006 - CANCELLED
    get_or_create_booking(
        trek6,
        trekker1,
        "cancelled",
        0,
    )

    # TRK007 - PENDING
    get_or_create_booking(
        trek7,
        trekker2,
        "pending",
        0,
    )

    # TRK008 - OPEN
    get_or_create_booking(
        trek8,
        trekker3,
        "approved",
        7000,
    )

    # TRK009 - APPROVED
    get_or_create_booking(
        trek9,
        trekker4,
        "requested",
        0,
    )

    # ========================================================
    # BOOKED SLOT COUNTS
    # ========================================================

    all_treks = [
        trek1,
        trek2,
        trek3,
        trek4,
        trek5,
        trek6,
        trek7,
        trek8,
        trek9,
    ]

    for trek in all_treks:
        trek.booked_slots = sum(
            1
            for booking in trek.bookings
            if booking.status in ["approved", "completed"]
        )

    # ========================================================
    # SAVE
    # ========================================================

    db.session.commit()

    print()
    print("=" * 60)
    print("DEMO DATABASE SEEDED SUCCESSFULLY")
    print("=" * 60)

    print()
    print("ADMIN")
    print("-" * 60)
    print("Email    : admin.demo@example.com")
    print("Password : AdminDemo@2026")

    print()
    print("STAFF")
    print("-" * 60)
    print("Email    : staff1.demo@example.com")
    print("Email    : staff2.demo@example.com")
    print("Email    : staff3.demo@example.com")
    print("Password : StaffDemo@2026")

    print()
    print("TREKKER")
    print("-" * 60)
    print("Email    : trekker1.demo@example.com")
    print("Email    : trekker2.demo@example.com")
    print("Email    : trekker3.demo@example.com")
    print("...")
    print("Email    : trekker10.demo@example.com")
    print("Password : TrekkerDemo@2026")

    print()
    print("Database:")
    print(Path(app.instance_path) / "database.sqlite3")

    print()
    print("Seed completed.")