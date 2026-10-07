# Application Tracker

A command-line Python application for tracking graduate job and PhD applications throughout the application process.

The tracker stores applications and their associated events in a local SQLite database. A dashboard summarises application stages and upcoming deadlines and activities.

## Application Features

- Add, view, update, and delete applications
- View the full details and events of an individual application
- Confirm before deleting an application
- Track application status through:
  - Interested
  - Applied
  - Online Assessment
  - Interview
  - Offer
  - Rejected
- Store application details including:
  - Organisation
  - Job title
  - Salary
  - Application deadline
  - Location
  - Job URL
  - Notes
- Automatically record when an application is added
- Store application data persistently using SQLite

## Application Events

Each application can have any number of associated events.

Supported event types:

- Online Assessment
- Interview
- Follow-up
- Email
- Other

Each event contains:

- A unique event ID
- The ID of its associated application
- Event type
- Title
- Date
- Notes
- Completion state

Event features:

- Add events to existing applications
- View events within an application's details
- Mark events as completed
- Edit event details
- Reopen completed events
- Clear event notes when editing
- Delete events with confirmation

Events are stored in a separate table linked to applications through a foreign key. Each event requires a date; times are not currently recorded.

Completing an event does not automatically change the application's status.

## Dashboard

The dashboard appears when the application starts and shows:

- Number of active applications
- Number of applications added during the current week
- Application pipeline counts with visual bars
- The three nearest upcoming activities, ordered by date

Example:

```text
APPLICATION TRACKER
───────────────────────────────────────────────────────

Active applications:     5
Applications this week:  5

PIPELINE
───────────────────────────────────────────────────────
Interested             4  ████
Applied                1  █
Online Assessment      0
Interview              0
Offer                   0
Rejected                0
```
UPCOMING combines:

- Application deadlines for applications with the status **Interested**
- Pending events dated today or later, regardless of application status

Completed events are excluded. Application deadlines disappear from UPCOMING when the application is no longer Interested.

Each upcoming activity displays its application ID. Event entries also display their event ID, allowing them to be located for editing, completion, or deletion.

Example:

```text
UPCOMING
───────────────────────────────────────────────────────
10 Oct  [App ID: 5 | Event ID: 2] ORGANISATION — JOB TITLE
        Online Assessment: Online Situational Judgement Test (SJT)
23 Oct  [App ID: 3] ORGANISATION — JOB TITLE
        Application Deadline
02 Nov  [App ID: 5] ORGANISATION — JOB TITLE
        Application Deadline
```

The dashboard currently refreshes when the program starts. Restart the tracker to see changes reflected in the dashboard.

## Application Menu

1. Add application
2. View all applications
3. View application
4. Update application
5. Delete application
6. Add event
7. Complete event
8. Update event
9. Delete event
10. Exit

## Project Structure

```text
application-tracker/
├── data/
│   └── applications.db
├── dashboard.py
├── database.py
├── main.py
├── models.py
└── README.md
```

- `main.py` — command-line interface and application/event menus
- `dashboard.py` — dashboard calculations and display
- `database.py` — SQLite table creation, storage operations, and queries
- `models.py` — application and event dataclasses, application statuses, and event types
- `data/applications.db` — local SQLite database containing applications and events

Database files are excluded from Git through `.gitignore`.

## Technologies

- Python
- SQLite
- Python dataclasses
- Python enums
- SQL

The application uses Python's standard library and requires no third-party packages.

## Running the Application

Clone the repository:

```bash
git clone https://github.com/2424hugo/application-tracker.git
cd application-tracker
```

Run from the project folder:

```bash
python main.py
```

Ensure the `data` folder exists before the first run. The application creates the database and required tables automatically.

Enter dates in `YYYY-MM-DD` format and status or event type names exactly as displayed.

## Planned Features

- Input validation for IDs, dates, statuses, and event types
- An overdue section for pending events whose dates have passed
- Dashboard refresh during use
- A daily activity summary showing progress and changes
- Clear handling of application deletion when associated events exist
