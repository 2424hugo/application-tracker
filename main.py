# main program to keep track of applications using database.py and models.py

from database import (
    create_database,
    add_application,
    get_applications,
    get_application,
    update_application,
    delete_application,
    number_of_applications,
)
from dashboard import display_dashboard
from datetime import date
from models import Application, ApplicationStatus

def main():
    create_database()
    display_dashboard()

    while True:
        print("\nApplication Tracker")
        print("1. Add application")
        print("2. View all applications")
        print("3. View application")
        print("4. Update application")
        print("5. Delete application")
        print("6. Exit")

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

            for application in applications:
                print(
                    f"[{application.id}] "
                    f"{application.organisation} — {application.job_title} "
                    f"({application.status.value})"
                )

        elif choice == "3":
            print(f"\nThere are {number_of_applications()} applications being tracked")
            ID_input = int(input("Enter ID number of application to view: "))
            application = get_application(ID_input)
            if application is None:
                print("Application not found.")
            else:
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
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()