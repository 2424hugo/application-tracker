# Program that creates the Application class which stores the information of each application
#
# Contains classes:
# Appliction -> Stores individal application information
# ApplicationStatus -> The statues a appliction can be

from dataclasses import dataclass
from datetime import date
from enum import Enum

class ApplicationStatus(Enum):
    INTERESTED = "Interested"
    PREPARING = "Preparing"
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    REJECTED = "Rejected"
    OFFER = "Offer"

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
    id: int | None = None