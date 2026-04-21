import gradio as gr
import sqlite3
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import re

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

conn = sqlite3.connect(":memory:", check_same_thread=False)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL,
    hire_date TEXT
);

INSERT INTO employees VALUES (1, 'Alice Johnson', 'Engineering', 95000, '2020-03-15');
INSERT INTO employees VALUES (2, 'Bob Smith', 'Marketing', 72000, '2019-07-22');
INSERT INTO employees VALUES (3, 'Carol White', 'Engineering', 105000, '2018-01-10');
INSERT INTO employees VALUES (4, 'David Brown', 'HR', 65000, '2021-11-05');
INSERT INTO employees VALUES (5, 'Eva Martinez', 'Engineering', 98000, '2020-09-30');
INSERT INTO employees VALUES (6, 'Frank Lee', 'Marketing', 78000, '2017-04-18');
INSERT INTO employees VALUES (7, 'Grace Kim', 'HR', 70000, '2022-02-14');
INSERT INTO employees VALUES (8, 'Henry Wilson', 'Engineering', 112000, '2016-08-25');

CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    budget REAL,
    status TEXT
);

INSERT INTO projects VALUES (1, 'AI Platform', 'Engineering', 500000, 'active');
INSERT INTO projects VALUES (2, 'Brand Refresh', 'Marketing', 150000, 'completed');
INSERT INTO projects VALUES (3, 'HR System', 'HR', 80000, 'active');
INSERT INTO projects VALUES (4, 'Mobile App', 'Engineering', 300000, 'active');
INSERT INTO projects VALUES (5, 'SEO Campaign', 'Marketing', 50000, 'completed');
""")
conn.commit()

schema = """
Tables:
1. employees (id, name, department, salary, hire_date)
2. projects (id, name, department, budget, status)
"""

prompt = ChatPromptTemplate.from_template("""
You are an expert SQL assistant. Convert the natural language question to a SQLite SQL query.

Database Schema:
{schema}

Rules:
- Return ONLY the SQL query, nothing else
- No markdown, no explanation, no backticks
- Use valid SQLite syntax

Question: {question}
SQL:""")

chain = prompt | llm | StrOutputParser()

def query_database(question):
    if not question.strip():
        return "", ""
    
    sql = chain.invoke({"schema": schema, "question": question})
    sql = sql.strip().strip("```").strip()
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [d[0] for d in cursor.description] if cursor.description else []
        
        if not results:
            return sql, "No results found."
        
        header = " | ".join(columns)
        separator = "-" * len(header)
        rows = "\n".join([" | ".join(str(v) for v in row) for row in results])
        
        return sql, f"{header}\n{separator}\n{rows}"
    except Exception as e:
        return sql, f"Error: {str(e)}"

with gr.Blocks(title="SQL Agent") as app:
    gr.Markdown("# Natural Language SQL Agent")
    gr.Markdown("Ask questions in plain English and get SQL queries + results instantly.")
    
    gr.Markdown("""
**Sample questions:**
- Show all engineers
- Who has the highest salary?
- What is the average salary by department?
- Show all active projects
- Which department has the most employees?
""")
    
    question_input = gr.Textbox(label="Ask a question", placeholder="Show me all engineers with salary above 100000")
    ask_btn = gr.Button("Ask", variant="primary")
    
    sql_out = gr.Code(label="Generated SQL", language="sql")
    result_out = gr.Textbox(label="Results", lines=10)
    
    ask_btn.click(fn=query_database, inputs=[question_input], outputs=[sql_out, result_out])
    question_input.submit(fn=query_database, inputs=[question_input], outputs=[sql_out, result_out])

app.launch()