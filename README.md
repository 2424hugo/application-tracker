# Application Tracker

A Python application for tracking graduate job and PhD applications through the recruitment process. It includes a command-line interface (CLI) and a desktop graphical user interface (GUI) built with PySide6.

Applications and their associated events are stored locally in SQLite. Both interfaces use the same database.

**Development status:** The CLI is functional. The PySide6 GUI is under active development on the `feature/pyside6-gui` branch and supports application and event management, a dashboard, searching and filtering, and an events calendar.

## Current Features

### Command-Line Interface

- Add, view, update, and delete applications, with deletion confirmation
- View applications grouped by recruitment status
- View an application's full details and associated events
- Add, complete, edit, reopen, and delete events
- Dashboard showing application statistics, recruitment stages, and upcoming activity
- Persist application and event data in a local SQLite database

### Graphical User Interface (PySide6)

The desktop interface contains three pages, accessible using the sidebar.

**Dashboard**

- Active application count and records added during the current week
- Application pipeline counts and percentage-based progress bars
- Upcoming and overdue application deadlines and pending events
- Scrollable layout and tables showing date, organisation, job/event, type, and application ID
- Double-click a deadline to edit the application, or an event to edit the event

**Applications**

- Table showing application ID, organisation, job title, status, deadline, and location
- Live, case-insensitive search by organisation or job title
- Status dropdown filter, which works together with the search field
- Double-click a row to edit its application
- Add, edit, and delete applications through the **Applications** menu
- Validation of required fields and numeric salary values
- Confirm application deletion, with a warning about linked events

**Events**

- Interactive calendar showing application deadlines and pending events
- Calendar weeks begin on Monday, with counts of due items on relevant dates
- Select a date to view its scheduled deadlines and events
- **Today** and **Refresh** buttons
- Double-click a listed calendar item to edit its application or event
- Add, complete, update, and delete events through the **Events** menu
- Reopen events by unchecking **Completed** in the event editing dialog

After a successful change made using a GUI menu or editing dialog, the Dashboard, Applications, and Events pages refresh. The Events page also refreshes when opened.

**Current limitation:** There is no separate read-only application detail page in the GUI. Double-clicking an application opens its editor.

## Applications and Recruitment Status

Each application stores:

- Unique application ID
- Organisation and job title
- Recruitment status
- Salary (optional)
- Application deadline (optional)
- Location
- Job URL
- Notes
- Record creation date and time

Supported statuses:

1. Interested
2. Applied
3. Online Assessment
4. Interview
5. Offer
6. Rejected

**Applications this week** counts records *created* during the current week, not necessarily applications submitted to employers during that week.

## Application Events

Each application can have multiple associated events, stored in a separate SQLite table and linked by application ID.

Supported event types:

- Online Assessment
- Interview
- Follow-up
- Email
- Other

Each event stores a unique ID, associated application ID, event type, title, date, notes, and a completed/pending flag.

The CLI and GUI support adding, editing, completing, reopening, and deleting events. Completing an event does **not** automatically change its application's status.

**Events currently record dates, not times.** An interview can be scheduled for a particular day, but its hour cannot yet be entered separately.

### Upcoming, Overdue, and Calendar Rules

- Application deadlines appear only for applications with status **Interested**.
- Pending events appear regardless of their associated application's status.
- Completed events are excluded from upcoming, overdue, and calendar activity lists.
- Upcoming entries are dated today or later; overdue entries are dated before today.
- Upcoming items are ordered from earliest to latest; the GUI overdue table shows the most recently overdue items first.
- The calendar can show past and future pending items on their respective dates.

Changing an application's status away from **Interested** removes its deadline from these activity views without deleting the deadline from its database record.

## Dashboard

Both interfaces display application statistics and upcoming activities. The GUI also displays overdue activities.

The GUI's progress bars show the proportion of **all tracked applications** in each recruitment status, including rejected applications.

Upcoming deadline and event records are retrieved from SQLite, combined, and sorted chronologically. On the GUI, a double-click opens the corresponding editor.

## Project Structure

```text
application-tracker/
├── data/
│   └── applications.db        # Created locally; not tracked by Git
├── gui/
│   ├── __init__.py
│   ├── main_window.py         # Main window and navigation
│   ├── dashboard_view.py      # Statistics, upcoming and overdue tables
│   ├── applications_view.py   # Application table, search and filtering
│   ├── events_view.py         # Events calendar
│   └── menu_actions.py        # GUI menus and editing dialogs
├── gui_main.py                # GUI entry point
├── main.py                    # CLI entry point
├── dashboard.py               # CLI dashboard logic
├── database.py                # SQLite schema and database operations
├── models.py                  # Dataclasses and enums
├── .gitignore
└── README.md
```

The database keeps application records and their events in related tables. Deleting an application through the application deletion function also deletes its linked events.

## Technologies

- Python
- PySide6 (Qt for Python)
- SQLite / SQL
- Python dataclasses and enums
- Git and GitHub

The CLI uses the Python standard library. The GUI requires PySide6.

## Installation and Running

### 1. Clone the Repository

```bash
git clone https://github.com/2424hugo/application-tracker.git
cd application-tracker
git switch feature/pyside6-gui
```

The PySide6 GUI is currently developed on the `feature/pyside6-gui` branch rather than the default `main` branch.

### 2. Create a Virtual Environment

On Windows using PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install PySide6
```

### 3. Initialise the Database

Before launching the GUI for the first time, create the data directory and initialise the database:

```powershell
python -c "from pathlib import Path; Path('data').mkdir(exist_ok=True); from database import create_database; create_database()"
```

The CLI initialises database tables on startup, but `gui_main.py` does not yet call `create_database()`. If your database is already initialised, this step is unnecessary.

### 4. Launch the Application

GUI:

```powershell
python gui_main.py
```

CLI:

```powershell
python main.py
```

Run these commands from the project root. The current database path is relative to the working directory.

### Data Storage and Backups

Application and event records are stored in:

```text
data/applications.db
```

Database files under `data/` are excluded from Git. Cloning the repository therefore does not restore personal application records.

Back up the database somewhere secure, especially before changing the database schema. Automatic backups and migrations have not yet been implemented.

## Planned Improvements

### Next Priorities

- Make database paths independent of the current working directory
- Initialise the database automatically when launching the GUI
- Add a read-only application detail page with notes and linked events
- Support start times for interviews and other events
- Add application table sorting
- Introduce automatic backups and database schema migrations
- Add automated tests for database operations, date filtering, and record deletion

### Longer-Term Features

- Application priorities and reminders for next actions
- Recruitment status history and date an application was submitted
- CSV export and calendar event export to ICS files
- More detailed application and recruitment outcome statistics
- Improved styling, keyboard shortcuts, and table interactions
- Optional desktop notifications for approaching deadlines and events
- Windows executable packaging

## Development

The project began as a command-line tool and is being extended into a desktop application while retaining the shared SQLite storage and Python data models.

The focus is on practical application management and a maintainable separation of database operations, application logic, and GUI components.
