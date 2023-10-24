# Job Tracker Automation

Automation tool to export jobs saved on Springboard Job Tracker to Google Sheets.
![Job-Tracker-Automation](https://github.com/coderhimanshu1/Job-Tracker-Automation/assets/87880250/565f4ce7-c17b-4dd3-bf49-8b9521899e92)

## Demo

https://github.com/coderhimanshu1/Job-Tracker-Automation/assets/87880250/4928509e-ab3f-4d74-90d6-4686b9956ae7


## Description

The `job_tracker.py` script uses Selenium to log into the Springboard platform and scrape job application details. The details are then stored in a Google Sheet, providing an organized view of your job applications.

## Features

- Automated login to Springboard
- Scraping of job details including:
  - Job Title
  - Company Name
  - Location
  - Last Updated
  - Job Status
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

5. Set up your .env file with your Springboard credentials:

```
SPRINGBOARD_EMAIL=your_email@example.com
SPRINGBOARD_PASSWORD=your_password
```

### Usage

Run the script:
`python job_tracker.py`

_After execution, you'll find the scraped job details in the "Job-Tracker-Automated" Google Sheet._

### Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License

MIT

### Disclaimer

Use this tool responsibly and ensure you have permission to scrape and automate tasks on the platforms you are interacting with.
