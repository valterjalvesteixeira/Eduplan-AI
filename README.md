![EduPlan AI](assets/banner.png)

# EduPlan AI — AI Educational Activity Planner

EduPlan AI is a Python-based AI agent that generates structured classroom activities using Large Language Models.

The system helps teachers design engaging learning experiences that integrate Artificial Intelligence into the classroom while maintaining a structured pedagogical framework.

This project demonstrates how LLMs can be combined with schema validation, prompt engineering, and modular agent design to produce reliable educational content.

---

## Key Features

- AI-generated classroom activities
- Structured JSON educational plans
- Multi-level education support
- Pydantic schema validation for reliable outputs
- Prompt-engineered activity generation
- Command-line interface for generating lesson plans
- Automatic saving of generated plans

---

## System Architecture

Teacher Input  
↓  
Prompt Builder  
↓  
LLM (OpenAI API)  
↓  
Structured JSON Output  
↓  
Pydantic Schema Validation  
↓  
Educational Plan  

This architecture ensures that LLM outputs remain structured, validated, and reliable for educational use.

---

## Project Structure

```
eduplan-ai

assets/
banner.png

runs/
Generated lesson plans

src/
Core application modules

agent.py
planner.py
llm_planner.py
validator.py
schemas.py
prompts.py
tools.py
logger.py
test_llm_planner.py

run.py
CLI runner for generating lesson plans

.env.example
Example environment configuration

requirements.txt
Project dependencies

README.md
Project documentation
```

---

## Installation

Clone the repository

```
git clone https://github.com/valterjalvesteixeira/Eduplan-AI.git
cd Eduplan-AI
```

Install dependencies

```
pip install -r requirements.txt
```

Create environment file

```
cp .env.example .env
```

Add your OpenAI API key inside the `.env` file.

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the Project

Generate a new educational activity plan using the CLI runner.

Example:

```
python run.py --goal "AI-assisted learning activities" --audience "10-12 years old" --duration 60
```

After generation, the plan is automatically saved in the `runs/` folder.

Example output file:

```
runs/eduplan_20260304_143210.json
```

---

## Example Generated Plan

Each generated plan follows a structured format:

```
{
  "meta": {...},
  "learning_objectives": [...],
  "levels": [...],
  "risk_analysis": [...]
}
```

This structured output allows the plans to be reused by educational platforms or integrated into other applications.

---

## Testing the Planner

To test the LLM planner module directly:

```
python -m src.test_llm_planner
```

This validates that:

- The LLM response follows the schema
- The OpenAI connection works
- The pipeline generates valid educational plans

---

## Technologies Used

- Python
- OpenAI API
- Pydantic
- Prompt Engineering

---

## Purpose of the Project

This project demonstrates practical techniques used in modern AI-driven software systems:

- Structured LLM outputs
- Schema validation for reliability
- AI agent pipelines
- Educational AI applications

It is designed as a portfolio project for AI engineering and AI agent development.

---

## Author

Valter Teixeira

Educational program designer with 12+ years of experience working with schools, museums, and cultural institutions.

Areas of experience include:

- educational program design
- museum learning experiences
- school partnerships
- experiential learning
- cultural education
