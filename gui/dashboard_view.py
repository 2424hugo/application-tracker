from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QLabel, 
    QProgressBar,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QScrollArea,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal

from database import (
    get_pipeline_counts,
    count_applications_this_week,
    get_upcoming_applications,
    get_upcoming_events,
    get_overdue_applications,
    get_overdue_events,
)
from dashboard import count_active_applications
from models import ApplicationStatus

class DashboardView(QWidget):
    application_edit_requested = Signal(int)
    event_edit_requested = Signal(int)

    def __init__(self):
        super().__init__()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # founts
        heading_font = QFont()
        heading_font.setPointSize(12)
        heading_font.setBold(True)

        # Create a vertical layout
        dashboard_layout = QVBoxLayout()

        # SQLite info

        # APPLICATION TRACKER
        application_tracker_heading = QLabel("APPLICATION TRACKER")
        application_tracker_heading.setFont(heading_font)
        dashboard_layout.addWidget(application_tracker_heading)
        dashboard_layout.addWidget(self.separator())
        self.active_applications_label = QLabel("Active Applications: —")
        dashboard_layout.addWidget(self.active_applications_label)
        self.this_week_label = QLabel("Applications this week: -")
        dashboard_layout.addWidget(self.this_week_label)

        dashboard_layout.addSpacing(15)

        # PIPLINE
        pipeline_heading = QLabel("PIPELINE")
        pipeline_heading.setFont(heading_font)
        dashboard_layout.addWidget(pipeline_heading)
        dashboard_layout.addWidget(self.separator())
        self.pipeline_bars = {}
        self.pipeline_labels = {}
        for status in ApplicationStatus:
            label = QLabel(status.value)
            self.pipeline_labels[status.value] = label
            dashboard_layout.addWidget(label)

            progress_bar = QProgressBar()
            progress_bar.setFormat("%p%")
            progress_bar.setRange(0, 100)
            self.pipeline_bars[status.value] = progress_bar
            dashboard_layout.addWidget(progress_bar)

        # UPCOMING
        upcoming_heading = QLabel("UPCOMING")
        upcoming_heading.setFont(heading_font)
        dashboard_layout.addWidget(upcoming_heading)
        dashboard_layout.addWidget(self.separator())
        self.upcoming_table = self.create_event_table()
        self.upcoming_table.cellDoubleClicked.connect(
            lambda row, column: self.edit_clicked_item(
                self.upcoming_table, row
            )
        )
        self.upcoming_table.setFixedHeight(220)
        dashboard_layout.addWidget(self.upcoming_table)

        # OVERDUE
        overdue_heading = QLabel("OVERDUE")
        overdue_heading.setFont(heading_font)
        dashboard_layout.addWidget(overdue_heading)
        dashboard_layout.addWidget(self.separator())
        self.overdue_table = self.create_event_table()
        self.overdue_table.cellDoubleClicked.connect(
            lambda row, column: self.edit_clicked_item(
                self.overdue_table, row
            )
        )
        self.overdue_table.setFixedHeight(220)
        dashboard_layout.addWidget(self.overdue_table)

        # Widget containing all dashboard content
        content_widget = QWidget()
        content_widget.setLayout(dashboard_layout)

        # Put the content widget inside the scroll area
        scroll_area.setWidget(content_widget)

        # Layout belonging to DashboardView itself
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.refresh()

    def refresh(self):
        pipeline = get_pipeline_counts()
        active_applications = count_active_applications(pipeline)
        total_applications = sum(pipeline.values())
        applications_this_week = count_applications_this_week()

        self.active_applications_label.setText(f"Active Applications: {active_applications}")
        for status in ApplicationStatus:
            count = pipeline.get(status.value, 0)
            self.pipeline_labels[status.value].setText(f"{status.value}: {count}")
            if total_applications > 0:
                percentage = round((count/total_applications)*100)
            else:
                percentage = 0
            self.pipeline_bars[status.value].setValue(percentage)

        self.this_week_label.setText(f"Applications this week: {applications_this_week}")

        upcoming = []
        # Application deadlines
        for application_id, organisation, job_title, deadline in get_upcoming_applications():
            upcoming.append((
                deadline,
                application_id,
                None,
                organisation,
                job_title,
                "Application Deadline",
            ))
        # Events
        for application_id, event_id, organisation, job_title, event_type, title, event_date in get_upcoming_events():
            upcoming.append((
                event_date,
                application_id,
                event_id,
                organisation,
                f"{job_title} — {title}",
                event_type,
            ))
        # Sort by date (earliest first)
        upcoming.sort(key=lambda item: item[0])
        self.upcoming_table.setRowCount(0)
        for date, application_id, event_id, organisation, title, event_type in upcoming:
            row = self.upcoming_table.rowCount()
            self.upcoming_table.insertRow(row)
            values = [
                str(date),
                str(organisation),
                str(title),
                str(event_type),
                str(application_id),
            ]
            for column, value in enumerate(values):
                self.upcoming_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )
            self.upcoming_table.item(row, 0).setData(
                Qt.ItemDataRole.UserRole,
                {
                    "application_id": application_id,
                    "event_id": event_id,
                },
            )

        overdue = []
        # Application deadlines
        for application_id, organisation, job_title, deadline in get_overdue_applications():
            overdue.append((
                deadline,
                application_id,
                None,
                organisation,
                job_title,
                "Application Deadline",
            ))
        # Events
        for application_id, event_id, organisation, job_title, event_type, title, event_date in get_overdue_events():
            overdue.append((
                event_date,
                application_id,
                event_id,
                organisation,
                f"{job_title} — {title}",
                event_type,
            ))
        # Sort by date (earliest first)
        overdue.sort(key=lambda item: item[0], reverse=True)
        self.overdue_table.setRowCount(0)
        for date, application_id, event_id, organisation, title, event_type in overdue:
            row = self.overdue_table.rowCount()
            self.overdue_table.insertRow(row)
            values = [
                str(date),
                str(organisation),
                str(title),
                str(event_type),
                str(application_id),
            ]
            for column, value in enumerate(values):
                self.overdue_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                        )
            self.overdue_table.item(row, 0).setData(
                Qt.ItemDataRole.UserRole,
                {
                    "application_id": application_id,
                    "event_id": event_id,
                },
            )

    def separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator

    def create_event_table(self):
        # Create QTableWidget
        table = QTableWidget()
        # Configure columns
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Date",
            "Organisation",
            "Job Title / Event",
            "Type",
            "Application ID",
        ])
        # Behaviour
        table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        # Configure resize behaviour
        header = table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        header.resizeSection(0, 105)  # Date
        header.resizeSection(1, 160)  # Organisation
        header.resizeSection(3, 150)  # Type
        header.resizeSection(4, 105)  # Application ID
        # Return table
        return table

    def edit_clicked_item(self, table, row):
        date_item = table.item(row, 0)

        if date_item is None:
            return

        record = date_item.data(Qt.ItemDataRole.UserRole)

        if not record:
            return

        if record["event_id"] is not None:
            self.event_edit_requested.emit(record["event_id"])
        else:
            self.application_edit_requested.emit(
                record["application_id"]
            )