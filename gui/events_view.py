from collections import defaultdict

from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtGui import QFont, QPalette
from PySide6.QtWidgets import (
    QCalendarWidget,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database import get_calendar_items

class EventsCalendar(QCalendarWidget):
    def __init__(self):
        self.item_counts = {}
        super().__init__()

        self.setGridVisible(True)
        self.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        self.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.setMinimumHeight(350)

    def set_item_counts(self, counts):
        self.item_counts = counts
        self.updateCells()

    def paintCell(self, painter, rect, calendar_date):
        super().paintCell(painter, rect, calendar_date)

        count = self.item_counts.get(
            calendar_date.toString("yyyy-MM-dd"), 0
        )

        if not count:
            return

        painter.save()

        # Match the text colour to the selected/unselected cell.
        role = (
            QPalette.ColorRole.HighlightedText
            if calendar_date == self.selectedDate()
            else QPalette.ColorRole.Text
        )
        painter.setPen(self.palette().color(role))

        font = painter.font()
        font.setPointSize(8)
        font.setBold(True)
        painter.setFont(font)

        label = "1 due" if count == 1 else f"{count} due"

        # Draw below the date number.
        painter.drawText(
            rect.adjusted(3, 0, -3, -3),
            Qt.AlignmentFlag.AlignHCenter
            | Qt.AlignmentFlag.AlignBottom,
            label,
        )

        painter.restore()

class EventsView(QWidget):
    application_edit_requested = Signal(int)
    event_edit_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.items_by_date = defaultdict(list)
        layout = QVBoxLayout(self)

        # Heading and controls
        heading = QLabel("EVENTS")
        heading.setFont(QFont("", 12, QFont.Weight.Bold))

        today_button = QPushButton("Today")
        today_button.clicked.connect(self.select_today)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh)

        controls = QHBoxLayout()
        controls.addWidget(heading)
        controls.addStretch()
        controls.addWidget(today_button)
        controls.addWidget(refresh_button)
        layout.addLayout(controls)

        # Calendar
        self.calendar = EventsCalendar()
        self.calendar.selectionChanged.connect(
            self.show_selected_date
        )
        layout.addWidget(self.calendar, stretch=3)

        # Details for the selected day
        self.date_heading = QLabel()
        self.date_heading.setFont(
            QFont("", 11, QFont.Weight.Bold)
        )
        layout.addWidget(self.date_heading)

        self.details_list = QListWidget()
        self.details_list.setWordWrap(True)
        self.details_list.itemDoubleClicked.connect(
            self.edit_clicked_item
        )
        layout.addWidget(self.details_list, stretch=1)

        self.refresh()

    def refresh(self):
        self.items_by_date.clear()

        for item in get_calendar_items():
            self.items_by_date[item["due_date"]].append(item)

        counts = {
            due_date: len(items)
            for due_date, items in self.items_by_date.items()
        }

        self.calendar.set_item_counts(counts)
        self.show_selected_date()

    def show_selected_date(self):
        selected_date = self.calendar.selectedDate()
        date_key = selected_date.toString("yyyy-MM-dd")

        self.date_heading.setText(
            selected_date.toString("dddd d MMMM yyyy")
        )
        self.details_list.clear()

        items = self.items_by_date.get(date_key, [])

        if not items:
            self.details_list.addItem(
                "No deadlines or pending events for this day."
            )
            return

        for item in items:
            list_item = QListWidgetItem(
                f"{item['item_type']} — {item['title']}\n"
                f"{item['organisation']} — {item['job_title']}"
            )

            list_item.setData(
                Qt.ItemDataRole.UserRole,
                {
                    "application_id": item["application_id"],
                    "event_id": item["event_id"],
                },
            )

            self.details_list.addItem(list_item)

    def select_today(self):
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.showSelectedDate()

    def showEvent(self, event):
        super().showEvent(event)
        # Reload whenever the user opens this page.
        self.refresh()

    def edit_clicked_item(self, item):
        record = item.data(Qt.ItemDataRole.UserRole)

        # The "No deadlines..." message has no attached record.
        if not record:
            return

        if record["event_id"] is not None:
            self.event_edit_requested.emit(record["event_id"])
        else:
            self.application_edit_requested.emit(
                record["application_id"]
            )