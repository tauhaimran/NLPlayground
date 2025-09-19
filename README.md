Ahhh okay, got it ✅
You don’t want the README just for **this scraper**, but for the **whole `NLPlayground` repo**, since that repo will hold **all your NLP assignments**.

Here’s a proper **repo-level README.md** 👇

---

# 🧠 NLPlayground

*A collection of my NLP (Natural Language Processing) assignments, experiments, and projects.*

---

## 📖 Overview

This repository contains my coursework and experiments in **Natural Language Processing (NLP)**.
Each assignment explores different aspects of NLP, from **basic text preprocessing** to **information extraction** and **language modeling**.

The repo is structured so that each assignment has:

* 📂 Its own folder (with code, dataset(s), and outputs).
* 📄 A README or description of the task.
* 💻 Implementations in **Python** (using Jupyter Notebooks `.ipynb` or scripts `.py`).

---

## 📂 Repository Structure

```
NLPlayground/
│── Assignment1_DataExtraction/   # Supreme Court Judgement Scraper
│   ├── supreme_court_scraper.py
│   ├── SupremeCourt_G4.json
│   ├── judgementpdfs/
│   └── README.txt
│
│── ...
│
└── README.md   # This file
```

---

## 🚀 Assignments

### 📌 Assignment 1 – Data Extraction (Supreme Court Judgements)

* Web scraping using **Selenium**.
* Extracted case metadata + downloaded judgment PDFs.
* Output stored as JSON + structured folders.

📎 Code: [`Assignment1_DataExtraction`](./Assignment1_DataExtraction)

---

### 📌 Assignment 2 – N-gram Language Models

* Built **unigram, bigram, trigram** models.
* Implemented **Laplace/Add-1 smoothing**.
* Predicted sentence probabilities.

📎 Code: [`Assignment2_LanguageModels`](./Assignment2_LanguageModels)

---

### 📌 Assignment 3 – Text Classification

* Implemented a **Naive Bayes classifier** for text.
* Used **confusion matrix, precision, recall, F1-score**.
* Compared **macro** vs **weighted** evaluation metrics.

📎 Code: [`Assignment3_TextClassification`](./Assignment3_TextClassification)

---

(⚡ more assignments will be added as the course progresses.)

---

## ⚙️ Tools & Dependencies

* Python 3.x
* Jupyter Notebook
* Selenium
* scikit-learn
* pandas / numpy / matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Author

**Tauha Imran**

* 🎓 FAST NUCES, Islamabad
* 📌 Roll No: 22i1239 – Group 4
* 📚 NLP Course Assignments

---
