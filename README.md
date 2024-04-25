# Google News Scraper
This script automates the extraction of news articles from Google News based on a specified date range. It utilizes the Selenium library to automate a web browser and the Pandas library for data manipulation and storage.

# Prerequisites
Before running the script, ensure that you have the following dependencies installed:

- Python >=3.7.8
- Selenium library (pip install selenium)
- Pandas
- ChromeDriver (automatically installed by webdriver_manager)

# Setup:
Clone or download the project repository to your local machine.
Install the necessary Python dependencies as mentioned in the Prerequisites section.

# Usage:

Open the GoogleNews.py file in a text editor.
Modify the STARTDATE, ENDDATE, and filename variables according to your desired date range and output file path.
Example for start and end date. Format for date is dd/mm/yyyy
```bash
STARTDATE  = "24/06/2023"
ENDDATE = "24/06/2023"
```
Save the file.

# Running the Script:

- Open a terminal or command prompt.
- Navigate to the directory containing the GoogleNews.py file.
- Run the script using the following command:
- python GoogleNews.py

# Additional Notes:

The script uses a Chrome web browser for scraping. Ensure you have Google Chrome installed on your machine.
The script may take some time to execute, depending on the number of articles and your internet connection speed.
The extracted article details (headline, news source, link, date posted) are stored in a CSV file.
Duplicate rows in the output file are automatically removed.
The script automatically installs the ChromeDriver binary using webdriver_manager to ensure compatibility.