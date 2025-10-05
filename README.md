🏥 Health Calculator Suite

A comprehensive desktop application that helps you manage your health through three powerful calculators: Caffeine Impact, Protein Requirements, and Meal Planning.

## ✨ Features

### ☕ Caffeine Calculator
- **Sleep Impact Analysis**: Calculate how long caffeine will affect your sleep based on dosage
- **Visual Decay Timeline**: Interactive graph showing caffeine levels over time
- **Safety Warnings**: Automatic alerts for dangerous or lethal doses
- **Quick Doses**: One-click buttons for common caffeine amounts (coffee, energy drinks, etc.)
- **Unit Conversion**: Support for both grams and milligrams

### 💪 Protein Calculator  
- **Personalized Recommendations**: Calculate daily protein needs based on your specific profile
- **Activity-Based Calculation**: Different recommendations for sedentary, moderate exercise, intense training, and athletes
- **Goal-Oriented**: Customized for maintenance, muscle building, or fat loss goals
- **Visual Distribution**: Pie chart showing protein distribution across meals
- **Weight Unit Support**: Works with both kilograms (kg) and pounds (lbs)

### 🍽️ Meal Planner
- **Personalized Meal Plans**: Generate daily meal plans based on your weight and preferences
- **Diet Flexibility**: Support for Mixed, Animal-Based, Plant-Based, and Vegetarian diets
- **Smart Nutrition**: Automatically calculates protein and calories for each meal
- **Visual Breakdown**: Bar chart showing protein sources across meals
- **Randomization**: Generate different meal combinations each time
- **Detailed Reporting**: Complete nutrition breakdown with serving sizes

## 🛠️ Installation Requirements

### Required Software
1. **Python 3.8 or higher** - The programming language
2. **pip package manager** - Comes with Python
3. **Internet connection** - For downloading packages

### Required Python Packages
The application needs these packages to run:
- `matplotlib` - For creating graphs and charts
- `numpy` - For mathematical calculations
- `tkinter` - For the user interface (usually pre-installed)

## 📥 Step-by-Step Installation Guide

### Step 1: Install Python
1. Go to [python.org](https://www.python.org/downloads/)
2. Download Python 3.8 or newer
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Complete the installation

### Step 2: Download Project Files
1. Create a folder called `health_calculator`
2. Download these 5 files into the folder:
   - `main.py`
   - `caffeine_calculator.py` 
   - `protein_calculator.py`
   - `meal_planner.py`
   - `shared.py`

### Step 3: Install Required Packages
Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
pip install matplotlib numpy
```

**Note about tkinter**: 
- Usually comes pre-installed with Python
- If you get tkinter errors, install it based on your OS:
  - **Windows**: Reinstall Python and check "tcl/tk" option
  - **Mac**: `brew install python-tk`
  - **Linux**: `sudo apt-get install python3-tk`

### Step 4: Verify Installation
Check if everything installed correctly:
```bash
python --version
pip list
```

You should see Python version and the installed packages.

### Step 5: Run the Application
```bash
cd health_calculator
python main.py
```

## 🚀 How to Use the Application

### Starting the App
1. Open command prompt/terminal in the project folder
2. Type `python main.py` and press Enter
3. The application window will open with three calculator options

### Using Caffeine Calculator
1. Click "☕ Caffeine Calculator" button
2. Enter caffeine amount (e.g., 0.2 for 200mg)
3. Select grams or milligrams
4. Use quick buttons or type custom amount
5. Click "Calculate Sleep Impact"
6. View results and decay graph

### Using Protein Calculator
1. Click "💪 Protein Calculator" button  
2. Enter your weight
3. Select kg or lbs
4. Choose activity level
5. Select fitness goal
6. Click "Calculate Protein Needs"
7. View recommendations and meal distribution chart

### Using Meal Planner
1. Click "🍽️ Meal Planner" button
2. Enter your weight
3. Choose diet preference
4. Select meals per day (3-6)
5. Click "Generate Meal Plan" or "Random Plan"
6. View detailed meal breakdown with nutrition info

## 📦 Creating EXE File (Optional)

### To create a standalone executable:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build EXE**:
   ```bash
   pyinstaller --onefile --windowed --name "HealthCalculator" main.py
   ```

3. **Find your EXE**:
   - Look in the `dist` folder
   - File: `HealthCalculator.exe`
   - This runs without Python installed!
