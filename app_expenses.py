#!/usr/bin/env python3
"""
Streamlit UI for Smart Expense Report Processor.

Run with: streamlit run app_expenses.py
"""

import streamlit as st
import json
from pathlib import Path
from dotenv import load_dotenv
from expense_validator import ExpenseValidator

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="💰 Expense Report Processor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .approved {
        color: #28a745;
        font-weight: bold;
    }
    .flagged {
        color: #ffc107;
        font-weight: bold;
    }
    .rejected {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("💰 Smart Expense Report Processor")
st.markdown("AI-powered expense validation using Groq Llama 3.1")

# Sidebar
st.sidebar.header("⚙️ Configuration")
approval_threshold = st.sidebar.slider("Approval Threshold ($)", 1000, 10000, 5000, step=500)

# Tab selection
tab1, tab2, tab3 = st.tabs(["📝 Single Expense", "📊 Batch Upload", "📈 Reports"])

# ============ TAB 1: Single Expense ============
with tab1:
    st.header("Validate Single Expense")
    
    col1, col2 = st.columns(2)
    
    with col1:
        expense_id = st.text_input("Expense ID", value="EXP001")
        description = st.text_area("Expense Description", 
                                   value="Team lunch at restaurant with clients",
                                   height=100)
    
    with col2:
        amount = st.number_input("Amount ($)", min_value=0.0, value=125.50, step=0.01)
        date = st.date_input("Date")
        employee = st.text_input("Employee Name", value="John Smith")
    
    if st.button("🔍 Validate Expense", key="single_validate"):
        with st.spinner("Analyzing expense with Groq AI..."):
            try:
                validator = ExpenseValidator()
                
                expense = {
                    "id": expense_id,
                    "description": description,
                    "amount": amount,
                    "date": str(date),
                    "employee": employee
                }
                
                result = validator.validate_expense(expense)
                
                # Display results
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Category", result.category)
                
                with col2:
                    status = "✅ APPROVED" if result.approved and not result.requires_manual_review else "⚠️ REVIEW"
                    st.metric("Status", status)
                
                with col3:
                    st.metric("Confidence", f"{result.confidence:.0%}")
                
                with col4:
                    st.metric("Amount", f"${result.amount:.2f}")
                
                # Reasoning
                st.subheader("💭 AI Reasoning")
                st.info(result.reasoning)
                
                # Risk flags
                if result.risk_flags:
                    st.subheader("⚠️ Risk Flags")
                    for flag in result.risk_flags:
                        st.warning(f"• {flag}")
                else:
                    st.success("✅ No risk flags detected")
                
                # Store result in session state
                st.session_state.last_result = result
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ============ TAB 2: Batch Upload ============
with tab2:
    st.header("📊 Batch Process Multiple Expenses")
    
    uploaded_file = st.file_uploader("Upload JSON file with expenses", type="json")
    
    if uploaded_file is not None:
        try:
            # Read JSON file
            expenses = json.load(uploaded_file)
            
            st.success(f"✅ Loaded {len(expenses)} expenses from file")
            
            if st.button("🚀 Process All Expenses", key="batch_process"):
                with st.spinner("Processing expenses with Groq AI..."):
                    validator = ExpenseValidator()
                    summary = validator.process_batch(expenses)
                    
                    # Display summary metrics
                    st.subheader("📈 Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Expenses", summary["total_expenses"])
                    
                    with col2:
                        st.metric("Total Amount", f"${summary['total_amount']:.2f}")
                    
                    with col3:
                        st.metric("Auto-Approved", summary["approved_auto"], 
                                 delta_color="off")
                    
                    with col4:
                        st.metric("Flagged for Review", summary["flagged_for_review"],
                                 delta_color="inverse")
                    
                    # Detailed results table
                    st.subheader("📋 Detailed Results")
                    
                    # Create display dataframe
                    display_data = []
                    for exp in summary["expenses"]:
                        status = "✅ Approved" if exp["approved"] and not exp["requires_manual_review"] else "⚠️ Review"
                        display_data.append({
                            "ID": exp["expense_id"],
                            "Description": exp["description"][:40] + "..." if len(exp["description"]) > 40 else exp["description"],
                            "Amount": f"${exp['amount']:.2f}",
                            "Category": exp["category"],
                            "Status": status,
                            "Confidence": f"{exp['confidence']:.0%}"
                        })
                    
                    st.dataframe(display_data, use_container_width=True)
                    
                    # Download results
                    results_json = json.dumps(summary, indent=2)
                    st.download_button(
                        label="📥 Download Results as JSON",
                        data=results_json,
                        file_name="expense_results.json",
                        mime="application/json"
                    )
                    
                    # Store in session
                    st.session_state.batch_summary = summary
        
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file format")
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")


# ============ TAB 3: Reports ============
with tab3:
    st.header("📈 Expense Analysis & Reports")
    
    # Check for data: first in session state, then on disk
    data = None
    
    # Check session state first (from batch upload in this session)
    if "batch_summary" in st.session_state:
        data = st.session_state.batch_summary
        st.info("📊 Showing batch processing results from current session")
    else:
        # Check for saved file on disk
        outputs_dir = Path("outputs")
        if outputs_dir.exists():
            summary_file = outputs_dir / "approval_summary.json"
            if summary_file.exists():
                with open(summary_file) as f:
                    data = json.load(f)
    
    if data:
        
        # Display summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Expenses", data["total_expenses"])
        
        with col2:
            st.metric("Total Amount", f"${data['total_amount']:.2f}")
        
        with col3:
            st.metric("Auto-Approved", data["approved_auto"])
        
        with col4:
            st.metric("Flagged for Review", data["flagged_for_review"])
        
        # Category breakdown
        st.subheader("📊 Category Breakdown")
        categories = {}
        for exp in data["expenses"]:
            cat = exp["category"]
            if cat not in categories:
                categories[cat] = {"count": 0, "total": 0}
            categories[cat]["count"] += 1
            categories[cat]["total"] += exp["amount"]
        
        cat_data = []
        for cat, stats in categories.items():
            cat_data.append({
                "Category": cat,
                "Count": stats["count"],
                "Total ($)": f"${stats['total']:.2f}"
            })
        
        st.dataframe(cat_data, use_container_width=True)
        
        # All expenses detail
        st.subheader("📋 All Expenses")
        for exp in data["expenses"]:
            with st.expander(f"{exp['expense_id']}: {exp['description'][:50]}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Category:** {exp['category']}")
                    st.write(f"**Amount:** ${exp['amount']:.2f}")
                
                with col2:
                    status = "✅ Approved" if exp["approved"] and not exp["requires_manual_review"] else "⚠️ Review"
                    st.write(f"**Status:** {status}")
                    st.write(f"**Confidence:** {exp['confidence']:.0%}")
                
                with col3:
                    st.write(f"**Reasoning:** {exp['reasoning']}")
                    if exp['risk_flags']:
                        st.write(f"**Flags:** {', '.join(exp['risk_flags'])}")
    
    else:
        st.info("💡 No processed data yet. Run expenses through the Single Expense or Batch Upload tabs first.")


# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #888;'>
    💰 Smart Expense Report Processor | Powered by Groq Llama 3.1
    </div>
    """, unsafe_allow_html=True)
