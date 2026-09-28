import sqlite3
import re
import ast
import operator
from datetime import datetime

def init_db():
    """Ensures hospital.db exists and contains sample doctors."""
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            specialty TEXT,
            days TEXT,
            shift_time TEXT
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] == 0:
        sample_doctors = [
            ("Dr. Smith", "Cardiology", "Mon, Wed, Fri", "09:00 AM - 01:00 PM"),
            ("Dr. John", "Pediatrics", "Tue, Thu, Sat", "10:00 AM - 02:00 PM"),
            ("Dr. Sarah", "Dermatology", "Mon, Thu", "02:00 PM - 06:00 PM"),
            ("Dr. Sharma", "Neurology", "Wed, Sat", "11:00 AM - 03:00 PM"),
            ("Dr. Kumar", "General Medicine", "Mon to Sat", "08:00 AM - 04:00 PM")
        ]
        cursor.executemany("INSERT INTO doctors (name, specialty, days, shift_time) VALUES (?, ?, ?, ?)", sample_doctors)
        conn.commit()
    conn.close()

# Auto-initialize database on import
init_db()

def get_doctor_schedule(query_text: str) -> str:
    """
    Searches hospital database for doctor availability by keyword extraction.
    """
    try:
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, specialty, days, shift_time FROM doctors")
        records = cursor.fetchall()
        conn.close()

        q = query_text.lower()
        matched = []

        for name, spec, days, shift in records:
            doc_name_parts = [p.lower() for p in name.replace("Dr.", "").strip().split()]
            if any(part in q for part in doc_name_parts if len(part) > 2) or spec.lower() in q:
                matched.append(f"👨‍⚕️ {name} ({spec}) | Days: {days} | Shift: {shift}")

        if matched:
            return "\n".join(matched)

        all_docs = [f"👨‍⚕️ {name} ({spec}) | Days: {days} | Shift: {shift}" for name, spec, days, shift in records]
        return "Doctor Directory:\n" + "\n".join(all_docs)

    except Exception as e:
        return f"Database query error: {str(e)}"

def get_current_time(query: str = "") -> str:
    """Returns current date and time."""
    now = datetime.now()
    return f"🕒 Current Date & Time: {now.strftime('%A, %B %d, %Y - %I:%M %p')}"

def calculate(expression: str) -> str:
    """
    Evaluates basic arithmetic expressions safely across all Python versions.
    """
    try:
        match = re.search(r'[\d\.\s\+\-\*\/\(\)]+', expression)
        if not match:
            return "Error: No math expression detected."

        clean_expr = match.group(0).strip()
        if not clean_expr or not any(char.isdigit() for char in clean_expr):
            return "Error: Please provide numbers to calculate (e.g., 25 * 4)."

        tree = ast.parse(clean_expr, mode='eval')

        def eval_node(node):
            if isinstance(node, getattr(ast, 'Constant', ast.Num)):
                return node.value if hasattr(node, 'value') else node.n
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                op_map = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv
                }
                return op_map[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                op = eval_node(node.operand)
                return -op if isinstance(node.op, ast.USub) else op
            else:
                raise ValueError("Unsupported node")

        res = eval_node(tree.body)
        if isinstance(res, float) and res.is_integer():
            res = int(res)

        return f"🔢 Calculation Result: {res}"
    except Exception as e:
        return f"Error evaluating calculation: {str(e)}"