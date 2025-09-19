# NLPlayground 📝
Assignments & experiments in Natural Language Processing (NLP).

---

## 📌 Assignment 1 – Data Extraction (Supreme Court Judgments)
This project automates the extraction of case judgments from the [Supreme Court of Pakistan](https://www.supremecourt.gov.pk/judgement-search/) using **Selenium**.

### ✨ Features
- Scrapes **case details**: subject, case no, title, judge, upload/judgment dates, citations.
- Downloads available **PDF files** into `judgementpdfs/`.
- Saves structured **JSON dataset** (`SupremeCourt_G4.json`).
- Provides **console logs** to track scraping progress.

### 🛠️ Setup
```
# install dependencies
pip install selenium requests webdriver-manager
```