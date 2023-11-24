# Job Tracker Automation: Setup Guide

This guide provides step-by-step instructions to set up the Job Tracker Automation tool, which exports jobs and contacts from Springboard Job Tracker to Google Sheets.

## Prerequisites

Before you begin, make sure you have the following prerequisites:

- **Python 3.x:** Ensure Python 3.x is installed on your system. Get Python [here](https://www.python.org/downloads/).

- **Google Sheets API Credentials:**

    To get your Google Sheets API credentials follow the instructions in this beautifully crafted [article](https://medium.com/@a.marenkov/how-to-get-credentials-for-google-sheets-456b7e88c430) by [Alexander Marenkov](https://medium.com/@a.marenkov).

- **Chrome WebDriver for Selenium:**
  - Download and install Chrome WebDriver from [official site](https://sites.google.com/chromium.org/driver/). You can also directly install from here [too](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/).

- **.env file:**
  - Create a `.env` file with your Springboard credentials:

    ```env
    SPRINGBOARD_EMAIL=your_email@example.com
    SPRINGBOARD_PASSWORD=your_password
    ```

    This means you must have a Springboard account. Please visit [here](https://www.springboard.com/) to setup a Springboard account.

## Installation

Follow these steps to set up the Job Tracker Automation tool:

1. **Clone the repository via your terminal:**

   ```bash
   git clone git@github.com:coderhimanshu1/Job-Tracker.git
   cd Job-Tracker-Automation
   ```

2. **Install required Python packages via your terminal:**

   ```bash
   pip install selenium gspread oauth2client python-dotenv BeautifulSoup4
   ```

3. **Google Sheets Setup:**
   - Create a new Google Sheet and name it **Job-Tracker-Automated**
   - Ensure you have two worksheets named "jobs" and "contacts."

4. **Set up API Credentials:**
   - Follow the Google Sheets API Credentials to obtain and save your `credentials.json` file. Visit [here](#prerequisites) for setup instructions.

5. **Configure .env file:**
   - Open the `.env` file and update it with your Springboard credentials.

## Usage

To run the script and export job details to Google Sheets, execute the following command in your terminal:

```bash
python job_tracker.py
```

After execution, you'll find the scraped job details in the "Job-Tracker-Automated" Google Sheet.

## Troubleshooting

### WebDriver Compatibility

If you encounter issues with the Chrome WebDriver, ensure it is compatible with your Chrome browser version. Visit the [official Chrome WebDriver site](https://sites.google.com/chromium.org/driver/) to download the appropriate version.

### API Credentials Error

If you receive errors related to API credentials, double-check the following:

- Ensure your `credentials.json` file is correctly placed in the project directory. Ideally the same place as your `job_tracker.py` file.
- Ensure your `.env` file is correctly place in the project directory. Ideally the same place as your `job_tracker.py` file.
- Confirm that the credentials have the necessary permissions for accessing Google Sheets.

### Script Execution Issues

If the script encounters errors during execution, consider the following steps:

1. Check your internet connection.
2. Verify that your Springboard credentials in the `.env` file are accurate.
3. Review the script for any modifications or customization that might have introduced errors.

For any persistent issues, feel free to reach out to the [project repository's issue tracker](https://github.com/coderhimanshu1/Job-Tracker/issues) for assistance.

---

**Note:** *If you encounter a security captcha, follow all the steps carefully before running the script.*
