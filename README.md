# 💰 Smart Expense Report Processor

A GenAI-powered expense report analyzer that validates, categorizes, and summarizes employee expense claims using natural language processing.

## What It Does

1. **Reads** unstructured expense descriptions (e.g., "lunch with client at Starbucks")
2. **Validates** against company policy (amount limits, allowed categories)
3. **Categorizes** automatically (meals, travel, entertainment, equipment, etc.)
4. **Flags** suspicious expenses for manual review
5. **Summarizes** for finance team approval
6. **Logs** all decisions for audit trail

## Quick Start

### Setup virtual Env
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

##If you come across any error, please use - pip install --upgrade groq
```

### Configure
# Edit .env and add your Groq API key
```

### Run

#### Command-line Mode
```bash
python process_expenses.py
```

#### 🎨 Streamlit Web UI (Recommended)
```bash
streamlit run app_expenses.py
```

This launches an interactive web interface at `http://localhost:8501` where you can:
- ✅ Validate individual expenses in real-time
- 📊 Upload and process batch JSON files
- 📈 View analytics and reports
- 📥 Download results

## Project Structure
```
finance-expense-processor/
├── requirements.txt
├── .env.sample
├── README.md
├── app_expenses.py              # 🎨 Streamlit web UI
├── process_expenses.py          # Command-line pipeline
├── expense_validator.py         # GenAI validation logic
├── debug_groq.py               # API connection test
├── data/
│   └── sample_expenses.json     # Sample expense reports
└── outputs/
    └── approval_summary.json    # Processing results
```

## Example Usage

```python
from expense_validator import ExpenseValidator

validator = ExpenseValidator()

# Process a single expense
expense = {
    "description": "Team lunch at The Grill House restaurant",
    "amount": 125.50,
    "date": "2026-06-10",
    "employee": "John Smith"
}

result = validator.validate_expense(expense)
print(result.approved)  # True/False
print(result.category)  # "Meals & Entertainment"
print(result.risk_flags)  # ["Amount above team average", "High frequency this month"]
```

## Output Example

```json
{
  "expense_id": "EXP001",
  "description": "Team lunch at The Grill House",
  "category": "Meals & Entertainment",
  "amount": 125.50,
  "approved": true,
  "confidence": 0.95,
  "reasoning": "Meal expense within policy limits with business purpose",
  "risk_flags": [],
  "requires_manual_review": false
}
```

## GenAI Features

- **Smart Categorization:** Uses Groq Llama to understand expense context
- **Policy Compliance:** Validates against configurable limits
- **Fraud Detection:** Flags anomalies and suspicious patterns
- **Reasoning:** Explains each decision in plain language
