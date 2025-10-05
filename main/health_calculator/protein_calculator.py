import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shared import *

class ProteinCalculator:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()
    
    def setup_ui(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.parent_frame, text="Protein Calculation Input", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Weight input
        weight_row = ttk.Frame(input_frame)
        weight_row.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(weight_row, text="Your Weight:").pack(side=tk.LEFT)
        
        self.weight_var = tk.DoubleVar(value=70)
        weight_entry = ttk.Entry(weight_row, textvariable=self.weight_var, width=10)
        weight_entry.pack(side=tk.LEFT, padx=(8, 5))
        
        self.weight_unit_var = tk.StringVar(value="kg")
        weight_unit_combobox = ttk.Combobox(weight_row, textvariable=self.weight_unit_var, 
                                           values=["kg", "lbs"], width=6, state="readonly")
        weight_unit_combobox.pack(side=tk.LEFT, padx=(5, 15))
        
        # Activity level
        activity_row = ttk.Frame(input_frame)
        activity_row.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(activity_row, text="Activity Level:").pack(side=tk.LEFT)
        
        self.activity_var = tk.StringVar(value="Moderate Exercise")
        activity_combobox = ttk.Combobox(activity_row, textvariable=self.activity_var,
                                        values=["Sedentary", "Light Exercise", "Moderate Exercise", 
                                               "Intense Exercise", "Athlete"], width=15, state="readonly")
        activity_combobox.pack(side=tk.LEFT, padx=(8, 15))
        
        # Goal
        goal_row = ttk.Frame(input_frame)
        goal_row.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(goal_row, text="Fitness Goal:").pack(side=tk.LEFT)
        
        self.goal_var = tk.StringVar(value="Muscle Building")
        goal_combobox = ttk.Combobox(goal_row, textvariable=self.goal_var,
                                    values=["Maintenance", "Muscle Building", "Fat Loss"], width=15, state="readonly")
        goal_combobox.pack(side=tk.LEFT, padx=(8, 15))
        
        # Calculate button
        calc_btn = ttk.Button(input_frame, text="Calculate Protein Needs",
                             command=self.calculate_protein_needs)
        calc_btn.pack(pady=(10, 0))
        
        # Results frame
        self.results_frame = ttk.LabelFrame(self.parent_frame, text="Protein Recommendations", padding="10")
        self.results_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.setup_results()
        
        # Chart frame
        self.chart_frame = ttk.LabelFrame(self.parent_frame, text="Protein Distribution", padding="5")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.chart_frame)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        self.result_label = ttk.Label(self.results_frame, 
                                    text="Enter your weight and click Calculate", 
                                    font=('Arial', 10),
                                    foreground='blue')
        self.result_label.pack(pady=8)
    
    def calculate_protein_needs(self):
        try:
            weight = self.weight_var.get()
            unit = self.weight_unit_var.get()
            activity = self.activity_var.get()
            goal = self.goal_var.get()
            
            # Convert to kg if needed
            if unit == "lbs":
                weight_kg = weight * 0.453592
            else:
                weight_kg = weight
            
            # Calculate protein needs based on activity and goal
            protein_needs = self.calculate_protein_requirements(weight_kg, activity, goal)
            
            self.update_results(weight, unit, protein_needs, activity, goal)
            self.update_chart(protein_needs, goal)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid weight!")
    
    def calculate_protein_requirements(self, weight_kg, activity, goal):
        # Base protein requirements (grams per kg)
        base_protein = {
            "Sedentary": 0.8,
            "Light Exercise": 1.0,
            "Moderate Exercise": 1.2,
            "Intense Exercise": 1.6,
            "Athlete": 2.0
        }
        
        # Adjust for goals
        goal_multiplier = {
            "Maintenance": 1.0,
            "Muscle Building": 1.2,
            "Fat Loss": 1.1
        }
        
        protein_per_kg = base_protein[activity] * goal_multiplier[goal]
        daily_protein = weight_kg * protein_per_kg
        
        return {
            "daily_protein": daily_protein,
            "protein_per_kg": protein_per_kg,
            "weight_kg": weight_kg
        }
    
    def update_results(self, weight, unit, protein_data, activity, goal):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        daily_protein = protein_data["daily_protein"]
        protein_per_kg = protein_data["protein_per_kg"]
        
        result_text = f"""• Your Weight: {weight} {unit}
• Activity Level: {activity}
• Fitness Goal: {goal}
• Recommended Daily Protein: {daily_protein:.1f}g
• Protein Intake: {protein_per_kg:.1f}g per kg
• Meal Distribution (4 meals): {daily_protein/4:.1f}g per meal"""
        
        result_label = ttk.Label(self.results_frame, text=result_text,
                               font=('Arial', 10), foreground='darkgreen')
        result_label.pack(pady=8)
    
    def update_chart(self, protein_data, goal):
        self.ax.clear()
        
        daily_protein = protein_data["daily_protein"]
        
        # Create meal distribution data
        meals = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
        protein_per_meal = daily_protein / 4
        
        # Colors based on goal
        colors = {
            "Maintenance": ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
            "Muscle Building": ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'],
            "Fat Loss": ['#ff9ff3', '#f368e0', '#ff9f43', '#ee5253']
        }
        
        color_set = colors.get(goal, colors["Maintenance"])
        
        # Create pie chart
        wedges, texts, autotexts = self.ax.pie([protein_per_meal] * 4, 
                                              labels=meals, 
                                              colors=color_set,
                                              autopct='%1.1fg',
                                              startangle=90)
        
        # Style the chart
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        self.ax.set_title(f'Daily Protein Distribution: {daily_protein:.1f}g total\n({goal})', 
                         fontsize=11, fontweight='bold', pad=20)
        
        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()