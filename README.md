# 🎓 EduPlan AI

![EduPlan AI Banner](assets/banner.png)

EduPlan AI is an AI-powered platform that helps teachers create structured, professional educational plans in minutes.

Designed for real-world school use, it supports study visits, classroom activities, and institutional documentation.

---

## Core Features

- 🤖 AI-generated educational plans
- 🖼️ Automatic activity banner generation
- 📄 PAA (Annual Activity Plan) document export
- 📝 Parent authorization document generation
- 💰 Automatic cost calculation per student and total
- 🌍 Multi-language support (PT, EN, ES, FR)
- 🧠 Suggested subjects and pedagogical structure

---

## Application Preview

### 🧩 Setup – Define the activity
![Setup](docs/screens/setup.png)

### 🧠 Generated Educational Plan
![Plan](docs/screens/plan.png)

### 💰 Costs and Materials
![Costs](docs/screens/costs.png)

### 📄 Final Output and Documents
![Output](docs/screens/output.png)

---

##  Installation
Clone the repository:

git clone https://github.com/valterjalvesteixeira/Eduplan-AI.git

cd Eduplan-AI

Create virtual environment:

python -m venv .venv

Activate environment (Windows):

.venv\Scripts\activate

Install dependencies:

python -m pip install -r requirements.txt

---
##  API Configuration

Create a .env file in the root folder:

OPENAI_API_KEY=your_api_key_here

---
##  Important:

Do NOT share your API key
Do NOT upload .env to GitHub
Ensure .env is in .gitignore

---
##  ▶️ Run the Application

streamlit run app.py

Open in your browser:

http://localhost:8501
 
---
##  How it Works
Select a theme (e.g., History, Science)
Define the activity details
Generate a structured plan using AI
Automatically generate:
Educational plan
Activity banner
PAA document
Parent authorization
Export documents as PDF

---
##  Use Cases

School study visits
Classroom activities
Educational program planning
Institutional reporting (PAA)
Teacher workflow optimization

---
️## Tech Stack

Python
Streamlit
OpenAI API
ReportLab (PDF generation)
Pillow (image processing)

---
##  Project Status
Core functionality complete
Continuous improvements in UI/UX and automation
Ready for real-world testing in educational environments

---
##  👤 Author

Valter Teixeira

---
##  📄 License

MIT