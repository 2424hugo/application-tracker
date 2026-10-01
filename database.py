# Program to handel the SQL using sqlite3
# connects to applications.db, creates applications table and commits change
# 
# Current functions are:
#

import sqlite3
from datetime import date
from models import Application, ApplicationStatus

DATABASE_PATH = "data/applications.db"

# function to create or connect to the application database
def create_database():
    # connect to the database, if not there create it
    connection = sqlite3.connect(DATABASE_PATH)
    # cursor object used to send SQL commands to database
    cursor = connection.cursor()
    # create the table for the database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organisation TEXT NOT NULL,
            job_title TEXT NOT NULL,
            status TEXT NOT NULL,
            salary REAL,
            deadline TEXT,
            location TEXT,
            url TEXT,
            notes TEXT
        )
    """)
    connection.commit() # commit to database
    connection.close() # close connection

# function to add applications to the applications table in the database
def add_application(application: Application):
    with sqlite3.connect(DATABASE_PATH) as connection:
        sql = """
            INSERT INTO applications (
                organisation,
                job_title,
                status,
                salary,
                deadline,
                location,
                url,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = connection.cursor()
        values = (
            application.organisation,
            application.job_title,
            application.status.value,
            application.salary,
            application.deadline.isoformat() if application.deadline else None,
            application.location,
            application.url,
            application.notes
        )

        cursor.execute(sql, values)
        return cursor.lastrowid

# fuction to retrive all applications
def get_applications():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        sql = """
            SELECT id,
                organisation,
                job_title,
                status,
                salary,
                deadline,
                location,
                url,
                notes
            FROM applications
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

    return [row_to_application(row) for row in rows]

def get_application(application_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        sql = """
            SELECT id,
                organisation,
                job_title,
                status,
                salary,
                deadline,
                location,
                url,
                notes
            FROM applications
            WHERE id = ?
        """

        cursor.execute(sql, (application_id,))
        row = cursor.fetchone()

    return row_to_application(row)

def update_application(application_id: int, application: Application):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        sql = """
            UPDATE applications
            SET
                organisation = ?,
                job_title = ?,
                status = ?,
                salary = ?,
                deadline = ?,
                location = ?,
                url = ?,
                notes = ?
            WHERE id = ?
        """
        values = (
            application.organisation,
            application.job_title,
            application.status.value,
            application.salary,
            application.deadline.isoformat() if application.deadline else None,
            application.location,
            application.url,
            application.notes,
            application_id
        )
        cursor.execute(sql, values)
        return cursor.rowcount

def delete_application(application_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        sql = """
            DELETE FROM applications
            WHERE id = ?
        """
        cursor.execute(sql, (application_id,))
        return cursor.rowcount # returns 1 if found and deleted

def row_to_application(row):
    if row is None:
        return None

    return Application(
        id=row[0],
        organisation=row[1],
        job_title=row[2],
        status=ApplicationStatus(row[3]),
        salary=row[4],
        deadline=date.fromisoformat(row[5]) if row[5] else None,
        location=row[6],
        url=row[7],
        notes=row[8],
    )

def number_of_applications():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        sql = """
            SELECT count(*)
            FROM applications
        """
        cursor.execute(sql)
        return cursor.fetchone()[0]

def main():
    create_database()

    print("All current applications:")

    applications = get_applications()

    for application in applications:
        print(application)


if __name__ == "__main__":
    main()