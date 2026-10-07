from database import (
    count_applications_this_week,
    get_pipeline_counts,
    get_upcoming_applications,
    get_upcoming_events,
)

from datetime import date
from models import ApplicationStatus

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
    upcoming = []

    for application_id, organisation, job_title, deadline in get_upcoming_applications():
        upcoming.append(
            (deadline, application_id, None,
            organisation, job_title, "Application Deadline")
        )

    for application_id, event_id, organisation, job_title, event_type, title, event_date in get_upcoming_events():
        upcoming.append(
            (event_date, application_id, event_id,
            organisation, job_title, f"{event_type}: {title}")
        )

    upcoming.sort(key=lambda item: item[0])
    upcoming = upcoming[:6]

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

    for activity_date, application_id, event_id, organisation, job_title, activity in upcoming:
        date_value = date.fromisoformat(activity_date)

        ids = f"App ID: {application_id}"
        if event_id is not None:
            ids += f" | Event ID: {event_id}"

        print(
            f"{date_value:%d %b}  [{ids}] "
            f"{organisation} — {job_title}\n"
            f"        {activity}"
        )
        
    print()

def main():
    display_dashboard()


if __name__ == "__main__":
    main()