# Program that creates the Application class which stores the information of each application
#
# Contains classes:
# Appliction -> Stores individal application information
# ApplicationStatus -> The statues a appliction can be

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum

class ApplicationStatus(Enum):
    INTERESTED = "Interested"
    APPLIED = "Applied"
    ONLINE_ASSESSMENT = "Online Assessment"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"

# Too be added later, a flexible event that can be added to an application
"""
class Event:
    id
    application_id
    event_type
    title
    due_date
    completed
"""
    

@dataclass
class Application:
    organisation: str
    job_title: str
    status: ApplicationStatus
    salary: float | None
    deadline: date | None
    location: str
    url: str
    notes: str
    created_at: datetime = field(default_factory=datetime.now)
    id: int | None = None