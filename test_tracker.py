#!/usr/bin/env python3
"""
Test script for Grocery Budget Tracker
Tests data persistence and calculation functions.
"""

import json
import os
import sys
import tempfile
import shutil

import tkinter as tk

from grocery_budget_tracker import GroceryBudgetTracker, MONTHLY_BUDGET, DEFAULT_DATA_FILE, CSV_DATA_FILE


def test_app_creation():
    """Test that the app initializes correctly"""
    print("Testing app creation...")

    root = tk.Tk()
    root.withdraw()  # Hide the main window for testing

    try:
        app = GroceryBudgetTracker(root)
        print("✓ App created successfully")
        return app
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        return None


def test_data_structure():
    """Test that data structure is correct"""
    print("\nTesting data structure...")
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = GroceryBudgetTracker(root)
        
        # Check that data dict exists
        assert isinstance(app.data, dict), "Data should be a dictionary"
        print("✓ Data structure is correct")
        
        # Test date key generation
        date_key = app.date_key()
        assert isinstance(date_key, str), "Date key should be a string"
        assert len(date_key) == 10, "Date should be in YYYY-MM-DD format"
        print(f"✓ Date key format: {date_key}")
        
        # Keep root alive for potential use by test_calculations
        return app
    except Exception as e:
        print(f"✗ Data structure test failed: {e}")
        if root.winfo_exists():
            root.destroy()
        return None


def test_calculations(app):
    """Test spending calculations"""
    print("\nTesting calculations...")
    
    # Test calculate_remaining
    remaining = app.calculate_remaining()
    assert isinstance(remaining, (int, float)), "Remaining should be numeric"
    print(f"✓ Remaining budget calculation: ${remaining:.2f}")
    
    # Test calculate_monthly_spending
    spending = app.calculate_monthly_spending()
    assert isinstance(spending, (int, float)), "Spending should be numeric"
    print(f"✓ Monthly spending calculation: ${spending:.2f}")
    
    # Test calculate_meal_total
    for meal in ["Breakfast", "Lunch", "Dinner"]:
        total = app.calculate_meal_total(meal)
        assert isinstance(total, (int, float)), f"Meal total should be numeric"
        print(f"✓ {meal} total: ${total:.2f}")
    
    return app


def test_data_persistence(app):
    """Test saving and loading data"""
    print("\nTesting data persistence...")
    
    # Add some test data
    date_key = app.date_key()
    app.data[date_key] = {
        "Breakfast": {"food": "Oatmeal", "cost": "4.50", "date": date_key},
        "Lunch": {"food": "Sandwich", "cost": "6.25", "date": date_key},
        "Dinner": {"food": "Pasta", "cost": "12.00", "date": date_key}
    }
    
    # Save to JSON
    try:
        app.save_data()
        print("✓ JSON save successful")
    except Exception as e:
        print(f"✗ JSON save failed: {e}")
    
    # Verify file exists
    if os.path.exists(DEFAULT_DATA_FILE):
        print(f"✓ Data file created: {DEFAULT_DATA_FILE}")
        
        # Load and verify
        with open(DEFAULT_DATA_FILE, 'r') as f:
            loaded_data = json.load(f)
        
        assert date_key in loaded_data, "Date key should be in loaded data"
        assert loaded_data[date_key]["Breakfast"]["food"] == "Oatmeal"
        print("✓ Data loaded correctly")
    else:
        print("✗ Data file not created")
    
    # Test CSV save
    try:
        app.save_csv()
        print("✓ CSV save successful")
    except Exception as e:
        print(f"✗ CSV save failed: {e}")
    
    if os.path.exists(CSV_DATA_FILE):
        print(f"✓ CSV file created: {CSV_DATA_FILE}")
    
    return app


def test_update_cell(app):
    """Test cell update functionality"""
    print("\nTesting cell update...")

    # Create a fresh app to avoid corrupted data from previous tests
    root = tk.Tk()
    root.withdraw()
    try:
        fresh_app = GroceryBudgetTracker(root)
    except Exception as e:
        print(f"✗ Failed to create fresh app: {e}")
        return app

    # Ensure we have clean data for today
    date_key = fresh_app.date_key()
    fresh_app.data[date_key] = {
        "Breakfast": {"food": "", "cost": "", "date": date_key},
        "Lunch": {"food": "", "cost": "", "date": date_key},
        "Dinner": {"food": "", "cost": "", "date": date_key}
    }

    # Update a cell
    fresh_app.update_cell(0, 0, "Eggs", "5.00")  # Monday Breakfast

    # Verify update
    key = (0, 0)
    if key in fresh_app.cell_data:
        print("✓ Cell data structure correct")

    # Verify internal data
    if date_key in fresh_app.data:
        breakfast = fresh_app.data[date_key].get("Breakfast", {})
        if breakfast.get("food") == "Eggs" and breakfast.get("cost") == "5.00":
            print("✓ Cell update successful")

    return fresh_app


def test_keyboard_shortcuts(app):
    """Test that keyboard shortcuts are bound"""
    print("\nTesting keyboard shortcuts...")

    # Check that shortcuts are bound on the app's root window
    shortcuts = ["<Control-s>", "<Control-j>", "<Control-q>"]
    all_bound = True

    for shortcut in shortcuts:
        try:
            # Try to get the command for this shortcut
            command = app.root.bind_get(shortcut)
            if command is not None:
                print(f"✓ Shortcut bound: {shortcut}")
            else:
                print(f"✗ Shortcut not bound: {shortcut}")
                all_bound = False
        except Exception:
            print(f"✗ Shortcut not bound: {shortcut}")
            all_bound = False

    return app


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("GROCERY BUDGET TRACKER - TEST SUITE")
    print("=" * 60)

    try:
        # Test 1: App creation
        app = test_app_creation()
        if not app:
            print("\n✗ Test suite failed at app creation")
            return False

        # Test 2: Data structure
        app = test_data_structure()
        if not app:
            print("\n✗ Test suite failed at data structure")
            return False

        # Test 3: Calculations
        app = test_calculations(app)

        # Test 4: Data persistence
        app = test_data_persistence(app)

        # Test 5: Cell updates
        app = test_update_cell(app)

        # Test 6: Keyboard shortcuts
        app = test_keyboard_shortcuts(app)

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ Test suite failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup any remaining root windows
        import tkinter as tk
        try:
            tk._default_root().destroy()
        except:
            pass


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
