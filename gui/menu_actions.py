from dataclasses import replace
from math import isfinite

from PySide6.QtCore import QDate, QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDateEdit, QDialog, QDialogButtonBox,
    QFormLayout, QInputDialog, QLineEdit, QMessageBox,
    QPlainTextEdit, QVBoxLayout,
)

import database as db
from models import Application, ApplicationStatus, Event, EventType


def date_edit(value=None):
    widget = QDateEdit()
    widget.setCalendarPopup(True)
    widget.setDisplayFormat("dd/MM/yyyy")
    widget.setDateRange(QDate(1900, 1, 1), QDate(9999, 12, 31))
    widget.setDate(QDate(value.year, value.month, value.day)
                   if value else QDate.currentDate())
    return widget


class RecordDialog(QDialog):
    def __init__(self, title, parent):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(520, 420)
        self.result_record = None
        layout = QVBoxLayout(self)
        self.form = QFormLayout()
        layout.addLayout(self.form)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        try:
            self.result_record = self.build_record()
        except ValueError as error:
            QMessageBox.warning(self, "Check your entries", str(error))
            return
        super().accept()


class ApplicationDialog(RecordDialog):
    def __init__(self, parent, application=None):
        super().__init__(
            "Update application" if application else "Add application", parent
        )
        self.original = application
        self.organisation = QLineEdit()
        self.job_title = QLineEdit()
        self.status = QComboBox()
        self.status.addItems([status.value for status in ApplicationStatus])
        self.salary = QLineEdit()
        self.salary.setPlaceholderText("Optional, e.g. 32000")
        self.has_deadline = QCheckBox("Application has a deadline")
        self.deadline = date_edit(application.deadline if application else None)
        self.deadline.setEnabled(False)
        self.has_deadline.toggled.connect(self.deadline.setEnabled)
        self.location = QLineEdit()
        self.url = QLineEdit()
        self.notes = QPlainTextEdit()

        for label, widget in (
            ("Organisation *", self.organisation),
            ("Job title *", self.job_title),
            ("Status", self.status),
            ("Salary (£)", self.salary),
            ("", self.has_deadline),
            ("Deadline", self.deadline),
            ("Location", self.location),
            ("Job URL", self.url),
            ("Notes", self.notes),
        ):
            self.form.addRow(label, widget)

        if application:
            self.organisation.setText(application.organisation)
            self.job_title.setText(application.job_title)
            self.status.setCurrentText(application.status.value)
            self.salary.setText(
                str(application.salary) if application.salary is not None else ""
            )
            self.has_deadline.setChecked(application.deadline is not None)
            self.location.setText(application.location or "")
            self.url.setText(application.url or "")
            self.notes.setPlainText(application.notes or "")

    def build_record(self):
        organisation = self.organisation.text().strip()
        job_title = self.job_title.text().strip()
        if not organisation or not job_title:
            raise ValueError("Enter an organisation and job title.")

        salary_text = self.salary.text().strip()
        salary = None
        if salary_text:
            try:
                salary = float(salary_text)
            except ValueError:
                raise ValueError("Enter salary as a number, without £ or commas.")
            if not isfinite(salary) or salary < 0:
                raise ValueError("Salary must be a finite, non-negative number.")

        values = dict(
            organisation=organisation,
            job_title=job_title,
            status=ApplicationStatus(self.status.currentText()),
            salary=salary,
            deadline=(self.deadline.date().toPython()
                      if self.has_deadline.isChecked() else None),
            location=self.location.text().strip(),
            url=self.url.text().strip(),
            notes=self.notes.toPlainText(),
        )
        # Keep the original ID and creation date when editing.
        return (replace(self.original, **values) if self.original
                else Application(**values))


class EventDialog(RecordDialog):
    def __init__(self, parent, application, event=None):
        super().__init__("Update event" if event else "Add event", parent)
        self.application_id = application.id
        self.original = event
        self.setWindowTitle(
            f"{self.windowTitle()} — {application.organisation}"
        )
        self.event_type = QComboBox()
        self.event_type.addItems([kind.value for kind in EventType])
        self.title = QLineEdit()
        self.event_date = date_edit(event.event_date if event else None)
        self.notes = QPlainTextEdit()
        self.completed = QCheckBox("Completed")

        self.form.addRow("Application", QLineEdit(
            f"{application.organisation} — {application.job_title}"
        ))
        application_field = self.form.itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
        application_field.setReadOnly(True)
        self.form.addRow("Type", self.event_type)
        self.form.addRow("Title *", self.title)
        self.form.addRow("Date", self.event_date)
        self.form.addRow("Notes", self.notes)
        self.form.addRow("", self.completed)

        if event:
            self.event_type.setCurrentText(event.event_type.value)
            self.title.setText(event.title)
            self.notes.setPlainText(event.notes or "")
            self.completed.setChecked(event.completed)

    def build_record(self):
        title = self.title.text().strip()
        if not title:
            raise ValueError("Enter an event title.")
        values = dict(
            application_id=self.application_id,
            event_type=EventType(self.event_type.currentText()),
            title=title,
            event_date=self.event_date.date().toPython(),
            notes=self.notes.toPlainText(),
            completed=self.completed.isChecked(),
        )
        return (replace(self.original, **values) if self.original
                else Event(**values))


