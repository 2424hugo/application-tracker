# main program to keep track of applications using database.py and models.py

from database import (
    create_database,
    add_application,
    get_applications,
    get_application,
    update_application,
    delete_application,
    number_of_applications,
    get_events,
    get_event,
    add_event,
    update_event,
    delete_event,
)
from dashboard import display_dashboard
from datetime import date
from models import Application, ApplicationStatus, Event, EventType

def main():
    create_database()
    display_dashboard()

    while True:
        print("\nApplication Tracker")
        print("1.  Add application")
        print("2.  View all applications")
        print("3.  View application")
        print("4.  Update application")
        print("5.  Delete application")
        print("6.  Add event")
        print("7.  Complete event")
        print("8.  Update event")
        print("9.  Delete event")
        print("10. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            print("\nAdding new application....")
            organisation = input("Name of organisation: ")
            job_title = input("Job title: ")

            print("\nStatus options:")
            for status in ApplicationStatus:
                print(f"- {status.value}")
            status_input = input("Status: ")
            status = ApplicationStatus(status_input)

            salary_input = input("Salary (leave blank if unknown): ")
            salary = float(salary_input) if salary_input else None  

            deadline_input = input("Deadline (YYYY-MM-DD, leave blank if unknown): ")
            deadline = date.fromisoformat(deadline_input) if deadline_input else None

            location = input("Location: ")
            url = input("Job URL: ")
            notes = input("Notes: ")

            application = Application(
                organisation=organisation,
                job_title=job_title,
                status=status,
                salary=salary,
                deadline=deadline,
                location=location,
                url=url,
                notes=notes
            )

            application_id = add_application(application)
            print(f"Application added with ID {application_id}")

        elif choice == "2":
            print("\nGetting all applications...\n")

            applications = get_applications()

            if not applications:
                print("No applications found.")
            else:
                current_status = None

                for app in applications:
                    # Print a heading when the status changes
                    if app.status != current_status:
                        current_status = app.status
                        print(f"\n========== {app.status.value.upper()} ==========")

                    # Print the application
                    print(
                        f"[{app.id}] {app.organisation} — "
                        f"{app.job_title} ({app.status.value})"
                    )
                    print()

        elif choice == "3":
            print(f"\nThere are {number_of_applications()} applications being tracked")
            ID_input = int(input("Enter ID number of application to view: "))
            application = get_application(ID_input)
            if application is None:
                print("Application not found.")
            else:
                events = get_events(application.id)
                print("\nApplication details")
                print("-" * 40)
                print(f"ID:           {application.id}")
                print(f"Organisation: {application.organisation}")
                print(f"Job title:    {application.job_title}")
                print(f"Status:       {application.status.value}")
                print(f"Salary:       {application.salary if application.salary is not None else 'Unknown'}")
                print(f"Deadline:     {application.deadline if application.deadline else 'Unknown'}")
                print(f"Location:     {application.location or 'Unknown'}")
                print(f"URL:          {application.url or 'None'}")
                print(f"Notes:        {application.notes or 'None'}")
                print("-" * 40)
                print("\nEvents:")
                if not events:
                    print("No events recorded.")
                else:
                    for event in events:
                        completion = "Completed" if event.completed else "Pending"
                        print(
                            f"[{event.id}] {event.event_date:%d %b %Y} — "
                            f"{event.event_type.value}: {event.title} "
                            f"({completion})"
                        )
                        if event.notes:
                            print(f"    Notes: {event.notes}")

        elif choice == "4":
            print(f"\nThere are {number_of_applications()} applications being tracked")
            ID_input = int(input("Enter ID number of application to update: "))
            application = get_application(ID_input)
            if application is None:
                print("Application not found.")
            else:
                print("\nLeave a field blank to keep its current value.\n")

                organisation = input(
                    f"Organisation [{application.organisation}]: "
                ) or application.organisation

                job_title = input(
                    f"Job title [{application.job_title}]: "
                ) or application.job_title

                status_input = input(
                    f"Status [{application.status.value}]: "
                )

                if status_input:
                    status = ApplicationStatus(status_input)
                else:
                    status = application.status

                salary_input = input(
                    f"Salary [{application.salary or 'Unknown'}]: "
                )

                if salary_input:
                    salary = float(salary_input)
                else:
                    salary = application.salary

                deadline_input = input(
                    f"Deadline [{application.deadline or 'Unknown'}]: "
                )

                if deadline_input:
                    deadline = date.fromisoformat(deadline_input)
                else:
                    deadline = application.deadline

                location = input(
                    f"Location [{application.location}]: "
                ) or application.location

                url = input(
                    f"URL [{application.url}]: "
                ) or application.url

                notes = input(
                    f"Notes [{application.notes}]: "
                ) or application.notes

                updated_application = Application(
                    organisation=organisation,
                    job_title=job_title,
                    status=status,
                    salary=salary,
                    deadline=deadline,
                    location=location,
                    url=url,
                    notes=notes,
                    id=application.id
                )
                rows_updated = update_application(ID_input, updated_application)

                if rows_updated == 1:
                    print("Application updated successfully.")
                else:
                    print("Application could not be updated.")

        elif choice == "5":
            print(f"\nThere are {number_of_applications()} applications being tracked")
            ID_input = int(input("Enter ID number of application to delete: "))
            application = get_application(ID_input)
            if application is None:
                print("Application not found.")
            else:
                print("You have selected:\n")
                print(
                    f"[{application.id}] "
                    f"{application.organisation} — {application.job_title} "
                    f"({application.status.value})"
                )
                check = input("Are you sure you want to delete this application? (Y/n)")
                if check == "Y":
                    delete_application(ID_input)
                    print("Deleted application")
                else:
                    print("Application not deleted")

        elif choice == "6":
            application_id = int(input("Application ID: "))
            application = get_application(application_id)

            if application is None:
                print("Application not found.")
            else:
                print(f"\nAdding new event to {application.job_title}....")

                print("\nEvent type:")
                for event_type_option in EventType:
                    print(f"- {event_type_option.value}")
                event_type_input = input("Type: ")
                event_type = EventType(event_type_input)
    
                title = input("Event title: ")
    
                date_input = input("Date (YYYY-MM-DD): ")
                event_date = date.fromisoformat(date_input)

                notes = input("Notes: ")
    
                event = Event(
                    application_id=application_id,
                    event_type=event_type,
                    title=title,
                    event_date=event_date,
                    notes=notes,
                )
    
                event_id = add_event(event)
                print(f"Event added with ID {event_id} for {application.job_title} at {application.organisation}")
        
        elif choice == "7":
            event_id = int(input("Event ID: "))
            event = get_event(event_id)
            if event is None:
                print("Event not found.")
            else:
                event.completed = True
                rows_updated = update_event(event_id, event)

                if rows_updated == 1:
                    print(f"Event '{event.title}' marked as completed.")
                else:
                    print("Event could not be updated.")
        elif choice == "8":
            event_id = int(input("Enter ID number of event to update: "))
            event = get_event(event_id)

            if event is None:
                print("Event not found.")
            else:
                print("\nLeave a field blank to keep its current value.\n")

                print("Event types:")
                for event_type_option in EventType:
                    print(f"- {event_type_option.value}")

                event_type_input = input(
                    f"Type [{event.event_type.value}]: "
                ).strip()
                event_type = (
                    EventType(event_type_input)
                    if event_type_input else event.event_type
                )

                title = input(
                    f"Title [{event.title}]: "
                ).strip() or event.title

                date_input = input(
                    f"Date [{event.event_date}] (YYYY-MM-DD): "
                ).strip()
                event_date = (
                    date.fromisoformat(date_input)
                    if date_input else event.event_date
                )

                notes_input = input(
                    f"Notes [{event.notes or 'None'}] ('-' to clear): "
                ).strip()
                notes = (
                    "" if notes_input == "-"
                    else notes_input or event.notes
                )

                while True:
                    completed_input = input(
                        f"Completed [{'y' if event.completed else 'n'}] (y/n): "
                    ).strip().lower()

                    if completed_input in ("", "y", "n"):
                        completed = (
                            event.completed
                            if completed_input == ""
                            else completed_input == "y"
                        )
                        break

                    print("Enter y, n, or leave blank.")

                updated_event = Event(
                    application_id=event.application_id,
                    event_type=event_type,
                    title=title,
                    event_date=event_date,
                    notes=notes,
                    completed=completed,
                    id=event.id,
                )

                rows_updated = update_event(event_id, updated_event)

                if rows_updated == 1:
                    print("Event updated successfully.")
                else:
                    print("Event could not be updated.")
        elif choice == "9":
            event_id = int(input("Enter ID number of event to delete: "))
            event = get_event(event_id)

            if event is None:
                print("Event not found.")
            else:
                print("\nYou have selected:")
                print(
                    f"[{event.id}] {event.event_date:%d %b %Y} — "
                    f"{event.event_type.value}: {event.title}"
                )

                check = input(
                    "Are you sure you want to delete this event? (y/N): "
                ).strip().lower()

                if check == "y":
                    rows_deleted = delete_event(event_id)

                    if rows_deleted == 1:
                        print("Event deleted successfully.")
                    else:
                        print("Event could not be deleted.")
                else:
                    print("Event not deleted.")
        elif choice == "10":
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()