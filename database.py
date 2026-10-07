# Program to handel the SQL using sqlite3
# connects to applications.db, creates applications table and commits change
# 
# Current functions are:
#

import sqlite3
from datetime import date, timedelta, datetime
from models import Application, ApplicationStatus, Event, EventType

DATABASE_PATH = "data/applications.db"

# function to create or connect to the application database
def create_database():
    # connect to the database, if not there create it
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
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
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            title TEXT NOT NULL,
            event_date TEXT NOT NULL,
            notes TEXT,
            completed INTEGER NOT NULL DEFAULT 0
                CHECK (completed IN (0, 1)),
            FOREIGN KEY (application_id) REFERENCES applications(id)
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
                notes,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            application.notes,
            application.created_at.isoformat()
        )

        cursor.execute(sql, values)
        return cursor.lastrowid

# function to add events to the events table in the database
def add_event(event: Event):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        sql = """
            INSERT INTO events (
                application_id,
                event_type,
                title,
                event_date,
                notes,
                completed
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = connection.cursor()
        values = (
            event.application_id,
            event.event_type.value,
            event.title,
            event.event_date.isoformat(),
            event.notes,
            event.completed
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
                notes,
                created_at
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
                notes,
                created_at
            FROM applications
            WHERE id = ?
        """

        cursor.execute(sql, (application_id,))
        row = cursor.fetchone()

    return row_to_application(row)

def get_events(application_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        sql = """
            SELECT id, application_id, event_type, title,
                event_date, notes, completed
            FROM events
            WHERE application_id = ?
            ORDER BY event_date, id
        """

        cursor.execute(sql, (application_id,))
        rows = cursor.fetchall()
    return [row_to_event(row) for row in rows]

def get_event(event_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        sql = """
            SELECT id, application_id, event_type, title,
                event_date, notes, completed
            FROM events
            WHERE id = ?
            ORDER BY event_date, id
        """

        cursor.execute(sql, (event_id,))
        row = cursor.fetchone()
    if row is None:
        return None
    return row_to_event(row)

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

def update_event(event_id: int, event: Event):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        sql = """
            UPDATE events
            SET event_type = ?,
                title = ?,
                event_date = ?,
                notes = ?,
                completed = ?
            WHERE id = ?
        """
        values = (
            event.event_type.value,
            event.title,
            event.event_date.isoformat(),
            event.notes,
            event.completed,
            event_id

        )
        cursor.execute(sql, values)
        return cursor.rowcount

def delete_application(application_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.cursor()
        sql = """
            DELETE FROM applications
            WHERE id = ?
        """
        cursor.execute(sql, (application_id,))
        return cursor.rowcount # returns 1 if found and deleted

def delete_event(event_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.cursor()
        sql = """
            DELETE FROM events
            WHERE id = ?
        """
        cursor.execute(sql, (event_id,))
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
        created_at=datetime.fromisoformat(row[9]),
    )

def row_to_event(row):
    return Event(
        id=row[0],
        application_id=row[1],
        event_type=EventType(row[2]),
        title=row[3],
        event_date=date.fromisoformat(row[4]),
        notes=row[5],
        completed=bool(row[6]),
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

def count_applications_this_week():
    today = date.today()

    # weekday(): Monday = 0, Tuesday = 1, ..., Sunday = 6
    start_of_week = today - timedelta(days=today.weekday())

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        sql = """
            SELECT COUNT(*)
            FROM applications
            WHERE created_at >= ?
        """

        cursor.execute(sql, (start_of_week.isoformat(),))

        return cursor.fetchone()[0]

# function to retrieve the number of applications in each Application Status
def get_pipeline_counts():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        sql = """
            SELECT status, COUNT(*)
            FROM applications
            GROUP BY status
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return {status: count for status, count in results}

def get_upcoming_applications():
    today = date.today().isoformat()

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        sql = """
            SELECT id, organisation, job_title, deadline
            FROM applications
            WHERE deadline IS NOT NULL
                AND deadline >= ?
                AND status = ?
            ORDER BY deadline ASC
            LIMIT 6
        """

        cursor.execute(sql, (today, ApplicationStatus.INTERESTED.value))
        return cursor.fetchall()

def get_upcoming_events():
    today = date.today().isoformat()

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        sql = """
            SELECT applications.id,
                events.id,
                applications.organisation,
                applications.job_title,
                events.event_type,
                events.title,
                events.event_date
            FROM events
            JOIN applications ON events.application_id = applications.id
            WHERE events.completed = 0
            AND events.event_date >= ?
            ORDER BY events.event_date, events.id
            LIMIT 6
        """

        cursor.execute(sql, (today,))
        return cursor.fetchall()

def add_created_at_column():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("""
                ALTER TABLE applications
                ADD COLUMN created_at TEXT
            """)
            print("Added created_at column.")

        except sqlite3.OperationalError as error:
            if "duplicate column name" in str(error):
                print("created_at column already exists.")
            else:
                raise

def update_existing_created_at():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE applications
            SET created_at = CURRENT_TIMESTAMP
            WHERE created_at IS NULL
        """)

        print(f"Updated {cursor.rowcount} applications.")

def main():
    pass

if __name__ == "__main__":
    main()