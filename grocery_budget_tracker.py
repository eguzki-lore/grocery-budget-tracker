#!/usr/bin/env python3
"""
Offline Grocery Budget Tracker
A tkinter-based application for tracking daily food expenses against a monthly budget.
Uses only Python standard library (tkinter, json, csv).
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import csv
from datetime import datetime, timedelta
import os

# Constants
MONTHLY_BUDGET = 300
DEFAULT_DATA_FILE = "grocery_budget_data.json"
CSV_DATA_FILE = "grocery_budget_data.csv"

# Days of the week
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fin", "Sat", "Sun"]
MEALS = ["Breakfast", "Lunch", "Dinner"]

class GroceryBudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Budget Tracker - $300 Monthly Budget")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f0f0f0")
        
        # Data structure: {date: {meal: {"food": str, "cost": float}}}
        self.data = self.load_data()

        # Calculate current month's spending
        self.current_month_spending = self.calculate_monthly_spending()
        
        # Initialize cell_data dictionary
        self.cell_data = {}

        # Set up the UI
        self.setup_menu()
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-s>", lambda e: self.save_csv())
        self.root.bind("<Control-j>", lambda e: self.save_json())
        self.root.bind("<Control-q>", lambda e: self.quit_app())
    
    def setup_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save as JSON", command=self.save_json, accelerator="Ctrl+J")
        file_menu.add_command(label="Save as CSV", command=self.save_csv, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit_app, accelerator="Ctrl+Q")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Budget Info", command=self.show_budget_info)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main UI components"""
        # Budget Status Frame
        budget_frame = ttk.Frame(self.root, padding="10")
        budget_frame.pack(fill=tk.X)
        
        budget_label = ttk.Label(
            budget_frame,
            text=f"Monthly Budget: ${MONTHLY_BUDGET}",
            font=("Arial", 14, "bold"),
            foreground="#333333"
        )
        budget_label.pack(side=tk.LEFT, padx=10)
        
        budget_var = tk.StringVar(value=f"Remaining: ${self.calculate_remaining()}")
        self.budget_var = budget_var  # Store as instance variable
        budget_display = ttk.Label(
            budget_frame,
            textvariable=budget_var,
            font=("Arial", 14, "bold"),
            foreground="#2e7d32" if self.calculate_remaining() >= 0 else "#c62828"
        )
        budget_display.pack(side=tk.LEFT, padx=10)
        
        spending_label = ttk.Label(
            budget_frame,
            text=f"Spent this month: ${self.current_month_spending:.2f}",
            font=("Arial", 12),
            foreground="#666666"
        )
        spending_label.pack(side=tk.RIGHT, padx=10)
        
        # Summary Buttons
        summary_frame = ttk.Frame(self.root, padding="5")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.summary_vars = {}
        for meal in MEALS:
            var = tk.StringVar(value="--")
            self.summary_vars[meal] = var
            ttk.Label(summary_frame, text=meal).pack(side=tk.LEFT, padx=5)
            ttk.Label(summary_frame, textvariable=var, width=15, font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(summary_frame, text="|").pack(side=tk.LEFT, padx=(5, 2))

        self.update_summary()
        
        # Main Grid Frame
        grid_frame = ttk.Frame(self.root, padding="5")
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create grid for 7 days x 3 meals
        # Each cell will have a frame for food name and cost
        for day_idx, day in enumerate(DAYS):
            for meal_idx, meal in enumerate(MEALS):
                # Create cell frame
                cell_frame = ttk.Frame(grid_frame)
                cell_frame.grid(row=meal_idx, column=day_idx, padx=2, pady=2, sticky="nsew")
                
                # Configure grid weights
                grid_frame.grid_rowconfigure(meal_idx, weight=1)
                grid_frame.grid_columnconfigure(day_idx, weight=1)
                
                # Food entry
                food_var = tk.StringVar()
                food_entry = ttk.Entry(cell_frame, textvariable=food_var, width=20)
                food_entry.pack(side=tk.TOP, fill=tk.X, padx=2)

                # Cost entry
                cost_var = tk.StringVar()
                cost_entry = ttk.Entry(cell_frame, textvariable=cost_var, width=12, foreground="#d32f2f")
                cost_entry.pack(side=tk.TOP, fill=tk.X, padx=2)

                # Store references for updates
                self.cell_data[(day_idx, meal_idx)] = {
                    "food_var": food_var,
                    "cost_var": cost_var,
                    "food_entry": food_entry,
                    "cost_entry": cost_entry
                }
    
    def get_current_date_str(self):
        """Get today's date as string"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(DEFAULT_DATA_FILE):
            try:
                with open(DEFAULT_DATA_FILE, 'r') as f:
                    data = json.load(f)
                # Validate data structure - only keep valid entries
                valid_data = {}
                for date_str, day_meals in data.items():
                    if isinstance(day_meals, dict):
                        valid_day_meals = {}
                        for meal, info in day_meals.items():
                            if isinstance(info, dict):
                                valid_day_meals[meal] = info
                        if valid_day_meals:
                            valid_data[date_str] = valid_day_meals
                return valid_data
            except (json.JSONDecodeError, IOError, TypeError):
                return {}
        return {}
    
    def save_data(self):
        """Save data to JSON file with validation"""
        try:
            # Validate data before saving
            valid_data = {}
            for date_str, day_meals in self.data.items():
                if isinstance(date_str, str) and isinstance(day_meals, dict):
                    valid_day_meals = {}
                    for meal, info in day_meals.items():
                        if isinstance(meal, str) and isinstance(info, dict):
                            valid_day_meals[meal] = info
                    if valid_day_meals:
                        valid_data[date_str] = valid_day_meals
            
            # Only save if we have valid data
            if valid_data:
                with open(DEFAULT_DATA_FILE, 'w') as f:
                    json.dump(valid_data, f, indent=2)
            else:
                # Clear the file if no valid data
                with open(DEFAULT_DATA_FILE, 'w') as f:
                    f.write("{}")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    def save_csv(self):
        """Save data to CSV file"""
        try:
            with open(CSV_DATA_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Day", "Meal", "Food", "Cost"])
                
                for date_str, day_meals in self.data.items():
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    day_name = date_obj.strftime("%A")
                    
                    for meal, info in day_meals.items():
                        if info:
                            writer.writerow([date_str, day_name, meal, info["food"], info["cost"]])
            
            messagebox.showinfo("Success", f"Data saved to {CSV_DATA_FILE}")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save CSV: {e}")
    
    def save_json(self, filename=None):
        """Save data to JSON file"""
        if filename is None:
            filename = DEFAULT_DATA_FILE
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.data, f, indent=2)
            messagebox.showinfo("Success", f"Data saved to {filename}")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save JSON: {e}")
    
    def calculate_remaining(self):
        """Calculate remaining budget for current month"""
        return MONTHLY_BUDGET - self.current_month_spending
    
    def calculate_monthly_spending(self):
        """Calculate total spending for current month"""
        current_month = datetime.now().strftime("%Y-%m")
        total = 0
        
        for date_str, day_meals in self.data.items():
            if date_str.startswith(current_month):
                for meal, info in day_meals.items():
                    if info and info.get("cost"):
                        total += float(info["cost"])
        
        return total
    
    def calculate_meal_total(self, meal):
        """Calculate total cost for a specific meal across all days"""
        total = 0

        for date_str, day_meals in self.data.items():
            if day_meals.get(meal) and day_meals[meal].get("cost"):
                total += float(day_meals[meal]["cost"])

        return total

    def update_summary(self):
        """Update summary labels and budget display"""
        for meal in MEALS:
            total = self.calculate_meal_total(meal)
            var = self.summary_vars[meal]
            var.set(f"${total:.2f}")
        remaining = self.calculate_remaining()
        # Update the existing budget_var StringVar
        self.budget_var.set(f"Remaining: ${remaining:.2f}")
    
    def get_cell_data(self, day_idx, meal_idx):
        """Get food and cost for a cell"""
        key = (day_idx, meal_idx)
        if key in self.cell_data and self.data.get(self.date_key):
            date_str = self.date_key
            day_meals = self.data.get(date_str, {})
            meal_data = day_meals.get(MEALS[meal_idx])
            if meal_data:
                return meal_data.get("food", ""), meal_data.get("cost", "")
        return "", ""
    
    def update_cell(self, day_idx, meal_idx, food="", cost=""):
        """Update a cell with new food and cost"""
        key = (day_idx, meal_idx)
        if key in self.cell_data:
            self.cell_data[key]["food_var"].set(food)
            self.cell_data[key]["cost_var"].set(cost)

        # Update internal data with validation
        date_str = self.date_key()
        if not isinstance(date_str, str) or len(date_str) != 10:
            date_str = self.date_key()  # Retry with fresh call
        
        # Only add the date key if it doesn't exist or is empty
        if date_str not in self.data or not isinstance(self.data.get(date_str), dict):
            self.data[date_str] = {}
        
        # Only add the meal key if it doesn't exist or is empty
        meal_name = MEALS[meal_idx]
        if meal_name not in self.data[date_str] or not isinstance(self.data[date_str].get(meal_name), dict):
            self.data[date_str][meal_name] = {"food": "", "cost": "", "date": date_str}

        # Only update if the meal entry is a valid dict
        if isinstance(self.data[date_str].get(meal_name), dict):
            self.data[date_str][meal_name]["food"] = food
            self.data[date_str][meal_name]["cost"] = cost
            self.data[date_str][meal_name]["date"] = date_str

        # Auto-save
        self.save_data()
        self.update_summary()
    
    def date_key(self):
        """Get current date key"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def add_row(self, day_idx, meal_idx):
        """Add a row for food items"""
        # This creates a frame with label and entry
        cell_frame = self.cell_data[(day_idx, meal_idx)]
        
        # Food entry frame
        food_frame = ttk.Frame(cell_frame["food_label"].parent)
        food_frame.pack(fill=tk.X, padx=5, pady=2)
        
        food_var = tk.StringVar()
        food_entry = ttk.Entry(food_frame, textvariable=food_var, width=25)
        food_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.cell_data[(day_idx, meal_idx)]["food_entry"] = food_entry
        self.cell_data[(day_idx, meal_idx)]["food_var"] = food_var
        
        # Cost entry frame
        cost_frame = ttk.Frame(cell_frame["food_label"].parent)
        cost_frame.pack(fill=tk.X, padx=5, pady=2)
        
        cost_var = tk.StringVar()
        cost_entry = ttk.Entry(cost_frame, textvariable=cost_var, width=10)
        cost_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.cell_data[(day_idx, meal_idx)]["cost_entry"] = cost_entry
        self.cell_data[(day_idx, meal_idx)]["cost_var"] = cost_var
        
        # Bind entry changes
        food_var.trace_add("write", lambda *args: self.on_change(day_idx, meal_idx))
        cost_var.trace_add("write", lambda *args: self.on_change(day_idx, meal_idx))
    
    def on_change(self, day_idx, meal_idx):
        """Handle cell change event"""
        food = self.cell_data[(day_idx, meal_idx)]["food_var"].get()
        cost = self.cell_data[(day_idx, meal_idx)]["cost_var"].get()
        self.update_cell(day_idx, meal_idx, food, cost)
    
    def quit_app(self):
        """Quit the application"""
        response = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit? Unsaved changes will be lost.")
        if response:
            self.root.destroy()
    
    def show_budget_info(self):
        """Show budget information dialog"""
        info = """
Grocery Budget Tracker Information
===================================

Monthly Budget: $300.00
Days: Monday - Sunday
Meals: Breakfast, Lunch, Dinner

Features:
- Track daily food expenses
- View spending summary by meal type
- Save data as JSON or CSV
- Automatic calculation of remaining budget
- Data persists across sessions

Keyboard Shortcuts:
Ctrl+J: Save as JSON
Ctrl+S: Save as CSV
Ctrl+Q: Quit Application
        """
        messagebox.showinfo("Budget Info", info)
    
    def show_about(self):
        """Show about dialog"""
        about = """
Grocery Budget Tracker v1.0
============================

A simple offline grocery budget tracking application.

Built with Python standard library:
- tkinter (GUI)
- json (Data storage)
- csv (CSV export)

No internet connection required!

Author: Auto-generated
        """
        messagebox.showinfo("About", about)


def main():
    root = tk.Tk()
    app = GroceryBudgetTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
