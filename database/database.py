import sqlite3
import hashlib


DATABASE = "database/telegronomy.db"

# For password
def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

#  establish connection to an SQLite database file
connection = sqlite3.connect(DATABASE)

# create a cursor object from an established database connection
cursor = connection.cursor()

# Creating farmer table. User data
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    location TEXT NOT NULL,
    role TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Creating farm table
cursor.execute("""
CREATE TABLE IF NOT EXISTS farms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_name TEXT NOT NULL,
    location TEXT NOT NULL,
    farm_size REAL NOT NULL,
    size_unit TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# Creating field table
cursor.execute("""
CREATE TABLE IF NOT EXISTS fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    field_size REAL NOT NULL,
    size_unit TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id)
)
""")

# Creating crops table *foreign key( field_id is related to field.id) we need to know where it comes from
cursor.execute("""
CREATE TABLE IF NOT EXISTS crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_id INTEGER NOT NULL,
    crop_name TEXT NOT NULL,
    variety TEXT,
    planting_date TEXT,
    expected_harvest_date TEXT,
    growth_stage TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (field_id) REFERENCES fields(id)
)
""")

# Create crop health assessment table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS crop_health_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_id INTEGER NOT NULL,
    overall_health TEXT NOT NULL,
    symptoms TEXT,
    farmer_notes TEXT,
    assessment_date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(id)
)
""")

# Create crop disease prediction/detection table
cursor.execute("""
CREATE TABLE IF NOT EXISTS disease_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_id INTEGER NOT NULL,
    image_path TEXT,
    predicted_disease TEXT,
    confidence REAL,
    model_version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(id)
)
""")

# -----------------------------
# SAVE CONSULTATION REQUEST
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS agronomist_consultations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    crop_id INTEGER NOT NULL,
    issue TEXT NOT NULL,
    description TEXT NOT NULL,
    image_path TEXT,
    status TEXT NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id)
)
""")
# --------------------------------
# ADD AGRONOMIST RESPONSE FIELDS
# --------------------------------

try:
    cursor.execute("""
        ALTER TABLE agronomist_consultations
        ADD COLUMN agronomist_response TEXT
    """)
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("""
        ALTER TABLE agronomist_consultations
        ADD COLUMN management_advice TEXT
    """)
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("""
        ALTER TABLE agronomist_consultations
        ADD COLUMN follow_up_required TEXT
    """)
except sqlite3.OperationalError:
    pass


# permernet save all pending database modification
connection.commit()
connection.close()


print("Telegronomy database is ready!")