import sqlite3

def setup_database():
    # 1. Connect to or create the database file
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    # 2. Create the table for doctors
    # id is a column that identify each docter
    # primary key means this column uniquely identifies every row — no duplicates allowed
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            days TEXT NOT NULL,
            shift_time TEXT NOT NULL
        )   
    """)

    # 3. Add sample doctors if the database is empty
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] == 0:
        sample_doctors = [
            ("Dr. Anjali Sharma", "Cardiology", "Mon, Wed, Fri", "09:00 AM - 01:00 PM"),
            ("Dr. Rajesh Kumar", "Pediatrics", "Tue, Thu, Sat", "02:00 PM - 06:00 PM"),
            ("Dr. Priya Singh", "Dermatology", "Mon to Sat", "10:00 AM - 04:00 PM")
        ]
        cursor.executemany("""
            INSERT INTO doctors (name, specialty, days, shift_time)
            VALUES (?, ?, ?, ?)
        """, sample_doctors)
        conn.commit()

    conn.close()
    print(" Success! 'hospital.db' created with doctor records.")

if __name__ == "__main__":
    setup_database()    