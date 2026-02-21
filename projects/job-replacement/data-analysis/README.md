# Data Analysis Automation 📊

**Automation Level:** 🟡 MEDIUM-HIGH (60-80% of tasks automatable)

---

## Jobs Being Replaced

| Role | Current Salary | Automation % | Monthly Savings |
|------|---------------|--------------|-----------------|
| Report Analyst | $4,000-6,000 | 80% | $3,200-4,800 |
| Dashboard Creator | $4,500-6,500 | 75% | $3,375-4,875 |
| Data Entry Analyst | $3,000-4,500 | 95% | $2,850-4,275 |
| Junior Data Analyst | $4,000-5,500 | 70% | $2,800-3,850 |
| BI Report Generator | $5,000-7,000 | 80% | $4,000-5,600 |

---

## Key Automations

### 1. Natural Language to SQL
**Replaces:** Manual query writing

```
Flow: Question in English → AI Generate SQL → Execute → Return Results
```

**n8n Templates:**
- `Chat with Postgresql Database`
- `Generate SQL queries from schema only - AI-powered`
- `Talk to your SQLite database with a LangChain AI Agent`

### 2. Automated Reporting
**Replaces:** Manual report generation

```
Flow: Schedule → Query Data → AI Analyze → Generate Report → Distribute
```

**n8n Templates:**
- `AI Agent to chat with Airtable and analyze data`
- `Visualize SQL Agent queries with OpenAI and Quickchart.io`

### 3. Data Visualization
**Replaces:** Manual chart creation

```
Flow: Data + Question → AI Select Chart Type → Generate Visualization
```

**n8n Templates:**
- `Visualize your SQL Agent queries with OpenAI and Quickchart.io`

### 4. Trend Analysis
**Replaces:** Manual trend spotting

```
Flow: Historical Data → AI Pattern Recognition → Insights → Alerts
```

### 5. Data Quality Checks
**Replaces:** Manual data validation

```
Flow: New Data → AI Validate → Flag Anomalies → Report
```

---

## SQL Agent Script (Python)

```python
import openai
import psycopg2
import json
from typing import List, Dict

class SQLAgent:
    def __init__(self, db_config: dict):
        self.conn = psycopg2.connect(**db_config)
        self.schema = self._get_schema()
    
    def _get_schema(self) -> str:
        """Get database schema for AI context"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """)
        
        schema = {}
        for table, column, dtype in cursor.fetchall():
            if table not in schema:
                schema[table] = []
            schema[table].append(f"{column} ({dtype})")
        
        return "\n".join([
            f"Table {t}: {', '.join(cols)}" 
            for t, cols in schema.items()
        ])
    
    def ask(self, question: str) -> dict:
        """Convert natural language to SQL and execute"""
        
        prompt = f"""
        You are a SQL expert. Convert this question to a PostgreSQL query.
        
        DATABASE SCHEMA:
        {self.schema}
        
        QUESTION: {question}
        
        Return JSON with:
        - sql: the SQL query
        - explanation: what the query does
        
        Rules:
        - Only SELECT queries (no modifications)
        - Use appropriate JOINs
        - Include LIMIT if results could be large
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Execute the query
        cursor = self.conn.cursor()
        cursor.execute(result['sql'])
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        return {
            "question": question,
            "sql": result['sql'],
            "explanation": result['explanation'],
            "columns": columns,
            "data": [dict(zip(columns, row)) for row in rows],
            "row_count": len(rows)
        }
    
    def generate_insight(self, data: List[Dict]) -> str:
        """Generate AI insight from query results"""
        
        prompt = f"""
        Analyze this data and provide insights:
        
        DATA:
        {json.dumps(data[:50], indent=2)}  # First 50 rows
        
        Provide:
        1. Key findings (3-5 bullet points)
        2. Trends or patterns
        3. Anomalies or outliers
        4. Recommendations
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content

# Example usage
db_config = {
    "host": "localhost",
    "database": "analytics",
    "user": "analyst",
    "password": "password"
}

agent = SQLAgent(db_config)

# Ask questions in plain English
result = agent.ask("What were our top 10 products by revenue last month?")
print(f"SQL: {result['sql']}")
print(f"Results: {result['data']}")

# Get AI insights
insights = agent.generate_insight(result['data'])
print(f"Insights: {insights}")
```

---

## Automated Report Generator

```python
import openai
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

def generate_weekly_report(data: dict) -> str:
    """Generate a complete weekly report with charts"""
    
    prompt = f"""
    Generate a professional weekly business report from this data:
    
    {json.dumps(data, indent=2)}
    
    Structure:
    1. Executive Summary (2-3 sentences)
    2. Key Metrics (table format)
    3. Week-over-Week Changes
    4. Highlights (wins)
    5. Areas of Concern
    6. Recommendations
    
    Use markdown formatting.
    """
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def create_chart(data: list, chart_type: str, title: str) -> str:
    """Generate chart and return as base64"""
    
    plt.figure(figsize=(10, 6))
    
    if chart_type == "bar":
        plt.bar([d['label'] for d in data], [d['value'] for d in data])
    elif chart_type == "line":
        plt.plot([d['label'] for d in data], [d['value'] for d in data])
    elif chart_type == "pie":
        plt.pie([d['value'] for d in data], labels=[d['label'] for d in data])
    
    plt.title(title)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

# Example
weekly_data = {
    "revenue": 125000,
    "revenue_change": "+12%",
    "customers": 450,
    "new_customers": 45,
    "churn": 5,
    "top_products": ["Widget A", "Widget B", "Widget C"],
    "issues": ["Shipping delays on West Coast"]
}

report = generate_weekly_report(weekly_data)
print(report)
```

---

## Automation Stack

```
Data Sources (DB, APIs, Sheets)
    ↓
Scheduled Trigger (daily/weekly)
    ↓
Pull Data
    ↓
AI Analysis
    ↓
Generate Visualizations
    ↓
Compile Report
    ↓
Distribute (Email, Slack, Dashboard)
```

---

## Selling Points for Clients

**Pain Points:**
- "Reports take forever to create"
- "I can't get data without bothering IT"
- "Dashboards are always out of date"
- "We don't know what questions to ask"

**Your Pitch:**
> "Talk to your data in plain English. Ask 'What were our best products last month?' and get instant answers with charts. Weekly reports generated automatically. $400/month vs $5,000 for a data analyst."

---

## Cost Analysis

| Item | Monthly Cost |
|------|-------------|
| n8n (self-hosted) | $20 |
| OpenAI API | $40-120 |
| Charting (Quickchart) | $0 |
| **Total** | $60-140 |
| **Savings** | $3,500-5,500+ |
| **ROI** | **30-90x** |
