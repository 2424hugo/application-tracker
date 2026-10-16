# Application Tracker

A Python application for tracking graduate job and PhD applications throughout the recruitment process, featuring a command-line interface (CLI) and a graphical user interface (GUI) built with PySide6.

The tracker stores applications and their associated events in a local SQLite database. Both interfaces use the same database, allowing application information to be managed through the CLI and displayed through the GUI.

The project is being developed incrementally, with the aim of providing a complete desktop application for managing job applications, deadlines, interviews, and assessments.

## Current Features

### Command-Line Interface

The CLI provides functionality for managing applications and their associated events.

**Application management:**

- Add, view, update, and delete applications
- View all applications, grouped by application status
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

### Graphical User Interface (PySide6)

A desktop GUI is under development using PySide6.

**Implemented GUI features:**

- Main application window with sidebar navigation
- Separate Dashboard, Applications, and Events navigation pages
- Dashboard displaying live data retrieved from SQLite when initialised
- Application pipeline visualisation using progress bars
- Upcoming and overdue application deadlines and events
- Scrollable dashboard layout
- Read-only tables with individually selectable cells
- Applications table displaying:
  - Application ID
  - Organisation
  - Job title
  - Application status
  - Deadline
  - Location
- Live searching by organisation or job title
- Application status filtering using a dropdown menu
- Combined search and status filtering
- Reusable methods for refreshing displayed database information

The Dashboard and Applications views are functional. The Events page currently contains placeholder content.

Adding, editing, and deleting applications through the GUI are planned features. These operations are currently available through the CLI.

## Application Events

Each application can have any number of associated events.

**Supported event types:**

- Online Assessment
- Interview
- Follow-up
- Email
- Other

**Each event contains:**

- A unique event ID
- The ID of its associated application
- Event type
- Title
- Date
- Notes
- Completion state

**Event management features (CLI):**

- Add events to existing applications
- View events within an application's details
- Mark events as completed
- Edit event details
- Reopen completed events
- Clear event notes when editing
- Delete events with confirmation

Events are stored in a separate SQLite table linked to applications through a foreign key.

Each event requires a date; times are not currently recorded.

Completing an event does not automatically change the application's status.

## Dashboard

Both interfaces provide a dashboard summarising application activity.

### Application Statistics

The dashboard displays:

- Number of active applications
- Number of applications added during the current week
- Application counts grouped by status
- Visual representations of the application pipeline

The CLI uses text-based bars, while the GUI uses `QProgressBar` widgets.

In the GUI, each progress bar represents the percentage of all tracked applications belonging to that status, including rejected applications.

**Example CLI output:**

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
Offer                  0
Rejected                0
```

### Upcoming Deadlines and Events

The UPCOMING section combines:

- Application deadlines for applications with the status **Interested**
- Pending events dated today or later, regardless of application status

Completed events are excluded. Application deadlines disappear from UPCOMING when the application is no longer Interested.

Activities are ordered chronologically, with the nearest dates first.

The CLI provides a summary of upcoming activities.

**Example CLI output:**

```text
UPCOMING
───────────────────────────────────────────────────────
10 Oct  [App ID: 5 | Event ID: 2] ORGANISATION — JOB TITLE
        Online Assessment: Online Situational Judgement Test

23 Oct  [App ID: 3] ORGANISATION — JOB TITLE
        Application Deadline

02 Nov  [App ID: 5] ORGANISATION — JOB TITLE
        Application Deadline
