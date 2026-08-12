# 📝 Notes Manager

A Python-based Notes Management System that allows users to create, manage, search, analyze, visualize, and generate AI-powered study notes.

The project uses **MySQL** as the primary database and provides a **Streamlit web interface** for managing notes. It also integrates **Pandas, NumPy, Matplotlib, Seaborn, Power BI, and Groq AI** for analytics, visualization, dashboarding, and AI-powered features.

---

## 🚀 Features

### 🗂️ Note Management

- Add Note
- View Notes
- Search Notes
- Update Notes
- Delete Notes
- Filter Notes
- Change Note Status

### 📊 Data Analysis

- Total notes analysis
- Category-wise analysis
- Priority-wise analysis
- Status analysis
- AI vs Manual note analysis
- Statistical analysis using Pandas and NumPy

### 📈 Data Visualization

- Category-wise visualization
- Priority-wise visualization
- Status visualization
- AI vs Manual visualization
- Interactive charts using Streamlit


## 📊 Power BI Dashboard

The project also includes an interactive Power BI dashboard
for analyzing notes data.

The dashboard provides:

- Total Notes KPI
- Active vs Completed Notes
- Category-wise analysis
- Priority-wise analysis
- AI vs Manual Notes
- Interactive filtering
- Data visualization

![Power BI Dashboard](Dashboard.png)

### 🤖 AI Features

- AI Note Generation
- AI Note Summarization
- AI Quiz Generation
- Quiz export as text file
- Powered by Groq AI

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| OOP | Application structure |
| MySQL | Database management |
| MySQL Connector/Python | Python-MySQL connection |
| Pandas | Data analysis |
| NumPy | Numerical analysis |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Streamlit | Web application interface |
| Power BI | Interactive analytics dashboard |
| Groq AI | AI-powered features |

---

## 🏗️ Project Structure

```text
Notes_Manager/
│
├── app.py
├── notes.py
├── database.py
├── ai_helper.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── Image/
│   └── Dashboard.png
│
└── Quiz_*.txt