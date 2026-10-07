# Application Tracker

A command-line Python application for tracking graduate job and PhD applications throughout the application process.

The tracker stores applications in a local SQLite database and provides a dashboard summarising current activity, application stages, and upcoming deadlines.

## Current Features

- Add new job or PhD applications
- View all tracked applications
- View the full details of an individual application
- Update existing applications
- Delete applications with confirmation
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

## Dashboard

The application displays a dashboard when it starts.

The dashboard currently shows:

- Number of active applications
- Number of applications added during the current week
- Application pipeline counts for each status
- A simple visual bar for each pipeline stage
- The three nearest upcoming application deadlines

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

UPCOMING
───────────────────────────────────────────────────────
23 Oct  Sellafield Ltd       Radiological Protection & Safety Graduate Programme
02 Nov  MBDA                 Guidance, Control and Navigation Engineer - Graduate Programme 2027
02 Nov  MBDA                 Weapon Systems Algorithms Engineer - Graduate Programme 2027
```

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

- `main.py` — command-line interface and application menu
- `dashboard.py` — dashboard calculations and display
- `database.py` — SQLite database operations and queries
- `models.py` — application data model and application status definitions
- `data/applications.db` — local SQLite database

## Technologies

- Python
- SQLite
- Python dataclasses
- Python enums
- Object-oriented programming
- SQL

## Running the Application

Clone the repository:

```bash
git clone https://github.com/2424hugo/application-tracker.git
cd application-tracker
```

Run the application:

```bash
python main.py
```

## Planned Features

The next major feature is a flexible event system associated with applications.

Each application will be able to have any number of events, such as:

- Interviews
- Online assessments
- Application deadlines
- Follow-ups
- Emails or other correspondence

Events will be linked to individual applications rather than adding a fixed field for every possible stage or activity.

Future development can then use these events to expand the dashboard and provide a clearer view of upcoming application activity.

Add an option to see progress made today, keeping track of changes for that day.

When an application changes from Interested to Applied, the deadline is removed from UPCOMING.