class MenuActions(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        applications_menu = window.menuBar().addMenu("&Applications")
        events_menu = window.menuBar().addMenu("&Events")
        for menu, title, handler in (
            (applications_menu, "Add application…", self.add_application),
            (applications_menu, "Update application…", self.update_application),
            (applications_menu, "Delete application…", self.delete_application),
            (events_menu, "Add event…", self.add_event),
            (events_menu, "Complete event…", self.complete_event),
            (events_menu, "Update event…", self.update_event),
            (events_menu, "Delete event…", self.delete_event),
        ):
            action = QAction(title, window)
            action.triggered.connect(
                lambda checked=False, callback=handler: self.run(callback)
            )
            menu.addAction(action)

    def run(self, callback):
        try:
            changed = callback()
        except Exception as error:
            QMessageBox.critical(self.window, "Action failed", str(error))
            return
        if changed:
            try:
                for index in range(self.window.pages.count()):
                    page = self.window.pages.widget(index)
                    refresh = getattr(page, "refresh", None)
                    if callable(refresh):
                        refresh()
                self.window.statusBar().showMessage("Changes saved.", 5000)
            except Exception as error:
                QMessageBox.warning(
                    self.window, "Saved; refresh failed",
                    f"Your change was saved. Reopen the page to reload it.\n\n{error}",
                )

    def choose(self, title, records, label):
        if not records:
            QMessageBox.information(self.window, title, "No matching records.")
            return None
        labels = [label(record) for record in records]
        selected, accepted = QInputDialog.getItem(
            self.window, title, "Select a record:", labels, 0, False
        )
        return records[labels.index(selected)] if accepted else None

    def choose_application(self):
        return self.choose(
            "Select application", db.get_applications(),
            lambda app: f"[{app.id}] {app.organisation} — {app.job_title}",
        )

    def choose_event(self, pending_only=False):
        application = self.choose_application()
        if application is None:
            return None, None
        events = db.get_events(application.id)
        if pending_only:
            events = [event for event in events if not event.completed]
        event = self.choose(
            "Select event", events,
            lambda event: (
                f"[{event.id}] {event.event_date:%d/%m/%Y} — {event.title}"
                f" ({'Completed' if event.completed else 'Pending'})"
            ),
        )
        return application, event

    def confirm(self, title, message):
        return QMessageBox.question(
            self.window, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) == QMessageBox.StandardButton.Yes

    def save_dialog(self, dialog, save):
        while dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                result = save(dialog.result_record)
                if not result:
                    raise ValueError("The record no longer exists. Reload and try again.")
            except Exception as error:
                QMessageBox.critical(dialog, "Could not save", str(error))
                continue
            return True
        return False

    def add_application(self):
        return self.save_dialog(ApplicationDialog(self.window), db.add_application)

    def update_application(self):
        application = self.choose_application()

        if application is not None:
            return self.edit_application(application.id)

    def edit_application(self, application_id):
        application = db.get_application(application_id)

        if application is None:
            raise ValueError(
                "This application no longer exists. Refresh the page."
            )

        return self.save_dialog(
            ApplicationDialog(self.window, application),
            lambda updated: db.update_application(
                application.id, updated
            ),
        )
    
    def open_application_editor(self, application_id):
        self.run(lambda: self.edit_application(application_id))

    def delete_application(self):
        application = self.choose_application()
        if application is None:
            return False
        count = len(db.get_events(application.id))
        if self.confirm(
            "Delete application",
            f"Delete {application.organisation} — {application.job_title}?\n\n"
            f"This will also delete its {count} linked event(s).",
        ):
            return bool(db.delete_application(application.id))
        return False

    def add_event(self):
        application = self.choose_application()
        if application is not None:
            return self.save_dialog(
                EventDialog(self.window, application), db.add_event
            )

    def complete_event(self):
        application, event = self.choose_event(pending_only=True)
        if event is not None and self.confirm(
            "Complete event",
            f"Mark '{event.title}' for {application.organisation} as completed?",
        ):
            return bool(db.update_event(event.id, replace(event, completed=True)))
        return False

    def update_event(self):
        application, event = self.choose_event()

        if event is not None:
            return self.edit_event(event.id)

    def open_event_editor(self, event_id):
        self.run(lambda: self.edit_event(event_id))

    def edit_event(self, event_id):
        event = db.get_event(event_id)

        if event is None:
            raise ValueError(
                "This event no longer exists. Refresh the page."
            )

        application = db.get_application(event.application_id)

        if application is None:
            raise ValueError(
                "The event's application no longer exists."
            )

        return self.save_dialog(
            EventDialog(self.window, application, event),
            lambda updated: db.update_event(event.id, updated),
        )

    def delete_event(self):
        application, event = self.choose_event()
        if event is not None and self.confirm(
            "Delete event",
            f"Delete '{event.title}' for {application.organisation}?",
        ):
            return bool(db.delete_event(event.id))
        return False
