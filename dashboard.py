from database import (
    count_applications_this_week,
    get_pipeline_counts,
    get_upcoming_applications,
)

from datetime import date
from models import Application, ApplicationStatus

def count_active_applications(pipeline):
    active_statuses = (
        ApplicationStatus.INTERESTED,
        ApplicationStatus.APPLIED,
        ApplicationStatus.ONLINE_ASSESSMENT,
        ApplicationStatus.INTERVIEW,
        ApplicationStatus.OFFER,
    )

    return sum(
        pipeline.get(status.value, 0)
        for status in active_statuses
    )

def display_dashboard():
    pipeline = get_pipeline_counts()
    active = count_active_applications(pipeline)
    this_week = count_applications_this_week()
    upcoming = get_upcoming_applications()

    print()
    print("APPLICATION TRACKER")
    print("─" * 55)
    print()

    print(f"Active applications:     {active}")
    print(f"Applications this week:  {this_week}")
    print()

    print("PIPELINE")
    print("─" * 55)

    for status in ApplicationStatus:
        count = pipeline.get(status.value, 0)
        bar = "█" * count

        print(f"{status.value:<20} {count:>3}  {bar}")

    print()

    print("UPCOMING")
    print("─" * 55)

    for organisation, job_title, deadline in upcoming:
        deadline_date = date.fromisoformat(deadline)

        print(
            f"{deadline_date.strftime('%d %b')}  "
            f"{organisation:<20} "
            f"{job_title}"
        )

    print()

def main():
    display_dashboard()


if __name__ == "__main__":
    main()