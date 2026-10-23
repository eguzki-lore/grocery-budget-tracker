# Grocery Budget Tracker

A simple offline grocery budget tracking application built entirely with Python's standard library. Track your monthly grocery spending against a $300 budget with a clean 2D matrix interface.

## 🎯 Project Goals

- Create a simple, intuitive grocery budget tracking application
- Enable users to track daily food expenses across 7 days and 3 meals
- Provide real-time budget visualization and spending summaries
- Implement offline-first design for privacy and reliability
- Document all developments in a centralized README
- Integrate with GitHub for version control and team collaboration

## ✨ Features

### Core Functionality
- **Budget Tracking**: Track your monthly grocery spending against a $300 budget
- **2D Matrix Grid Layout**: 7 days (Mon-Sun) × 3 meals (Breakfast, Lunch, Dinner)
- **Real-time Summary**: View spending summary by meal type with dynamic updates
- **Data Persistence**: Save and load data in JSON or CSV format
- **Offline Operation**: Works without internet connection
- **Keyboard Shortcuts**: Save and quit with keyboard shortcuts

### User Interface
- Clean, intuitive grid-based interface
- Color-coded budget status (green = within budget, red = over budget)
- Real-time budget calculation and display
- Interactive entry fields for food items and costs

## 📋 Requirements

- **Python 3.x** (requires Python 3.4+ for tkinter compatibility)
- **No external packages** required (uses only `tkinter`, `json`, `csv` from standard library)

## 📦 Installation

### Prerequisites
- Python 3.x installed on your system

### Quick Start
No installation required! Just run the script directly:

```bash
python grocery-budget-tracker.py
```

## 🚀 Usage

### Running the Application

1. **Launch the application:**
   ```bash
   python grocery-budget-tracker.py
   ```

2. **Track your expenses:**
   - Enter food names in the breakfast, lunch, and dinner cells
   - Enter costs in the format: `5.99` (decimal with two decimal places)
   - Data is automatically saved when you make changes

3. **Save your data:**
   - **Ctrl+J**: Save as JSON (recommended for data integrity)
   - **Ctrl+S**: Save as CSV (easy to open in Excel/Google Sheets)

4. **View your budget:**
   - Remaining budget is shown at the top (green = good, red = over budget)
   - Spending summary shows total per meal type
   - Monthly total is displayed

## 📁 File Structure

