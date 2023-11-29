# Job Tracker Automation

An automation tool to export jobs and contacts saved on Springboard Job Tracker to Google Sheets.
![Job-Tracker-Automation](https://github.com/coderhimanshu1/Job-Tracker-Automation/assets/87880250/565f4ce7-c17b-4dd3-bf49-8b9521899e92)

## Demo

https://github.com/coderhimanshu1/Job-Tracker-Automation/assets/87880250/57404966-238d-4c24-ac21-e82fd8c3143b

## Description

The `job_tracker.py` script uses Selenium to log into the Springboard platform and scrape job applications and contact details. These details are then stored in a Google Sheet, providing an organized view of your job applications and professional contacts.

## Features

- Automated login to Springboard
  - _Note: There can be cases where you are required to enter a security captcha if you end up running the script multiple times. So please ensure to follow all the steps before running the script._
- Scraping of job details including:
  - Job Title
  - Company Name
  - Location
  - Last Updated
  - Job Status
- Scraping of contact details including:
  - Contact Name
  - Role
  - Company
  - Last Updated
  - Next steps (description)
- Export job details to Google Sheets

## Setup & Installation

### Prerequisites

1. Python 3.x
2. Google Sheets API credentials (`credentials.json`)
3. Chrome WebDriver for Selenium
4. `.env` file with your Springboard credentials (`SPRINGBOARD_EMAIL` and `SPRINGBOARD_PASSWORD`)

### Steps:

1. Clone the repository:

   ```
   git clone git@github.com:coderhimanshu1/Job-Tracker.git
   cd Job-Tracker-Automation
   ```

2. Install required Python packages:

`pip install selenium gspread oauth2client python-dotenv BeautifulSoup4`

3. Make sure you have set up your Google Sheets API permissions [Steps Here](https://developers.google.com/sheets/api/quickstart/python).

4. Create a Google Sheet and name it "Job-Tracker-Automated".

5. MAke sure two have two worksheets named: "jobs" and "contacts".

6. Set up your .env file with your Springboard credentials:

```
SPRINGBOARD_EMAIL=your_email@example.com
SPRINGBOARD_PASSWORD=your_password
```

See a comprehensive setup guide [HERE](setup_guide.md).

### Usage

Run the script:
`python job_tracker.py`

_After execution, you'll find the scraped job details in the "Job-Tracker-Automated" Google Sheet._

## Development

See [`.github/CONTRIBUTING.md`](./.github/CONTRIBUTING.md), then [`.github/DEVELOPMENT.md`](./.github/DEVELOPMENT.md).
Thanks!

### License

MIT

### Disclaimer

This tool is specifically designed for Springboard students to aid in managing their job search and networking endeavors. Use this tool responsibly and ensure you have permission to scrape and automate tasks on the platforms you are interacting with. Unauthorized or improper use of this tool outside the context of Springboard may violate terms of service or user agreements. Always adhere to the platform's terms and conditions.
