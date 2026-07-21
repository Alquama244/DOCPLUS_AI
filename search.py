import sqlite3
from typing import Optional


def get_doctor_schedule(doctor_name: Optional[str] = None, specialty: Optional[str] = None) -> str:
    """
    Searches hospital.db for doctors matching a name or specialty.

    Args:
        doctor_name: The name of the doctor to search for (e.g. "Sharma").
            Partial matches are supported. Leave empty to search by specialty only.
        specialty: The medical specialty/department to search for (e.g. "Cardiology").
            Partial matches are supported. Leave empty to search by name only.
    """
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    query = "SELECT name, specialty, days, shift_time FROM doctors WHERE 1=1"
    params = []

    if doctor_name:
        query += " AND name LIKE ?"
        params.append(f"%{doctor_name}%")

    if specialty:
        query += " AND specialty LIKE ?"
        params.append(f"%{specialty}%")

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No matching doctor or department found in database."

    # Format output nicely
    formatted_results = []
    for name, spec, days, shift in results:
        formatted_results.append(f"👨‍⚕️ {name} ({spec}) | Available: {days} | Shift: {shift}")

    return "\n".join(formatted_results)


# --- QUICK TEST ---
if __name__ == "__main__":
    print("--- Test 1: Search Cardiology ---")
    print(get_doctor_schedule(specialty="Cardiology"))

    print("\n--- Test 2: Search Dr. Sharma ---")
    print(get_doctor_schedule(doctor_name="Sharma"))