```
grocery-budget-tracker.py  # Main application script
grocery_budget_data.json   # Auto-saved JSON data (created on first use)
grocery_budget_data.csv    # CSV export (created when you save as CSV)
README.md                  # Project documentation
DEVELOPMENT_LOG.md        # Detailed development progress and issues
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+J | Save as JSON |
| Ctrl+S | Save as CSV |
| Ctrl+Q | Quit Application |

## 🎨 Budget Display

- **Green text**: You're within budget
- **Red text**: You've exceeded the $300 budget

## 💾 Data Format

### JSON (Recommended)
```json
{
  "2026-10-22": {
    "Breakfast": {
      "food": "Oatmeal",
      "cost": "4.50",
      "date": "2026-10-22"
    },
    "Lunch": {
      "food": "Sandwich",
      "cost": "6.25",
      "date": "2026-10-22"
    },
    "Dinner": {
      "food": "Pasta",
      "cost": "12.00",
      "date": "2026-10-22"
    }
  }
}
```

### CSV
```csv
Date,Day,Meal,Food,Cost
2026-10-22,Wednesday,Breakfast,Oatmeal,4.50
2026-10-22,Wednesday,Lunch,Sandwich,6.25
2026-10-22,Wednesday,Dinner,Pasta,12.00
```

## 🐙 GitHub Integration

### Current Status: IN PROGRESS

The project is being set up for GitHub version control and collaboration.

### Repository Setup Steps

1. **Create a GitHub repository** (if not already created):
   - Go to https://github.com/new
   - Create a new repository (public or private)
   - Note the repository name and owner

2. **Initialize git repository in your project folder:**
   ```bash
   cd C:\Users\Cano\qwen-workspace
   git init
   ```

3. **Configure git (if not already configured):**
   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

4. **Add files to staging:**
   ```bash
   git add .
   ```

5. **Create initial commit:**
   ```bash
   git commit -m "Initial commit: Grocery Budget Tracker application"
   ```

6. **Link to remote repository:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

7. **Push to GitHub:**
   ```bash
   git branch -M main
   git push -u origin main
   ```

### GitHub Features to Enable
- ✅ Issue tracking for bug reports and feature requests
- ✅ Pull requests for code review
- ✅ Git branches for feature development
- ✅ GitHub Actions for automated testing (future)
- ✅ GitHub Pages for documentation (future)

## 📈 Development Progress

### ✅ Resolved Issues

#### Issue #1: 2D Matrix Editable Interface
**Status**: RESOLVED

**Problem**: The application needed an editable 2D matrix interface for the 7 days × 3 meals grid. The initial implementation used non-editable widgets.

**Solution Implemented**:
- Implemented `Entry` widgets for all grid cells instead of `Label` widgets
- Made all 21 cells (7 days × 3 meals) editable for both food names and costs
- Added proper event handling for cell focus and input
- Ensured keyboard navigation works smoothly across the grid

#### Issue #2: update_summary() Method Fix
**Status**: RESOLVED

**Problem**: The `update_summary()` method was not properly updating existing summary labels when new data was entered. The method was creating new label widgets instead of updating the existing ones.

**Solution Implemented**:
- Modified `update_summary()` to check if summary labels already exist before creating new ones
- Added proper event binding to trigger summary updates on data change
- Implemented incremental cost tracking for real-time updates
- Fixed the cost extraction logic to properly parse values from grid cells

## 🔍 Known Issues

### Current Known Issues

1. **Cost Entry Color is Hardcoded Red**
   - When entering a cost value, the entry field is hardcoded to red color
   - **Recommendation**: Add a configurable color variable or make it context-aware (e.g., green if within budget, red if over)

2. **No Input Validation for Cost Entries**
   - Users can enter any text in the cost fields, including invalid formats
   - **Recommendation**: Add validation to ensure cost entries are numeric values with proper decimal formatting

3. **Single Data File Could Use Database Backend**
   - All data is stored in a single JSON file
   - **Recommendation**: For larger datasets, consider migrating to SQLite or another database backend for better performance and data integrity

## 💡 Technical Critiques

### 1. Code Organization
**Issue**: The `create_widgets()` method is too large and contains multiple unrelated responsibilities.

**Recommendation**: Refactor into smaller, focused methods:
- `create_grid()` - Setup the main grid layout
- `create_summary_labels()` - Create the summary display area
- `create_menu_bar()` - Create the menu bar and shortcuts
- `create_data_loaders()` - Create file load/save buttons

### 2. Error Handling
**Issue**: No error handling for corrupted data files.

**Recommendation**: Add comprehensive error handling:
- Try-except blocks around `load_data()`
- Informative error messages to the user
- Fallback to empty state if data file is corrupted
- Log errors to a separate file for debugging

### 3. Input Validation
**Issue**: No validation for cost entries.

**Recommendation**: Implement validation:
- Check that cost values are numeric
- Ensure decimal format (e.g., "5.99")
- Prevent negative values
- Provide user feedback for invalid input

### 4. Data Format Validation
**Issue**: The `load_data()` method doesn't validate the date format.

**Recommendation**: Add date format validation:
- Validate dates match YYYY-MM-DD format
- Handle invalid date formats gracefully
- Provide clear error messages for corrupted data

### 5. Budget Calculation Logic
**Issue**: The budget calculation doesn't handle edge cases well.

**Recommendation**: Improve the logic:
- Handle empty/zero costs properly
- Add tolerance for floating-point arithmetic
- Consider rounding to 2 decimal places for display

### 6. User Feedback
**Issue**: Limited user feedback when operations fail.

**Recommendation**: Add feedback mechanisms:
- Status bar for operation feedback
- Toast notifications for actions
- Confirmation dialogs for destructive actions

## 🔮 Future Enhancements

### Short-term (Next Sprint)
- [ ] Implement input validation for cost entries
- [ ] Add error handling for corrupted data files
- [ ] Make cost entry color context-aware
- [ ] Add date format validation in `load_data()`
- [ ] Implement logging for debugging
- [ ] Add unit tests with pytest

### Medium-term (This Quarter)
- [ ] Refactor large methods into smaller focused functions
- [ ] Implement SQLite database backend option
- [ ] Add data export to Excel format
- [ ] Implement data import functionality
- [ ] Add budget goal setting (customizable budget amount)
- [ ] Implement data visualization (charts/graphs)

### Long-term (Future Versions)
- [ ] Multi-user support for shared household tracking
- [ ] Cloud sync with GitHub repository
- [ ] Mobile app version (React Native or Flutter)
- [ ] Recipe integration with cost estimation
- [ ] Barcode scanner integration for grocery items
- [ ] Budget analytics and trends over time
- [ ] Weekly/monthly summary reports
- [ ] Integration with grocery delivery services

## 🧪 Testing

### Current Testing Status
- ✅ Manual testing completed for core functionality
- ✅ Grid layout and data entry working correctly
- ✅ Save/load functionality verified
- ✅ Budget calculation verified

### Planned Testing
- [ ] Unit tests with pytest
- [ ] Integration tests for data persistence
- [ ] Edge case testing (empty entries, invalid inputs)
- [ ] Performance testing with large datasets

### Running Tests
```bash
pytest
```

## 📖 License

MIT License - Free to use and modify.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Use PEP 8 style guide
- Include docstrings for all functions
- Add comments for complex logic
- Write meaningful commit messages

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the [Development Log](DEVELOPMENT_LOG.md) for recent changes
- Review the [Known Issues](#-known-issues) section

## 🙏 Acknowledgments

- Built with Python 3.x standard library
- Inspired by personal finance tracking needs
- Developed with open-source principles in mind

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-10-22 | Initial release with basic grid layout and budget tracking |
| 0.2.0 | 2026-10-22 | Resolved Issue #1: Implemented 2D Matrix Editable Interface |
| 0.3.0 | 2026-10-22 | Resolved Issue #2: Fixed update_summary() method to properly update existing labels |
| 0.4.0 | TBD | GitHub integration (IN PROGRESS) |

## 📄 Development Log

For detailed information about recent development activities, resolved issues, and technical critiques, see [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md).

---

Enjoy tracking your grocery expenses! 🛒💰
