import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import numpy as np
from shared import *

class MealPlanner:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()
    
    def setup_ui(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.parent_frame, text="Meal Planner Input", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Weight input
        weight_row = ttk.Frame(input_frame)
        weight_row.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(weight_row, text="Your Weight:").pack(side=tk.LEFT)
        
        self.weight_var = tk.DoubleVar(value=68)
        weight_entry = ttk.Entry(weight_row, textvariable=self.weight_var, width=10)
        weight_entry.pack(side=tk.LEFT, padx=(8, 5))
        
        self.weight_unit_var = tk.StringVar(value="kg")
        weight_unit_combobox = ttk.Combobox(weight_row, textvariable=self.weight_unit_var, 
                                           values=["kg", "lbs"], width=6, state="readonly")
        weight_unit_combobox.pack(side=tk.LEFT, padx=(5, 15))
        
        # Diet Preference
        diet_row = ttk.Frame(input_frame)
        diet_row.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(diet_row, text="Diet Preference:").pack(side=tk.LEFT)
        
        self.diet_pref_var = tk.StringVar(value="Mixed")
        diet_combobox = ttk.Combobox(diet_row, textvariable=self.diet_pref_var,
                                    values=["Mixed", "Animal Based", "Plant Based", "Vegetarian"], 
                                    width=15, state="readonly")
        diet_combobox.pack(side=tk.LEFT, padx=(8, 15))
        
        # Number of meals
        meals_row = ttk.Frame(input_frame)
        meals_row.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(meals_row, text="Meals per Day:").pack(side=tk.LEFT)
        
        self.meals_per_day_var = tk.StringVar(value="4")
        meals_combobox = ttk.Combobox(meals_row, textvariable=self.meals_per_day_var,
                                     values=["3", "4", "5", "6"], width=6, state="readonly")
        meals_combobox.pack(side=tk.LEFT, padx=(8, 15))
        
        # Generate buttons
        button_row = ttk.Frame(input_frame)
        button_row.pack(fill=tk.X, pady=(10, 0))
        
        generate_btn = ttk.Button(button_row, text="Generate Meal Plan",
                                 command=self.generate_meal_plan)
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        random_btn = ttk.Button(button_row, text="Random Plan",
                               command=self.generate_random_plan)
        random_btn.pack(side=tk.LEFT)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(self.parent_frame, text="Daily Meal Plan", padding="10")
        self.results_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.setup_results()
        
        # Chart frame
        self.chart_frame = ttk.LabelFrame(self.parent_frame, text="Nutrition Breakdown", padding="5")
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
                                    text="Enter your weight and click Generate Meal Plan", 
                                    font=('Arial', 10),
                                    foreground='blue')
        self.result_label.pack(pady=8)
    
    def generate_meal_plan(self):
        try:
            weight = self.weight_var.get()
            unit = self.weight_unit_var.get()
            diet_pref = self.diet_pref_var.get()
            meals_per_day = int(self.meals_per_day_var.get())
            
            # Convert weight to kg
            if unit == "lbs":
                weight_kg = weight * 0.453592
            else:
                weight_kg = weight
            
            # Calculate daily protein needs (1.6g per kg for muscle building)
            daily_protein = weight_kg * PROTEIN_PER_KG
            protein_per_meal = daily_protein / meals_per_day
            
            # Generate meal plan based on diet preference
            meal_plan = self.create_meal_plan(diet_pref, daily_protein, meals_per_day)
            
            self.update_results(weight, unit, daily_protein, meal_plan)
            self.update_chart(meal_plan)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid values!")
    
    def generate_random_plan(self):
        # Randomize diet preference for variety
        diets = ["Mixed", "Animal Based", "Plant Based", "Vegetarian"]
        self.diet_pref_var.set(random.choice(diets))
        self.generate_meal_plan()
    
    def create_meal_plan(self, diet_pref, daily_protein, meals_per_day):
        # Filter foods based on diet preference
        if diet_pref == "Animal Based":
            available_foods = {k: v for k, v in FOOD_DATABASE.items() if v['category'] == 'animal'}
        elif diet_pref == "Plant Based":
            available_foods = {k: v for k, v in FOOD_DATABASE.items() if v['category'] == 'plant'}
        elif diet_pref == "Vegetarian":
            available_foods = {k: v for k, v in FOOD_DATABASE.items() if v['category'] in ['vegetarian', 'plant']}
        else:  # Mixed
            available_foods = FOOD_DATABASE.copy()
        
        # Remove some random foods to create variety
        foods_list = list(available_foods.keys())
        if len(foods_list) > 8:
            foods_to_remove = random.sample(foods_list, min(3, len(foods_list) - 8))
            for food in foods_to_remove:
                if food in available_foods:
                    del available_foods[food]
        
        meal_plan = {
            'total_protein': 0,
            'total_calories': 0,
            'meals': [],
            'foods': []
        }
        
        remaining_protein = daily_protein
        
        # Distribute protein across meals
        while remaining_protein > 0 and available_foods:
            # Select a random food
            food_name = random.choice(list(available_foods.keys()))
            food_data = available_foods[food_name]
            
            # Calculate how much of this food to add
            protein_per_serving = food_data['protein']
            max_servings = min(3, int(remaining_protein / protein_per_serving) + 1)
            
            if max_servings < 1:
                # Remove food if it doesn't fit remaining protein
                del available_foods[food_name]
                continue
            
            servings = random.randint(1, max_servings)
            protein_from_food = protein_per_serving * servings
            calories_from_food = food_data['calories'] * servings
            
            # Add to meal plan
            meal_plan['foods'].append({
                'name': food_name,
                'servings': servings,
                'protein': protein_from_food,
                'calories': calories_from_food,
                'serving_size': food_data['serving']
            })
            
            meal_plan['total_protein'] += protein_from_food
            meal_plan['total_calories'] += calories_from_food
            remaining_protein -= protein_from_food
            
            # Remove this food to avoid repetition
            if food_name in available_foods:
                del available_foods[food_name]
        
        # Distribute foods into meals
        foods_per_meal = max(1, len(meal_plan['foods']) // meals_per_day)
        for i in range(meals_per_day):
            start_idx = i * foods_per_meal
            end_idx = (i + 1) * foods_per_meal
            meal_foods = meal_plan['foods'][start_idx:end_idx]
            if meal_foods:
                meal_plan['meals'].append({
                    'name': f"Meal {i+1}",
                    'foods': meal_foods,
                    'protein': sum(food['protein'] for food in meal_foods),
                    'calories': sum(food['calories'] for food in meal_foods)
                })
        
        return meal_plan
    
    def update_results(self, weight, unit, daily_protein, meal_plan):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable text widget for meal plan
        text_frame = ttk.Frame(self.results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        meal_text = tk.Text(text_frame, height=12, wrap=tk.WORD, font=('Arial', 9),
                           yscrollcommand=scrollbar.set)
        meal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=meal_text.yview)
        
        # Header
        meal_text.insert(tk.END, f"📊 DAILY MEAL PLAN SUMMARY\n", 'header')
        meal_text.insert(tk.END, "="*50 + "\n")
        meal_text.insert(tk.END, f"• Weight: {weight} {unit}\n")
        meal_text.insert(tk.END, f"• Target Protein: {daily_protein:.1f}g\n")
        meal_text.insert(tk.END, f"• Achieved Protein: {meal_plan['total_protein']:.1f}g\n")
        meal_text.insert(tk.END, f"• Total Calories: {meal_plan['total_calories']:.0f} kcal\n")
        meal_text.insert(tk.END, f"• Diet Preference: {self.diet_pref_var.get()}\n\n")
        
        # Meals
        for meal in meal_plan['meals']:
            meal_text.insert(tk.END, f"🍽️ {meal['name']}\n", 'meal_header')
            meal_text.insert(tk.END, f"   Protein: {meal['protein']:.1f}g | Calories: {meal['calories']:.0f}\n")
            
            for food in meal['foods']:
                meal_text.insert(tk.END, f"   • {food['name']}: {food['servings']} serving(s) ({food['serving_size']})\n")
                meal_text.insert(tk.END, f"     → Protein: {food['protein']:.1f}g | Calories: {food['calories']:.0f}\n")
            meal_text.insert(tk.END, "\n")
        
        # Configure tags for styling
        meal_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='darkblue')
        meal_text.tag_configure('meal_header', font=('Arial', 10, 'bold'), foreground='darkgreen')
        
        meal_text.configure(state='disabled')
    
    def update_chart(self, meal_plan):
        self.ax.clear()
        
        if not meal_plan['meals']:
            self.ax.text(0.5, 0.5, 'No meal data available', 
                        ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return
        
        # Prepare data for stacked bar chart
        meal_names = [meal['name'] for meal in meal_plan['meals']]
        food_data = {}
        
        # Collect all unique foods across meals
        all_foods = set()
        for meal in meal_plan['meals']:
            for food in meal['foods']:
                all_foods.add(food['name'])
        
        # Initialize food data
        for food in all_foods:
            food_data[food] = [0] * len(meal_names)
        
        # Fill food data
        for i, meal in enumerate(meal_plan['meals']):
            for food in meal['foods']:
                food_data[food['name']][i] = food['protein']
        
        # Create stacked bar chart
        bottom = [0] * len(meal_names)
        colors = plt.cm.Set3(np.linspace(0, 1, len(all_foods)))
        
        for (food, color) in zip(all_foods, colors):
            values = food_data[food]
            self.ax.bar(meal_names, values, bottom=bottom, label=food, color=color)
            bottom = [bottom[i] + values[i] for i in range(len(values))]
        
        self.ax.set_xlabel('Meals')
        self.ax.set_ylabel('Protein (g)')
        self.ax.set_title('Protein Distribution Across Meals', fontsize=11, fontweight='bold')
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        self.ax.grid(True, alpha=0.3)
        
        # Rotate x labels for better fit
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
        
        self.fig.tight_layout()
        self.canvas.draw()