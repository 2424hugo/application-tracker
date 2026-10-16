from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QLabel, 
    QTableWidget,
    QHeaderView,
    QAbstractItemView,
    QTableWidgetItem,
    QLineEdit,
    QComboBox,
)
from models import ApplicationStatus
from PySide6.QtGui import QFont
from database import (
    get_applications,
)

class ApplicationsView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout
        application_layout = QVBoxLayout()

        # founts
        heading_font = QFont()
        heading_font.setPointSize(12)
        heading_font.setBold(True)

        # Heading
        application_heading = QLabel("APPLICATIONS")
        application_heading.setFont(heading_font)
        application_layout.addWidget(application_heading)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search organisation or job title...")
        self.search_bar.textChanged.connect(self.filter_applications)
        application_layout.addWidget(self.search_bar)

        # Status Dropdown
        self.status_filter = QComboBox()
        self.status_filter.addItem("All statuses")
        for status in ApplicationStatus:
            self.status_filter.addItem(status.value)
            # Connect dropdown to filtering method
        self.status_filter.currentTextChanged.connect(
            lambda _: self.filter_applications(self.search_bar.text())
        )
        application_layout.addWidget(self.status_filter)
        

        # Table
        self.application_table = self.create_application_table()
        application_layout.addWidget(self.application_table)

        self.setLayout(application_layout)
        self.refresh()

    def refresh(self):
        applications = get_applications()

        self.application_table.setRowCount(0)
        for application in applications:
            row = self.application_table.rowCount()
            self.application_table.insertRow(row)
            values = [
                application.id,
                application.organisation,
                application.job_title,
                application.status.value,
                str(application.deadline) if application.deadline else "",
                application.location or "",
            ]
            for column, value in enumerate(values):
                self.application_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value))
                )
        self.filter_applications(self.search_bar.text())

    def create_application_table(self):
        # Create QTableWidget
        table = QTableWidget()
        # Configure columns
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "ID",
            "Organisation",
            "Job Title",
            "Status",
            "Deadline",
            "Location",
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
        # Return table
        return table


    def filter_applications(self, search_text):
        search_text = search_text.lower()
        selected_status = self.status_filter.currentText()

        for row in range(self.application_table.rowCount()):
            # Retrieve organisation from column 1
            organisation = self.application_table.item(row, 1).text().lower()

            # Retrieve job title from column 2
            job_title = self.application_table.item(row, 2).text().lower()

            # Retrieve the application's status
            application_status = self.application_table.item(row, 3).text()

            # Check whether either field contains the search text
            search_matches = search_text in organisation or search_text in job_title
            status_matches = (
                selected_status == "All statuses"
                or application_status == selected_status
            )

            # Hide rows that do not match
            matches = search_matches and status_matches
            self.application_table.setRowHidden(row, not matches)
