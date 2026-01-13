import pymysql
from datetime import datetime

def insert_to_db(face_id, gender, age, confidence):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="53787",
        database="age_gender_db"
    )
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO person_detection
        (face_uid, gender, age_range, confidence, first_seen, last_seen)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        f"FACE_{face_id}",
        gender,
        age,
        confidence,
        datetime.now(),
        datetime.now()
    ))

    conn.commit()
    cursor.close()
    conn.close()
