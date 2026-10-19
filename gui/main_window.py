from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    )
from PySide6.QtGui import QFont

from .dashboard_view import DashboardView
from .applications_view import ApplicationsView
from .events_view import EventsView
from .menu_actions import MenuActions

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application Tracker")
        self.resize(1100, 700)
        self.pages = QStackedWidget()

        # main layout for the window
        main_layout = QHBoxLayout()

        # sidebar to select dashboard, applications, events
        sidebar_layout = QVBoxLayout()

        dashboard_button = QPushButton("Dashboard")
        sidebar_layout.addWidget(dashboard_button)

        applications_button = QPushButton("Applications")
        sidebar_layout.addWidget(applications_button)

        events_button = QPushButton("Events")
        sidebar_layout.addWidget(events_button)

        sidebar_layout.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)

        # content layout that contains title and dashboard labels
        content_layout = QVBoxLayout()

        # Dashboard page
        dashboard_page = DashboardView()

        # Applications page
        applications_page = ApplicationsView()

        # Events page
        events_page = EventsView()

        # Set buttons
        dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )
        applications_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )
        events_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )


        # add pages to self.pages
        self.pages.addWidget(dashboard_page)
        self.pages.addWidget(applications_page)
        self.pages.addWidget(events_page)

        # Place the stacked pages inside the content widget
        content_layout.addWidget(self.pages)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        # Adding content_widget and sidebar_widget to main_layout
        main_layout.addWidget(sidebar_widget, stretch=1)
        main_layout.addWidget(content_widget, stretch=4)

        # centrel widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        
        self.setCentralWidget(central_widget)
        self.menu_actions = MenuActions(self)



if __name__ == '__main__':
    print()