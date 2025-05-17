# Email and Phone Number Crawler (Flask Web App)

This project is a web application built with Flask that allows users to upload a CSV file containing website links and then crawls those websites to extract email addresses and phone numbers. The results are provided back to the user as a downloadable CSV file.

## Features

*   Web-based interface for easy use.
*   Upload CSV file with website names and links.
*   Crawls websites using Selenium (requires Chrome and ChromeDriver).
*   Extracts email addresses using regex.
*   Extracts various phone number formats using multiple regex patterns.
*   Handles `mailto:` and `tel:` links.
*   Provides results as a downloadable CSV file.
*   Simple and clean UI using Bootstrap 5.

## Prerequisites

Before running this project, ensure you have the following installed:

1.  **Python 3.7+**
2.  **Google Chrome Browser**
3.  **ChromeDriver:** Download the ChromeDriver version that matches your installed Chrome browser version from [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/). You will need to make sure `chromedriver` is accessible in your system's PATH, or you'll need to specify the path to the executable in the `app/crawler.py` file (see `EmailCrawler.__init__`).

## Setup and Installation

1.  **Clone the repository (or create the files manually based on the provided code):**

    ```bash
    # If using git
    # git clone <repository_url>
    # cd <project_directory>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  Make sure your virtual environment is activated (`source venv/bin/activate`).
2.  Navigate to the project's root directory (`Email_crawler`).
3.  Run the application:

    ```bash
    python run.py
    ```

4.  You should see output in your terminal indicating that the Flask development server is running. It will likely say something like:

    ```
    Starting Flask application...
    Please visit http://127.0.0.1:8000 in your browser
     * Running on http://127.0.0.1:8000 (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: ...
    ```

5.  Open your web browser and go to the address shown (e.g., `http://127.0.0.1:8000`).

## Usage

1.  Prepare a CSV file with at least two columns: `"website name"` and `"website link"`. Ensure the column headers match exactly (case-sensitive).
    Example `input.csv`:
    ```csv
    website name,website link
    Example Site 1,https://example.com
    Another Site,http://anothersite.org
    Local Business,www.localbiz.net
    ```
2.  On the web page, click the "Choose File" button and select your CSV file.
3.  Click the "Process CSV" button.
4.  The application will start crawling the websites. You will see a progress bar and status text.
5.  Once processing is complete, a results CSV file (`results.csv`) will be automatically downloaded by your browser.
6.  The downloaded CSV will include the original website names and links, plus new columns for "emails" and "phone numbers" found on each site, separated by semicolons.


## Development

If you want to modify the crawler logic (e.g., change regex patterns, adjust crawling depth), you can edit the `app/crawler.py` file. Remember to restart the Flask application after making changes.

```bash
# Stop the server (Ctrl+C)
# python run.py
```
