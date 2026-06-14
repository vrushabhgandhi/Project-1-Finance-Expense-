"""GenAI-powered expense report validator using Groq."""

import os
import json
from typing import Optional
from dataclasses import dataclass, asdict
from groq import Groq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExpenseValidation:
    """Validated expense with AI reasoning."""
    expense_id: str
    description: str
    amount: float
    category: str
    approved: bool
    confidence: float
    reasoning: str
    risk_flags: list[str]
    requires_manual_review: bool


class ExpenseValidator:
    """Validates and categorizes expenses using Groq LLM."""
    
    # Allowed expense categories
    VALID_CATEGORIES = [
        "Travel - Flights",
        "Travel - Hotels",
        "Travel - Ground Transportation",
        "Meals & Entertainment",
        "Office Supplies",
        "Software & Subscriptions",
        "Professional Services",
        "Equipment",
        "Training & Development",
        "Client Entertainment",
        "Other"
    ]
    
    # Policy limits per category (in USD)
    CATEGORY_LIMITS = {
        "Meals & Entertainment": 150,
        "Client Entertainment": 500,
        "Travel - Hotels": 300,
        "Travel - Flights": 2000,
        "Software & Subscriptions": 1000,
        "Equipment": 5000,
        "Training & Development": 2000,
    }
    
    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize the expense validator with Groq client."""
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        try:
            self.client = Groq(api_key=api_key)
        except TypeError as e:
            # Handle version compatibility issues
            logger.warning(f"Groq initialization with proxies failed: {e}, retrying...")
            self.client = Groq(api_key=api_key)
        
        self.approval_threshold = float(os.getenv("APPROVAL_THRESHOLD", 5000))
    
    def validate_expense(self, expense: dict) -> ExpenseValidation:
        """
        Validate and categorize an expense using Groq.
        
        Args:
            expense: Dict with 'description', 'amount', 'date', 'employee'
            
        Returns:
            ExpenseValidation object with reasoning
        """
        expense_id = expense.get("id", "UNKNOWN")
        description = expense.get("description", "")
        amount = expense.get("amount", 0)
        
        logger.info(f"Validating expense {expense_id}: {description} (${amount})")
        
        # Get AI categorization and reasoning
        category, reasoning, risk_flags = self._analyze_with_groq(description, amount)
        
        # Check policy limits
        limit = self.CATEGORY_LIMITS.get(category, self.approval_threshold)
        approved = amount <= limit and amount > 0
        
        if amount > limit:
            risk_flags.append(f"Amount exceeds {category} limit of ${limit}")
        
        # Flag high amounts for manual review
        requires_review = amount > self.approval_threshold or len(risk_flags) > 0
        
        result = ExpenseValidation(
            expense_id=expense_id,
            description=description,
            amount=amount,
            category=category,
            approved=approved,
            confidence=0.85 + (0.1 if not risk_flags else 0),  # Higher confidence if no flags
            reasoning=reasoning,
            risk_flags=risk_flags,
            requires_manual_review=requires_review
        )
        
        logger.info(f"Result: {category}, Approved: {approved}, Flags: {risk_flags}")
        return result
    
    def _analyze_with_groq(self, description: str, amount: float) -> tuple[str, str, list[str]]:
        """
        Use Groq to categorize and analyze expense.
        
        Returns:
            Tuple of (category, reasoning, risk_flags)
        """
        prompt = f"""Analyze this expense claim and respond with valid JSON only:

Expense Description: {description}
Amount: ${amount}

Available categories: {', '.join(self.VALID_CATEGORIES)}

Respond with ONLY a valid JSON object (no markdown, no code blocks):
{{
    "category": "one of the provided categories",
    "reasoning": "brief explanation in 1-2 sentences",
    "risk_flags": ["potential issue 1", "potential issue 2"]
}}

Risk flags should include: unusual descriptions, suspicious patterns, vague details, or personal items.
"""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                max_tokens=300,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response_text = message.choices[0].message.content.strip()
            
            # Clean up response (remove markdown if present)
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            result = json.loads(response_text)
            
            category = result.get("category", "Other")
            reasoning = result.get("reasoning", "Automatically categorized")
            risk_flags = result.get("risk_flags", [])
            
            # Validate category
            if category not in self.VALID_CATEGORIES:
                category = "Other"
            
            return category, reasoning, risk_flags
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response: {e}")
            return "Other", "Unable to analyze - using default categorization", ["Parse error"]
        except Exception as e:
            logger.error(f"Groq API error: {type(e).__name__}: {str(e)}")
            logger.debug(f"Full traceback:", exc_info=True)
            return "Other", f"Unable to analyze - {type(e).__name__}", ["API error"]
    
    def process_batch(self, expenses: list[dict]) -> dict:
        """
        Process multiple expenses and generate summary.
        
        Args:
            expenses: List of expense dicts
            
        Returns:
            Summary with approved/rejected counts and details
        """
        logger.info(f"Processing batch of {len(expenses)} expenses")
        
        results = []
        approved_count = 0
        flagged_count = 0
        total_amount = 0
        
        for expense in expenses:
            result = self.validate_expense(expense)
            results.append(asdict(result))
            
            if result.approved and not result.requires_manual_review:
                approved_count += 1
            elif result.requires_manual_review:
                flagged_count += 1
            
            total_amount += result.amount
        
        summary = {
            "total_expenses": len(expenses),
            "total_amount": total_amount,
            "approved_auto": approved_count,
            "flagged_for_review": flagged_count,
            "expenses": results
        }
        
        logger.info(f"Summary: {approved_count} approved, {flagged_count} flagged")
        return summary
