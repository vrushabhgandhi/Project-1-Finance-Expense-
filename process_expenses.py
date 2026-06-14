#!/usr/bin/env python3
"""
Main pipeline for processing expense reports using Groq GenAI.

Usage:
    python process_expenses.py
"""

import json
from pathlib import Path
from dotenv import load_dotenv
from expense_validator import ExpenseValidator

def main():
    """Process sample expense reports."""
    
    # Load environment variables
    load_dotenv()
    
    # Setup paths
    data_dir = Path("data")
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Load sample expenses
    expenses_file = data_dir / "sample_expenses.json"
    with open(expenses_file) as f:
        expenses = json.load(f)
    
    print("\n" + "="*70)
    print("💰 SMART EXPENSE REPORT PROCESSOR")
    print("="*70)
    print(f"Processing {len(expenses)} expenses using Groq Llama 3.1...\n")
    
    # Initialize validator
    validator = ExpenseValidator()
    
    # Process all expenses
    summary = validator.process_batch(expenses)
    
    # Save results
    output_file = output_dir / "approval_summary.json"
    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    # Display results
    print("\n" + "="*70)
    print("📊 PROCESSING SUMMARY")
    print("="*70)
    print(f"Total Expenses: {summary['total_expenses']}")
    print(f"Total Amount: ${summary['total_amount']:.2f}")
    print(f"✅ Auto-Approved: {summary['approved_auto']}")
    print(f"⚠️  Flagged for Review: {summary['flagged_for_review']}")
    print("\n" + "-"*70)
    print("DETAILED RESULTS:")
    print("-"*70)
    
    for expense in summary["expenses"]:
        status = "✅ APPROVED" if expense["approved"] and not expense["requires_manual_review"] else "⚠️  REVIEW"
        flags = f" | Flags: {', '.join(expense['risk_flags'])}" if expense["risk_flags"] else ""
        
        print(f"\n{expense['expense_id']}: {expense['description']}")
        print(f"  Amount: ${expense['amount']:.2f}")
        print(f"  Category: {expense['category']}")
        print(f"  Status: {status}{flags}")
        print(f"  Reasoning: {expense['reasoning']}")
    
    print("\n" + "="*70)
    print(f"Results saved to: {output_file}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
