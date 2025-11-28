import sqlite3
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger("fraud-db")

DB_PATH = Path(__file__).parent.parent / "fraud_cases.db"

def init_db():
    """Initialize the database with the fraud_cases table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_cases (
            username TEXT PRIMARY KEY,
            security_identifier TEXT,
            card_ending TEXT,
            status TEXT,
            transaction_name TEXT,
            transaction_amount TEXT,
            transaction_time TEXT,
            transaction_city TEXT,
            transaction_merchant TEXT,
            security_question TEXT,
            security_answer TEXT,
            outcome_note TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def seed_db():
    """Seed the database with sample data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Sample data
    cases = [
        (
            "john_doe",
            "12345",
            "4242",
            "pending_review",
            "Electronics Purchase",
            "₹85,000",
            "2023-10-27 14:30:00",
            "New Delhi, India",
            "Croma Electronics",
            "What is your mother's maiden name?",
            "Smith",
            ""
        ),
        (
            "jane_smith",
            "67890",
            "8888",
            "pending_review",
            "Luxury Hotel Stay",
            "₹25,000",
            "2023-10-26 09:15:00",
            "Mumbai, India",
            "Taj Mahal Palace",
            "What was the name of your first pet?",
            "Fluffy",
            ""
        ),
        (
            "alice_wonder",
            "11223",
            "9090",
            "pending_review",
            "Crypto Exchange Transfer",
            "₹50,000",
            "2023-10-28 03:45:00",
            "Unknown Location",
            "WazirX",
            "What is the name of your favorite teacher?",
            "Mrs. Johnson",
            ""
        ),
        (
            "bob_builder",
            "33445",
            "1212",
            "pending_review",
            "Construction Supplies",
            "₹15,000",
            "2023-10-25 11:20:00",
            "Bangalore, India",
            "Asian Paints Store",
            "What city were you born in?",
            "Chicago",
            ""
        ),
        (
            "charlie_brown",
            "55667",
            "3434",
            "pending_review",
            "Gaming Console",
            "₹49,990",
            "2023-10-29 18:10:00",
            "Hyderabad, India",
            "Sony Center",
            "What is your favorite sports team?",
            "Yankees",
            ""
        ),
        (
            "priyanshujha",
            "99887",
            "1818",
            "pending_review",
            "VIP Match Tickets",
            "₹12,500",
            "2023-11-05 10:00:00",
            "Ahmedabad, India",
            "BookMyShow",
            "Who is your favorite cricketer?",
            "Virat Kohli",
            ""
        ),
        (
            "reet_singh",
            "55443",
            "7777",
            "pending_review",
            "International Flight Booking",
            "₹1,20,000",
            "2023-11-10 08:00:00",
            "Chandigarh, India",
            "MakeMyTrip",
            "What is your favorite food?",
            "Butter Chicken",
            ""
        )
    ]
    
    for case in cases:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO fraud_cases (
                    username, security_identifier, card_ending, status,
                    transaction_name, transaction_amount, transaction_time,
                    transaction_city, transaction_merchant, security_question,
                    security_answer, outcome_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, case)
        except sqlite3.Error as e:
            logger.error(f"Error seeding case {case[0]}: {e}")
            
    conn.commit()
    conn.close()
    logger.info("Database seeded successfully.")

def get_case(username: str) -> Optional[Dict[str, Any]]:
    """Retrieve a fraud case by username."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM fraud_cases WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return dict(row)
    return None

def find_user_fuzzy(input_name: str) -> Optional[Dict[str, Any]]:
    """Find a user by matching name ignoring underscores, spaces, and case."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Normalize input: remove spaces, underscores, lowercase
    clean_input = input_name.replace(" ", "").replace("_", "").lower()
    
    cursor.execute("SELECT * FROM fraud_cases")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        db_user = row["username"]
        # Normalize db user
        clean_db = db_user.replace("_", "").lower()
        if clean_db == clean_input:
            return dict(row)
            
    return None

def update_case_status(username: str, status: str, note: str):
    """Update the status and outcome note of a fraud case."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE fraud_cases 
        SET status = ?, outcome_note = ?
        WHERE username = ?
    """, (status, note, username))
    
    conn.commit()
    conn.close()
    logger.info(f"Updated case for {username} to {status}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
    seed_db()
