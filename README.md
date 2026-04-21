# Natural Language SQL Agent

Ask questions in plain English and get SQL queries + results instantly.

## What it does
- Takes a natural language question as input
- Converts it to a SQL query using Groq LLM
- Executes the query on a SQLite database
- Returns the results in a clean format

## Tech Stack
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **Database**: SQLite (in-memory)
- **Framework**: LangChain
- **UI**: Gradio

## Sample Questions
- Show all engineers
- Who has the highest salary?
- What is the average salary by department?
- Show all active projects
- Which department has the most employees?

## Setup

1. Clone the repo
2. Create virtual environment

    python -m venv venv
    venv\Scripts\activate

3. Install dependencies

    pip install langchain langchain-groq python-dotenv gradio

4. Create `.env` file

    GROQ_API_KEY=your_key_here

5. Run

    python app.py

## Built by
Shubham Yadav — building AI projects in public