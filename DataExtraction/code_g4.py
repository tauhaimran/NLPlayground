### Tauha Imran 22i1239 - G4
#### NLP - A1 - Data Extraction
#setting up selenium

#download selenium
#!pip install selenium
#also need to download the appropriate web driver for our browser
#for chrome, we can download it from https://sites.google.com/chromium.org/driver/s/downloads
#make sure to download the version that matches your browser version

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import requests

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.supremecourt.gov.pk/judgement-search/")
#driver.get("https://techwithtim.com/")
wait = WebDriverWait(driver, 20)


import os, json, time, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.supremecourt.gov.pk/judgement-search/")
wait = WebDriverWait(driver, 20)

os.makedirs("judgementpdfs", exist_ok=True)
all_data = []

print("🔍 Collecting dropdown options...")

# --- get all judge/case subject options ---
judge_box = wait.until(EC.element_to_be_clickable((By.ID, "select2-former_judge-container")))
judge_box.click()
time.sleep(1)
options = driver.find_elements(By.XPATH, "//ul[@id='select2-former_judge-results']/li")
judge_options = [opt.text.strip() for opt in options if opt.text.strip()]
driver.find_element(By.TAG_NAME, "body").click()  # close dropdown

print(f"✅ Found {len(judge_options)} Judge/Case Subject options.")

# --- reported options ---
reported_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "reported"))))
reported_options = [opt.text.strip() for opt in reported_dropdown.options if opt.text.strip()]

print(f"✅ Found {len(reported_options)} Reported options: {reported_options}")

# --- loop over combos ---
for judge in judge_options:
    for rep in reported_options:
        print(f"\n➡️ Searching for Judge/CaseSubject = '{judge}', Reported = '{rep}'")

        # reopen judge dropdown each time
        judge_box = wait.until(EC.element_to_be_clickable((By.ID, "select2-former_judge-container")))
        judge_box.click()
        search_field = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-search__field")))
        search_field.send_keys(judge + Keys.ENTER)

        reported_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "reported"))))
        reported_dropdown.select_by_visible_text(rep)

        # click search
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Search Result']")))
        search_btn.click()
        time.sleep(3)

        rows = driver.find_elements(By.XPATH, "//table//tr")
        print(f"📄 Found {len(rows)-1} rows in this search result.")

        for row in rows[1:]:  # skip header
            cols = row.find_elements(By.TAG_NAME, "td")
            if not cols: continue

            case_no = cols[2].text.strip().replace("/", "-")
            case_title = cols[3].text.strip()
            print(f"   → Case: {case_no} | {case_title}")

            pdf_link = None
            filename = None
            pdf_size = None
            try:
                pdf_link = row.find_element(By.XPATH, ".//a[contains(@href,'.pdf')]").get_attribute("href")
                filename = f"judgementpdfs/judgement_{case_no}.pdf"
                print(f"     ⬇️ Downloading PDF: {filename}")
                with open(filename, "wb") as f:
                    f.write(requests.get(pdf_link).content)
                pdf_size = os.path.getsize(filename)
                print(f"     ✅ Downloaded ({pdf_size} bytes)")
            except:
                print("     ⚠️ No PDF found for this case.")

            all_data.append({
                "Case Subject": cols[1].text.strip(),
                "Case No": case_no,
                "Case Title": case_title,
                "Author Judge": cols[4].text.strip(),
                "Upload Date": cols[5].text.strip(),
                "Judgment Date": cols[6].text.strip(),
                "Citation": cols[7].text.strip(),
                "SCCitation": cols[8].text.strip(),
                "PDF": filename if pdf_link else None,
                "File Size": pdf_size
            })

# save to JSON
print("\n💾 Saving results to SupremeCourt_G4.json ...")
with open("SupremeCourt_G4.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

print("🎉 Done! Total cases scraped:", len(all_data))

driver.quit()