```

The GUI presents upcoming activities in a table containing:

- Date
- Organisation
- Job Title / Event
- Type
- Application ID

Application deadlines and events are retrieved from separate database tables, combined into a common data structure, and sorted chronologically.

### Overdue Deadlines and Events

The OVERDUE section identifies:

- Past application deadlines that remain relevant to applications with the status Interested
- Pending events whose scheduled dates have passed

The GUI displays overdue activities in a separate table, ordered from most recently overdue to oldest.

### GUI Dashboard Layout

The graphical dashboard uses:

- `QVBoxLayout` for organising content vertically
- `QLabel` for application statistics and headings
- `QProgressBar` for pipeline visualisation
- `QFrame` for section separators
- `QTableWidget` for upcoming and overdue activities
- `QScrollArea` for vertical scrolling

The dashboard provides a `refresh()` method that retrieves updated information from SQLite.

Currently, dashboard information is loaded when the GUI starts. Automatic updating following changes to application data is planned.

## Applications View (GUI)

The Applications page provides a graphical overview of all tracked applications.

Applications are retrieved from SQLite and displayed in a six-column `QTableWidget`.

### Searching

A `QLineEdit` search field provides live, case-insensitive searching across:

- Organisation
- Job title

Table rows are automatically hidden or displayed as the search text changes.

### Status Filtering

A `QComboBox` allows applications to be filtered by status:

- All statuses
- Interested
- Applied
- Online Assessment
- Interview
- Offer
- Rejected

Searching and status filtering can be used simultaneously.

For example, searching for `nuclear` while selecting `Applied` displays only applied applications whose organisation or job title contains that term.

Filtering operates on the existing table contents without repeatedly querying SQLite.

The table is read-only to prevent changes that would not be saved to the database.

## Application Menu (CLI)

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
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── dashboard_view.py
│   └── applications_view.py
│
├── gui_main.py
├── dashboard.py
├── database.py
├── main.py
├── models.py
├── .gitignore
└── README.md
```

**Core files:**

- `main.py` — command-line interface and application/event menus
- `gui_main.py` — entry point for launching the PySide6 GUI
- `dashboard.py` — dashboard calculations and CLI display
- `database.py` — SQLite table creation, storage operations, and queries
- `models.py` — application and event dataclasses, application statuses, and event types

**GUI components:**

- `gui/main_window.py` — main application window, navigation sidebar, and page management
- `gui/dashboard_view.py` — application statistics, pipeline visualisation, and upcoming/overdue tables
- `gui/applications_view.py` — applications table, searching, and status filtering
- `gui/__init__.py` — Python package initialisation

**Database:**

- `data/applications.db` — local SQLite database containing applications and events

Database files and local backups are excluded from Git through `.gitignore`.

## Technologies

- Python
- PySide6 (Qt for Python)
- SQLite
- Python dataclasses
- Python enums
- SQL
- Git and GitHub

The CLI uses Python's standard library and requires no additional packages.

The GUI requires PySide6.

## Running the Application

### 1. Clone the Repository

```bash
git clone https://github.com/2424hugo/application-tracker.git
cd application-tracker
```

The GUI is currently being developed on the `feature/pyside6-gui` branch. If these changes have not yet been merged into `main`, switch to that branch:

```bash
git switch feature/pyside6-gui
```

### 2. Run the Command-Line Interface

The CLI requires no third-party dependencies.

Run:

```bash
python main.py
```

Ensure the `data` directory exists before the first run. The application creates the SQLite database and required tables automatically.

Enter dates in `YYYY-MM-DD` format and status or event type names exactly as displayed.

### 3. Run the Graphical Interface

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows using PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install PySide6:

```bash
python -m pip install PySide6
```

Launch the GUI:

```bash
python gui_main.py
```

The graphical application will open with navigation between the Dashboard, Applications, and Events pages.

Both interfaces use the same SQLite database.

### Database Storage

Application and event records are stored locally in:

```text
data/applications.db
```

The database is excluded from version control, so cloning the repository does not include existing application records.

Back up the database before making significant structural changes.

## Planned Features

### GUI Development

- View full application details in a separate dialog
- Add applications through the GUI
- Edit application information
- Delete applications with confirmation
- Display associated events in the application details view
- Add, edit, complete, and delete events through the GUI
- Implement the Events page
- Automatically refresh dashboard statistics and tables after changes
- Enable additional application table sorting
- Support copying selected table cells using keyboard shortcuts
- Improve styling and visual consistency
- Package the GUI as a Windows executable

### General Improvements

- Expand input validation for IDs, dates, statuses, and event types
- Improve error handling and database operation feedback
- Add automated tests for database and application functionality
- Introduce a daily activity summary showing progress and changes
- Improve handling of application deletion when associated events exist

## Development

The project is being developed incrementally, beginning with a functional command-line application and extending its existing database functionality into a graphical interface.

The GUI is currently being developed on the `feature/pyside6-gui` branch.

The long-term objective is to provide a complete desktop application for managing graduate job and PhD applications while maintaining a clear separation between the database, application logic, and user interface.
