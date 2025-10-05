import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shared import *

class CaffeineCalculator:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()
    
    def setup_ui(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.parent_frame, text="Caffeine Input", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Caffeine amount with unit selection
        input_row1 = ttk.Frame(input_frame)
        input_row1.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(input_row1, text="Caffeine Amount:").pack(side=tk.LEFT)
        
        self.caffeine_var = tk.DoubleVar(value=0.2)
        self.caffeine_entry = ttk.Entry(input_row1, textvariable=self.caffeine_var, width=12)
        self.caffeine_entry.pack(side=tk.LEFT, padx=(8, 5))
        
        self.unit_var = tk.StringVar(value="grams")
        unit_combobox = ttk.Combobox(input_row1, textvariable=self.unit_var, 
                                    values=["grams", "milligrams"], width=8, state="readonly")
        unit_combobox.pack(side=tk.LEFT, padx=(5, 15))
        
        # Quick dose buttons
        quick_doses_frame = ttk.Frame(input_frame)
        quick_doses_frame.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(quick_doses_frame, text="Quick doses:").pack(side=tk.LEFT)
        
        quick_doses = [
            ("0.1g", 0.1),
            ("0.2g", 0.2),
            ("0.15g", 0.15),
            ("0.5g", 0.5),
            ("1g", 1.0),
            ("10g", 10.0)
        ]
        
        for text, dose in quick_doses:
            btn = ttk.Button(quick_doses_frame, text=text, 
                           command=lambda d=dose: self.set_caffeine_dose(d))
            btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Calculate button
        calc_button = ttk.Button(input_frame, text="Calculate Sleep Impact", 
                                command=self.calculate_impact)
        calc_button.pack(pady=(10, 0))
        
        # Results frame
        self.results_frame = ttk.LabelFrame(self.parent_frame, text="Results", padding="10")
        self.results_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.setup_results()
        
        # Chart frame
        self.chart_frame = ttk.LabelFrame(self.parent_frame, text="Caffeine Decay Timeline", padding="5")
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
                                     text="Enter caffeine amount and click Calculate", 
                                     font=('Arial', 10),
                                     foreground='blue')
        self.result_label.pack(pady=8)
    
    def set_caffeine_dose(self, dose):
        self.caffeine_var.set(dose)
        self.unit_var.set("grams")
        self.calculate_impact()
    
    def calculate_remaining_caffeine(self, initial_dose_mg, hours):
        return initial_dose_mg * (0.5) ** (hours / CAFFEINE_HALF_LIFE)
    
    def hours_until_safe(self, initial_dose_mg):
        hours = 0
        max_hours = 200
        while (self.calculate_remaining_caffeine(initial_dose_mg, hours) > SLEEP_THRESHOLD_MG 
               and hours < max_hours):
            hours += 1
        return min(hours, max_hours)
    
    def get_dose_safety_level(self, dose_mg):
        if dose_mg >= LETHAL_DOSE_MG:
            return "LETHAL", "red"
        elif dose_mg >= DANGER_DOSE_MG:
            return "EXTREMELY DANGEROUS", "darkred"
        elif dose_mg >= MAX_SAFE_DOSE_MG:
            return "HIGH DOSE", "orange"
        else:
            return "SAFE RANGE", "green"
    
    def calculate_impact(self):
        try:
            caffeine_amount = self.caffeine_var.get()
            
            if self.unit_var.get() == "grams":
                caffeine_mg = caffeine_amount * 1000
                caffeine_grams = caffeine_amount
            else:
                caffeine_mg = caffeine_amount
                caffeine_grams = caffeine_amount / 1000
            
            safety_level, color = self.get_dose_safety_level(caffeine_mg)
            
            if caffeine_mg >= LETHAL_DOSE_MG:
                messagebox.showwarning("Lethal Dose Warning", 
                                     f"Warning: {caffeine_mg:,.0f}mg is a potentially lethal dose!")
            elif caffeine_mg >= DANGER_DOSE_MG:
                messagebox.showwarning("Dangerous Dose", 
                                     f"Warning: {caffeine_mg:,.0f}mg is extremely dangerous!")
            
            safe_hours = self.hours_until_safe(caffeine_mg)
            self.update_results(caffeine_grams, caffeine_mg, safe_hours, safety_level, color)
            self.update_chart(caffeine_grams, caffeine_mg)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number!")
    
    def update_results(self, caffeine_grams, caffeine_mg, safe_hours, safety_level, color):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        caffeine_mg_formatted = f"{caffeine_mg:,.0f}" if caffeine_mg >= 1000 else f"{caffeine_mg:.0f}"
        caffeine_grams_formatted = f"{caffeine_grams:,.1f}" if caffeine_grams >= 1 else f"{caffeine_grams:.3f}"
        
        result_text = f"""• Dose: {caffeine_grams_formatted}g ({caffeine_mg_formatted}mg)
• Sleep Impact: {safe_hours:.1f} hours
• Safety: {safety_level}"""
        
        result_label = ttk.Label(self.results_frame, text=result_text,
                               font=('Arial', 10), foreground=color)
        result_label.pack(pady=8)
    
    def update_chart(self, caffeine_grams, caffeine_mg):
        self.ax.clear()
        
        safe_hours = self.hours_until_safe(caffeine_mg)
        
        if safe_hours < 12:
            max_hours = 12
        elif safe_hours < 24:
            max_hours = safe_hours + 4
        elif safe_hours < 48:
            max_hours = safe_hours + 8
        else:
            max_hours = safe_hours + 12
        
        max_hours = min(max_hours, 168)
        
        if max_hours <= 24:
            time_step = 0.5
        elif max_hours <= 72:
            time_step = 1
        else:
            time_step = 2
        
        hours = [x * time_step for x in range(0, int(max_hours/time_step) + 1)]
        remaining = [self.calculate_remaining_caffeine(caffeine_mg, h) for h in hours]
        
        self.ax.plot(hours, remaining, 'b-', linewidth=2, label='Caffeine in body')
        self.ax.axhline(y=SLEEP_THRESHOLD_MG, color='r', linestyle='--', 
                       linewidth=1.5, label=f'Sleep threshold ({SLEEP_THRESHOLD_MG}mg)')
        
        if safe_hours <= max_hours:
            self.ax.axvline(x=safe_hours, color='g', linestyle=':', 
                           linewidth=1.5, label=f'Safe to sleep ({safe_hours:.1f}h)')
        
        self.ax.set_xlabel('Hours after consumption', fontsize=9)
        self.ax.set_ylabel('Caffeine (mg)', fontsize=9)
        
        if caffeine_mg > 1000:
            self.ax.ticklabel_format(style='plain', axis='y')
            self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
        
        title_text = f'Caffeine Decay: {caffeine_grams:.3f}g → {safe_hours:.1f}h affect'
        self.ax.set_title(title_text, fontsize=11, fontweight='bold', pad=10)
        
        self.ax.set_xlim(0, max_hours)
        self.ax.set_ylim(0, caffeine_mg * 1.05)
        self.ax.grid(True, alpha=0.2)
        self.ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
        
        if max_hours <= 24:
            self.ax.xaxis.set_major_locator(plt.MultipleLocator(2))
        elif max_hours <= 72:
            self.ax.xaxis.set_major_locator(plt.MultipleLocator(6))
        else:
            self.ax.xaxis.set_major_locator(plt.MultipleLocator(24))
        
        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()