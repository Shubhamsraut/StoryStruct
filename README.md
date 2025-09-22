# 📄 StoryStruct  
### _Transform your requirements into actionable insights_

![StoryStruct Banner](https://via.placeholder.com/1200x300.png?text=StoryStruct+-+User+Story+Extractor)  

## 🚀 Overview  
**StoryStruct** is a sleek and powerful **Streamlit application** designed for **Business Analysts** and **Product Teams**. It extracts **Epics**, **User Stories**, and **Acceptance Criteria** from `.docx` requirement documents, summarizes them with metrics, and provides filtering, search, and export options—all within a modern, responsive UI.  

---

## ✨ Features  
- 📂 **Upload Multiple Word Documents** (`.docx`) simultaneously.  
- 🔎 **Automatic Parsing** of Epics, User Stories, and Acceptance Criteria.  
- 📊 **Dynamic Metrics**:  
  - Total Epics, Stories, ACs, Avg ACs per Story.  
  - Filtered metrics update instantly.  
- 🔖 **Smart Filters**: Filter by Epic, Source File, Story ID, or search keywords.  
- 🖼 **Beautiful UI**: Inline file chips, styled metric cards, and responsive tabs.  
- 📥 **Export Options**: Download filtered results in **CSV** or **Excel**.  
- 🔗 **Future-Ready Jira Integration**: Placeholder for OAuth-based Jira sync.  
- 🧑‍🏫 **User Manual**: Includes sample user story and AC formats for guidance.  

---

## 🛠 Tech Stack  
| Component       | Technology           |
|-----------------|--------------------|
| Frontend & App  | [Streamlit](https://streamlit.io) |
| Backend Parsing | [python-docx](https://python-docx.readthedocs.io/) |
| Data Processing | [pandas](https://pandas.pydata.org/) |
| Exports         | xlsxwriter, CSV    |

---



## 📦 Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/storystruct.git
cd storystruct
```bash

2️⃣ Create & Activate Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows



