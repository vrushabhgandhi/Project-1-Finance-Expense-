# 🎨 Streamlit UI Quick Reference

## Quick Start Guide

### Finance Expense Processor

```powershell
# 1. Navigate to project
cd "c:\projects\Finance & Healthcare\finance-expense-processor"

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Install dependencies (first time only)
pip install -r requirements.txt

# 4. Run Streamlit app
streamlit run app_expenses.py
```

**Opens at:** `http://localhost:8501`

**Features:**
- 📝 **Single Expense Tab:** Validate individual expenses in real-time
- 📊 **Batch Upload Tab:** Process multiple expenses from JSON file
- 📈 **Reports Tab:** View analytics and historical results

---

### Healthcare Intake Assistant

```powershell
# 1. Navigate to project
cd "c:\projects\Finance & Healthcare\healthcare-intake-assistant"

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Install dependencies (first time only)
pip install -r requirements.txt

# 4. Run Streamlit app
streamlit run app_intake.py
```

**Opens at:** `http://localhost:8501`

**Features:**
- 👤 **Single Patient Tab:** Process individual intakes with clinical pattern detection
- 👥 **Batch Upload Tab:** Process multiple patients from JSON file
- 📊 **Reports Tab:** View urgency breakdown and detailed analysis

---

## Features Comparison

### Finance Expense Processor

| Feature | Description |
|---------|-------------|
| **Single Expense Validation** | Real-time categorization and approval status |
| **Policy Enforcement** | Validates amounts against category limits |
| **Risk Detection** | Identifies suspicious patterns and personal items |
| **Batch Processing** | Upload JSON to process multiple expenses |
| **Export Results** | Download approval summary as JSON |
| **Historical Reports** | View past processing results |

### Healthcare Intake Assistant

| Feature | Description |
|---------|-------------|
| **Patient Intake** | Converts unstructured symptoms to structured form |
| **Clinical Pattern Detection** | Identifies urgent conditions from symptom combinations |
| **Medication Tracking** | Extracts current medications and allergies |
| **Suggested Questions** | AI-generated clinically relevant follow-up questions |
| **Provider Summary** | One-paragraph clinical summary for doctor |
| **Batch Processing** | Process multiple patient intakes at once |
| **Urgency Triage** | Automatic sorting by urgency level |

---

## Using Sample Data

### Finance Project

Sample data is pre-loaded in `data/sample_expenses.json`:
```json
[
  {
    "id": "EXP001",
    "description": "Team lunch at The Grill House restaurant with clients",
    "amount": 125.50,
    "date": "2026-06-10",
    "employee": "John Smith"
  },
  ...
]
```

### Healthcare Project

Sample data is pre-loaded in `data/sample_patient_input.json`:
```json
[
  {
    "patient_id": "P001",
    "description": "I've had a terrible headache for 3 days with stiff neck..."
  },
  ...
]
```

---

## Troubleshooting

### Issue: Port 8501 already in use

**Solution:**
```powershell
streamlit run app_expenses.py --server.port 8502
```

### Issue: API errors

**Solution:** Check Groq API key in `.env` file:
```powershell
python debug_groq.py
```

### Issue: Missing modules

**Solution:** Reinstall requirements:
```powershell
pip install --upgrade -r requirements.txt
```

---

## Performance Notes

- **Finance App:** ~2-3 seconds per expense with Groq API
- **Healthcare App:** ~3-5 seconds per patient intake with clinical analysis
- **Batch Processing:** Scales linearly with number of records

---

## Architecture

Both Streamlit apps:
- ✅ Use existing Python logic (no duplication)
- ✅ Call the same validator/processor classes
- ✅ Generate identical JSON outputs
- ✅ Display results in user-friendly format
- ✅ Support batch upload/download

```
┌─────────────────────┐
│  Streamlit UI       │  (app_expenses.py / app_intake.py)
├─────────────────────┤
│  Validator/         │  (expense_validator.py / intake_processor.py)
│  Processor Classes  │
├─────────────────────┤
│  Groq API           │  (llama-3.1-8b-instant)
└─────────────────────┘
```

---

## Next Steps

1. ✅ Install Streamlit: `pip install -r requirements.txt`
2. ✅ Run the app: `streamlit run app_*.py`
3. ✅ Test with sample data
4. ✅ Upload your own data (JSON format)
5. ✅ Export results

**Enjoy the interactive UI!** 🎉
