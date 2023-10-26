from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

load_dotenv()

email = os.getenv('SPRINGBOARD_EMAIL')
password = os.getenv('SPRINGBOARD_PASSWORD')



# Set up the driver
driver = webdriver.Chrome()

# Navigate to the login page
login_url = "https://www.springboard.com/login/?next=%2Fworkshops%2Fsoftware-engineering-career-track%2Flearn%23%2Fjob-search%2Fapplication"
driver.get(login_url)

# Find the email and password input elements and fill them in
email_elem = driver.find_element(By.CSS_SELECTOR, 'input[formControlName="login"]')
email_elem.send_keys(email)

password_elem = driver.find_element(By.CSS_SELECTOR, 'input[formControlName="password"]')
password_elem.send_keys(password)

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
        soup = BeautifulSoup(page_source, 'html.parser')

        job_groups = soup.find_all('div', class_='info-group ng-star-inserted')

        for job_group in job_groups:
            job_title = job_group.find('div', class_='job-title').text.strip()
            company_name = job_group.find('img', alt='company icon').find_next_sibling().text.strip()
            location = job_group.find('img', alt='location icon').find_next_sibling().text.strip()
            last_updated = job_group.find('img', alt='calendar icon').find_next_sibling().text.strip()
            job_status_container = job_group.find('div', class_='status-container')
            job_status = job_status_container.find('div', class_='status-item-active').text.strip()

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

    time.sleep(5)

    contacts = []
    
    # Start loop for pagination for contacts
    while True:
        # Use Selenium to get the page source
        contacts_page_source = driver.page_source
        contacts_soup = BeautifulSoup(contacts_page_source, 'html.parser')

        # Get all contact elements
        contact_elements = contacts_soup.find_all('div', class_='networking-activity-item')

        for contact_element in contact_elements:
            contact_name = contact_element.find('a', class_='contact-name-link').text.strip()
            role = contact_element.find('span', class_='activity-role').text.strip()
            company = contact_element.find('img', class_='company-icon-image').find_next_sibling().text.strip()
            calendar_icon_elem = contact_element.find('img', alt='calendar icon')
            if calendar_icon_elem:
                source = calendar_icon_elem.find_next_sibling(text=True).strip()
            last_updated = contact_element.find('img', alt='calendar icon').find_next_sibling().text.strip()
            next_steps = contact_element.find('div', class_='activity-desc').text.strip()

            contact = [contact_name, role, company, source, last_updated, next_steps]
            contacts.append(contact)

        # Check if there's a 'Next' button for contacts and if it's not disabled
        try:
            contacts_next_button = driver.find_element(By.CSS_SELECTOR, ".pagination-next")
            if "disabled" in contacts_next_button.get_attribute("class"):
                break  # Exit the loop if 'Next' button is disabled

            # Click the 'Next' button to navigate to the next page for contacts
            contacts_next_button.click()
            time.sleep(5)  # Wait for the next page to load

        except Exception as e:
            print("Error with contacts pagination:", e)
            break  # Exit the loop if there's an error

    # Export to Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
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

    job_title_index = headers.index('Job Title')
    company_name_index = headers.index('Company Name')
    job_status_index = headers.index('Job Status')

    for job in jobs:
        # Variables to check if job already exists and if status has changed
        job_exists = False
        status_changed = False
        
        # Extract the job details for easier comparison
        job_title, company_name, _, _, job_status = job

        for index, entry in enumerate(existing_entries):
            # Check if job title and company name match
            if entry[job_title_index] == job_title and entry[company_name_index] == company_name:
                job_exists = True

                # Check if the job status has changed
                if entry[job_status_index] != job_status:
                    status_changed = True
                    row_to_update = index + 2  # +1 for zero-based index, +1 for header row

                break

        if job_exists:
            if status_changed:
                # Update the status in the Google Sheet
                sheet.update_cell(row_to_update, job_status_index + 1, job_status)
        else:
            # Append the new job to the Google Sheet
            sheet.append_row(job)
            print("Script ended")
        
        # For Contacts
        contacts_sheet = client.open("Job-Tracker-Automated").worksheet("contacts")

        # Headers for the contacts sheet
        contact_headers = ["Contact Name", "Role", "Company", "Source", "Last Updated", "Next Steps"]
        existing_contact_headers = contacts_sheet.row_values(1)
        
        if existing_contact_headers != contact_headers:
            contacts_sheet.insert_row(contact_headers, 1)

        # Fetch all existing rows from the contacts sheet
        existing_contact_entries = contacts_sheet.get_all_values()[1:]  # Exclude headers

        contact_name_index = contact_headers.index('Contact Name')
        role_index = contact_headers.index('Role')
        company_index = contact_headers.index('Company')

        for contact in contacts:
            # Variables to check if contact already exists
            contact_exists = False
            
            # Extract the contact details for easier comparison
            contact_name, role, company, _, _, _ = contact

            for index, entry in enumerate(existing_contact_entries):
                # Check if contact name, role, and company match
                if entry[contact_name_index] == contact_name and entry[role_index] == role and entry[company_index] == company:
                    contact_exists = True
                    break

            if not contact_exists:
                # Append the new contact to the Google Sheet
                contacts_sheet.append_row(contact)

    print("Contacts added to Google Sheets")
    

except Exception as e:
    print("Error:", e)

# Close the driver
driver.quit()