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

class EventType(Enum):
    ONLINE_ASSESSMENT = "Online Assessment"
    INTERVIEW = "Interview"
    FOLLOW_UP = "Follow-up"
    EMAIL = "Email"
    OTHER = "Other"

@dataclass
class Event:
    application_id: int
    event_type: EventType
    title: str
    event_date: date
    notes: str = ""
    completed: bool = False
    id: int | None = None

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