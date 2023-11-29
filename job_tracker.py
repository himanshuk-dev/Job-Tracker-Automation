import time

import gspread

from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.constants import Constants
from utils.helpers import get_springboard_credentials_from_env
from utils.type_aliases import SpringboardCredentials

springboard_credentials: SpringboardCredentials = get_springboard_credentials_from_env()


# Set up the driver
driver = webdriver.Chrome()

# Navigate to the login page
login_url: str = Constants.LOGIN_URL
driver.get(login_url)

# Find the email and password input elements and fill them in
email_elem = driver.find_element(By.CSS_SELECTOR, 'input[formControlName="login"]')
email_elem.send_keys(springboard_credentials.email)

password_elem = driver.find_element(
    By.CSS_SELECTOR, 'input[formControlName="password"]'
)
password_elem.send_keys(springboard_credentials.password)

# Submit the form
password_elem.send_keys(Keys.RETURN)

# Wait for login to complete - NOTE:edit this time to wait to enter verification capcha
time.sleep(25)

# Navigate to the job search page
job_search_url = "https://www.springboard.com/workshops/software-engineering-career-track/learn#/job-search/application"
driver.get(job_search_url)

try:
    print("Script started")

    jobs = []

    # While loop to navigate through multiple pages
    while True:
        # Use Selenium to get the page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        job_groups = soup.find_all("div", class_="info-group ng-star-inserted")

        for job_group in job_groups:
            job_title = job_group.find("div", class_="job-title").text.strip()
            company_name = (
                job_group.find("img", alt="company icon")
                .find_next_sibling()
                .text.strip()
            )
            location = (
                job_group.find("img", alt="location icon")
                .find_next_sibling()
                .text.strip()
            )
            last_updated = (
                job_group.find("img", alt="calendar icon")
                .find_next_sibling()
                .text.strip()
            )
            job_status_container = job_group.find("div", class_="status-container")
            job_status = job_status_container.find(
                "div", class_="status-item-active"
            ).text.strip()

            job = [job_title, company_name, location, last_updated, job_status]
            jobs.append(job)

        # Check if there's a 'Next' button and if it's not disabled
        next_button = driver.find_element(By.CSS_SELECTOR, ".pagination-next")
        if "disabled" in next_button.get_attribute("class"):
            break  # Exit the loop if 'Next' button is disabled

        # Click the 'Next' button to navigate to the next page
        next_button.click()
        time.sleep(5)  # Wait for the next page to load

        # Check if there's a 'Next' button and if it's not disabled
        next_button = driver.find_element(By.CSS_SELECTOR, ".pagination-next")
        if "disabled" in next_button.get_attribute("class"):
            break  # Exit the loop if 'Next' button is disabled

        # Click the 'Next' button to navigate to the next page
        next_button.click()
        time.sleep(5)  # Wait for the next page to load

    # Navigate to the contacts page
    contacts_url = "https://www.springboard.com/workshops/software-engineering-career-track/learn#/job-search/networking"
    driver.get(contacts_url)
    time.sleep(10)

    contacts = []

    # Start loop for pagination for contacts
    while True:
        # Use Selenium to get the page source
        contacts_page_source = driver.page_source
        contacts_soup = BeautifulSoup(contacts_page_source, "html.parser")

        # Get all contact elements
        contact_elements = contacts_soup.find_all(
            "div", class_="info-group ng-star-inserted"
        )

        for contact_element in contact_elements:
            # Extracting contact name
            contact_name_element = contact_element.find("a", class_="primary-anchor")
            contact_name = (
                contact_name_element.text.strip() if contact_name_element else ""
            )

            # Extracting role
            role_element = contact_element.find("span", class_="activity-role")
            role = role_element.text.strip() if role_element else ""

            # Extracting company
            company_element = contact_element.find("img", alt="company icon")
            company = company_element.next_sibling.strip() if company_element else ""

            # Extracting source (assuming it's "Outreach via LinkedIn" as per given HTML)
            source_element = contact_element.find("img", alt="networking type icon")
            source = source_element.next_sibling.strip() if source_element else ""

            # Extracting last updated date
            last_updated_element = contact_element.find("img", alt="calendar icon")
            last_updated = (
                last_updated_element.next_sibling.strip()
                if last_updated_element
                else ""
            )

            # Extracting next steps (assuming it's "next: informational interview" as per given HTML)
            next_steps_element = contact_element.find("div", class_="activity-desc")
            next_steps = next_steps_element.text.strip() if next_steps_element else ""

            contact = [contact_name, role, company, source, last_updated, next_steps]
            contacts.append(contact)

        # Check if there's a 'Next' button for contacts and if it's not disabled
        try:
            contacts_next_button = driver.find_element(
                By.CSS_SELECTOR, ".pagination-next"
            )
            if "disabled" in contacts_next_button.get_attribute("class"):
                break  # Exit the loop if 'Next' button is disabled

            # Click the 'Next' button to navigate to the next page for contacts
            contacts_next_button.click()
            time.sleep(5)  # Wait for the next page to load

        except Exception as e:
            print("Error with contacts pagination:", e)
            break  # Exit the loop if there's an error

    # Export to Google Sheets
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # For jobs
    sheet = client.open("Job-Tracker-Automated").worksheet("jobs")

    # Check if headers already exist or insert them
    headers = ["Job Title", "Company Name", "Location", "Last Updated", "Job Status"]
    existing_headers = sheet.row_values(1)

    if existing_headers != headers:
        sheet.insert_row(headers, 1)

    # Fetch all existing rows from the sheet
    existing_entries = sheet.get_all_values()[1:]  # Exclude headers

    job_title_index = headers.index("Job Title")
    company_name_index = headers.index("Company Name")
    job_status_index = headers.index("Job Status")

    for job in jobs:
        # Variables to check if job already exists and if status has changed
        job_exists = False
        status_changed = False

        # Extract the job details for easier comparison
        job_title, company_name, _, _, job_status = job

        for index, entry in enumerate(existing_entries):
            # Check if job title and company name match
            if (
                entry[job_title_index] == job_title
                and entry[company_name_index] == company_name
            ):
                job_exists = True

                # Check if the job status has changed
                if entry[job_status_index] != job_status:
                    status_changed = True
                    row_to_update = (
                        index + 2
                    )  # +1 for zero-based index, +1 for header row

                break

        if job_exists:
            if status_changed:
                # Update the status in the Google Sheet
                sheet.update_cell(row_to_update, job_status_index + 1, job_status)
        else:
            # Append the new job to the Google Sheet
            sheet.append_row(job)
    print("Jobs added to Google Sheets")

    # For Contacts
    contacts_sheet = client.open("Job-Tracker-Automated").worksheet("contacts")

    # Headers for the contacts sheet
    contact_headers = [
        "Contact Name",
        "Role",
        "Company",
        "Source",
        "Last Updated",
        "Next Steps",
    ]
    existing_contact_headers = contacts_sheet.row_values(1)

    if existing_contact_headers != contact_headers:
        contacts_sheet.insert_row(contact_headers, 1)

    # Fetch all existing rows from the contacts sheet
    existing_contact_entries = contacts_sheet.get_all_values()[1:]  # Exclude headers

    contact_name_index = contact_headers.index("Contact Name")
    role_index = contact_headers.index("Role")
    company_index = contact_headers.index("Company")
    source_index = contact_headers.index("Source")

    for contact in contacts:
        # Variable to track the position of the existing contact
        existing_contact_position = -1

        # Extract the contact details for easier comparison
        contact_name, _, _, source, _, _ = contact

        for index, entry in enumerate(existing_contact_entries):
            # Check if contact name matches
            if entry[contact_name_index] == contact_name:
                existing_contact_position = index
                break

        if existing_contact_position != -1:  # Contact exists
            # Compare the sources
            if entry[source_index] != source:
                # Update the source in the Google Sheet
                contacts_sheet.update_cell(
                    existing_contact_position + 1, source_index + 1, source
                )  # +1 to adjust for 0-based index
        else:
            # Append the new contact to the Google Sheet
            contacts_sheet.append_row(contact)

    print("Contacts added to Google Sheets")

    print("Script ended")
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback

    print(traceback.format_exc())


# Close the driver
driver.quit()
