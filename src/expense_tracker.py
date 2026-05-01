"""
Expense Tracker Core Module

Production-ready expense tracking system with JSON persistence,
budget management, and CSV export capabilities.

Author: RodZilla (CTO, GrowBiz)
"""

import json
import csv
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class Expense:
    """Represents a single expense record.
    
    Attributes:
        id: Unique identifier (auto-generated)
        amount: Transaction amount in dollars
        merchant: Vendor or merchant name
        category: Expense category (e.g., 'groceries', 'utilities')
        date: Transaction date (ISO format YYYY-MM-DD)
        description: Optional description or note
        items: Optional list of purchased items
        payment_method: Payment method used (e.g., 'credit_card', 'cash')
        created_at: Timestamp when record was created
    """
    id: str
    amount: float
    merchant: str
    category: str
    date: str
    description: Optional[str] = None
    items: Optional[list] = None
    payment_method: Optional[str] = None
    created_at: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate expense data after initialization."""
        if self.amount < 0:
            raise ValueError(f"Expense amount cannot be negative: {self.amount}")
        if not self.merchant or not self.merchant.strip():
            raise ValueError("Merchant name cannot be empty")
        if not self.category or not self.category.strip():
            raise ValueError("Category cannot be empty")
        # Validate date format
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {self.date}. Expected YYYY-MM-DD")


class ExpenseTracker:
    """Core expense tracking engine with JSON persistence.
    
    Manages expense records, provides summary analytics,
    budget monitoring, and CSV export functionality.
    
    Attributes:
        data_file: Path to JSON storage file
        budget_limit: Monthly budget threshold in dollars
        expenses: In-memory list of Expense objects
    """
    
    def __init__(
        self,
        data_file: str = "expenses.json",
        budget_limit: float = 2000.0
    ) -> None:
        """Initialize the expense tracker.
        
        Args:
            data_file: Path to JSON storage file
            budget_limit: Monthly budget threshold in dollars
        """
        self.data_file: Path = Path(data_file)
        self.budget_limit: float = budget_limit
        self.expenses: list[Expense] = []
        self._load_data()
        logger.info(f"ExpenseTracker initialized | file={data_file} | budget=${budget_limit:,.2f}")
    
    def _generate_id(self) -> str:
        """Generate a unique expense ID based on timestamp."""
        return f"EXP-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')[:-3]}"
    
    def _load_data(self) -> None:
        """Load expenses from JSON file."""
        try:
            if self.data_file.exists():
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.expenses = [
                        Expense(**record) for record in data.get("expenses", [])
                    ]
                logger.info(f"Loaded {len(self.expenses)} expenses from {self.data_file}")
            else:
                logger.info(f"No existing data file found. Starting fresh.")
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted JSON file: {e}. Starting fresh.")
            self.expenses = []
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self.expenses = []
    
    def _save_data(self) -> None:
        """Persist expenses to JSON file."""
        try:
            data = {
                "expenses": [asdict(expense) for expense in self.expenses],
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "total_count": len(self.expenses),
                    "budget_limit": self.budget_limit
                }
            }
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Saved {len(self.expenses)} expenses to {self.data_file}")
        except PermissionError:
            logger.error(f"Permission denied writing to {self.data_file}")
            raise
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise
    
    def add_expense(
        self,
        amount: float,
        merchant: str,
        category: str,
        date: Optional[str] = None,
        description: Optional[str] = None,
        items: Optional[list] = None,
        payment_method: Optional[str] = None
    ) -> Expense:
        """Add a new expense record.
        
        Args:
            amount: Transaction amount in dollars
            merchant: Vendor or merchant name
            category: Expense category
            date: Transaction date (defaults to today)
            description: Optional description
            items: Optional list of purchased items
            payment_method: Optional payment method
            
        Returns:
            The created Expense object
            
        Raises:
            ValueError: If amount is negative or required fields are empty
        """
        try:
            expense = Expense(
                id=self._generate_id(),
                amount=float(amount),
                merchant=merchant.strip(),
                category=category.strip().lower(),
                date=date or datetime.now().strftime("%Y-%m-%d"),
                description=description,
                items=items or [],
                payment_method=payment_method,
                created_at=datetime.now().isoformat()
            )
            self.expenses.append(expense)
            self._save_data()
            logger.info(f"Added expense: {expense.id} | ${expense.amount:,.2f} | {expense.merchant}")
            return expense
        except Exception as e:
            logger.error(f"Failed to add expense: {e}")
            raise
    
    def get_expenses(
        self,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        merchant: Optional[str] = None
    ) -> list[Expense]:
        """Retrieve expenses with optional filtering.
        
        Args:
            category: Filter by category
            start_date: Filter from date (inclusive, YYYY-MM-DD)
            end_date: Filter to date (inclusive, YYYY-MM-DD)
            merchant: Filter by merchant name (partial match)
            
        Returns:
            List of matching Expense objects
        """
        results = self.expenses.copy()
        
        if category:
            results = [e for e in results if e.category.lower() == category.lower()]
        
        if start_date:
            results = [e for e in results if e.date >= start_date]
        
        if end_date:
            results = [e for e in results if e.date <= end_date]
        
        if merchant:
            results = [e for e in results if merchant.lower() in e.merchant.lower()]
        
        logger.info(f"Retrieved {len(results)} expenses (filtered from {len(self.expenses)})")
        return results
    
    def get_summary(
        self,
        period: str = "month",
        category: Optional[str] = None
    ) -> dict:
        """Generate expense summary for a given period.
        
        Args:
            period: Time period ('week', 'month', 'year', or 'all')
            category: Optional category filter
            
        Returns:
            Dictionary with summary statistics
        """
        today = datetime.now()
        
        if period == "week":
            start = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
        elif period == "month":
            start = today.replace(day=1).strftime("%Y-%m-%d")
        elif period == "year":
            start = today.replace(month=1, day=1).strftime("%Y-%m-%d")
        else:  # all
            start = "1900-01-01"
        
        expenses = self.get_expenses(start_date=start, category=category)
        
        if not expenses:
            return {
                "period": period,
                "total": 0.0,
                "count": 0,
                "average": 0.0,
                "by_category": {},
                "by_merchant": {},
                "start_date": start,
                "end_date": today.strftime("%Y-%m-%d")
            }
        
        total = sum(e.amount for e in expenses)
        
        # Group by category
        by_category = defaultdict(float)
        for e in expenses:
            by_category[e.category] += e.amount
        
        # Group by merchant
        by_merchant = defaultdict(float)
        for e in expenses:
            by_merchant[e.merchant] += e.amount
        
        summary = {
            "period": period,
            "total": round(total, 2),
            "count": len(expenses),
            "average": round(total / len(expenses), 2),
            "by_category": dict(by_category),
            "by_merchant": dict(by_merchant),
            "largest_expense": max(expenses, key=lambda e: e.amount).amount,
            "start_date": start,
            "end_date": today.strftime("%Y-%m-%d")
        }
        
        logger.info(f"Summary generated: {period} | ${summary['total']:,.2f} | {summary['count']} items")
        return summary
    
    def check_budget(self) -> dict:
        """Check current budget status and generate alerts.
        
        Returns:
            Dictionary with budget analysis and alert status
        """
        today = datetime.now()
        month_start = today.replace(day=1).strftime("%Y-%m-%d")
        
        monthly_expenses = self.get_expenses(start_date=month_start)
        total_spent = sum(e.amount for e in monthly_expenses)
        remaining = self.budget_limit - total_spent
        percentage_used = (total_spent / self.budget_limit * 100) if self.budget_limit > 0 else 0
        
        # Determine alert level
        if percentage_used >= 100:
            alert_level = "CRITICAL"
            alert_message = f"BUDGET EXCEEDED! Over by ${abs(remaining):,.2f}"
        elif percentage_used >= 90:
            alert_level = "WARNING"
            alert_message = f"Budget at {percentage_used:.1f}% - only ${remaining:,.2f} remaining"
        elif percentage_used >= 75:
            alert_level = "CAUTION"
            alert_message = f"Budget at {percentage_used:.1f}% - ${remaining:,.2f} left"
        else:
            alert_level = "OK"
            alert_message = f"Budget healthy: ${remaining:,.2f} remaining ({percentage_used:.1f}% used)"
        
        status = {
            "month": today.strftime("%Y-%m"),
            "budget_limit": self.budget_limit,
            "total_spent": round(total_spent, 2),
            "remaining": round(remaining, 2),
            "percentage_used": round(percentage_used, 2),
            "expense_count": len(monthly_expenses),
            "alert_level": alert_level,
            "alert_message": alert_message,
            "days_remaining": self._days_remaining_in_month()
        }
        
        logger.info(f"Budget check: {alert_level} | ${total_spent:,.2f}/${self.budget_limit:,.2f}")
        return status
    
    def _days_remaining_in_month(self) -> int:
        """Calculate days remaining in current month."""
        today = datetime.now()
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        return (next_month - today).days
    
    def export_csv(self, filepath: str, **filters) -> str:
        """Export expenses to CSV file.
        
        Args:
            filepath: Output CSV file path
            **filters: Optional filters (category, start_date, end_date, merchant)
            
        Returns:
            Path to the exported CSV file
        """
        expenses = self.get_expenses(**filters)
        
        if not expenses:
            logger.warning(f"No expenses to export with filters: {filters}")
            return ""
        
        fieldnames = [
            "id", "date", "merchant", "category", "amount",
            "description", "items", "payment_method", "created_at"
        ]
        
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for expense in expenses:
                    row = asdict(expense)
                    row["items"] = "; ".join(row["items"]) if row["items"] else ""
                    writer.writerow(row)
            
            logger.info(f"Exported {len(expenses)} expenses to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Export failed: {e}")
            raise
    
    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense by ID.
        
        Args:
            expense_id: The expense ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        original_count = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.id != expense_id]
        
        if len(self.expenses) < original_count:
            self._save_data()
            logger.info(f"Deleted expense: {expense_id}")
            return True
        
        logger.warning(f"Expense not found: {expense_id}")
        return False
    
    def update_budget(self, new_limit: float) -> None:
        """Update the monthly budget limit.
        
        Args:
            new_limit: New budget threshold in dollars
        """
        if new_limit < 0:
            raise ValueError("Budget limit cannot be negative")
        
        self.budget_limit = float(new_limit)
        self._save_data()
        logger.info(f"Budget updated to ${self.budget_limit:,.2f}")
