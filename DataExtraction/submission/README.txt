Tauha Imran - 22i1239 - G4
NLP - Assignment 1 (Data Extraction)

====================================
Tools Used
====================================
- Python 3
- Selenium
- Requests
- WebDriver Manager (for auto-installing ChromeDriver)
- Google Chrome Browser

====================================
Steps Followed
====================================
1. Installed required libraries:
   pip install selenium requests webdriver-manager

2. Opened the Supreme Court of Pakistan "Judgement Search" page.

3. Used Selenium to:
   - Collect Judge/Case Subject options.
   - Collect Reported options.
   - Iterate through all combinations and search.

4. For each search result:
   - Extracted case details (subject, case no, title, judge, upload date, judgment date, citation, SCCitation).
   - Downloaded PDFs (if available) and stored them in:
     PDFs_22i1239/

5. Stored all metadata into:
   SupremeCourt_G4.json

6. Printed progress logs to console (for transparency).

====================================
Issues Faced
====================================
- Some cases did not contain downloadable PDF files.
- Website response was sometimes slow; had to add wait times.
- Case numbers containing "/" were replaced with "-" to avoid filename errors.

====================================
Submission Notes
====================================
This zip contains:
- Code file (supreme_court_scraper.py)
- JSON file (SupremeCourt_G4.json)
- PDF folder (PDFs_22i1239/)
- This readme.txt