import tkinter as tk
from tkinter import ttk
from caffeine_calculator import CaffeineCalculator
from protein_calculator import ProteinCalculator
from meal_planner import MealPlanner

class HealthCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Calculator - Caffeine, Protein & Meal Planner")
        self.root.geometry("1000x800")
        self.root.configure(bg='#f0f0f0')
        
        self.current_calculator = "caffeine"
        self.setup_ui()
        
        # Initialize calculators
        self.caffeine_calc = CaffeineCalculator(self.caffeine_frame)
        self.protein_calc = ProteinCalculator(self.protein_frame)
        self.meal_planner = MealPlanner(self.meal_frame)
    
    def setup_ui(self):
        # Main container frame
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header with toggle buttons
        self.setup_header()
        
        # Initialize calculator frames
        self.caffeine_frame = ttk.Frame(self.main_container)
        self.protein_frame = ttk.Frame(self.main_container)
        self.meal_frame = ttk.Frame(self.main_container)
        
        # Show caffeine calculator by default
        self.show_caffeine_calculator()
    
    def setup_header(self):
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # CENTERED Title
        title_label = ttk.Label(header_frame, text="🏥 Health Calculator", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(expand=True)
        
        # Toggle buttons frame
        toggle_frame = ttk.Frame(header_frame)
        toggle_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Center the toggle buttons
        button_container = ttk.Frame(toggle_frame)
        button_container.pack(expand=True)
        
        # Calculator toggle buttons
        self.caffeine_btn = tk.Button(button_container, text="☕ Caffeine Calculator",
                                     font=('Arial', 10, 'bold'),
                                     command=self.show_caffeine_calculator,
                                     bg='#0078D7', fg='white',
                                     relief='raised', padx=10, pady=5)
        self.caffeine_btn.pack(side=tk.LEFT, padx=(5, 2))
        
        self.protein_btn = tk.Button(button_container, text="💪 Protein Calculator",
                                    font=('Arial', 10, 'bold'),
                                    command=self.show_protein_calculator,
                                    bg='#f0f0f0', fg='black',
                                    relief='raised', padx=10, pady=5)
        self.protein_btn.pack(side=tk.LEFT, padx=(2, 2))
        
        self.meal_btn = tk.Button(button_container, text="🍽️ Meal Planner",
                                 font=('Arial', 10, 'bold'),
                                 command=self.show_meal_planner,
                                 bg='#f0f0f0', fg='black',
                                 relief='raised', padx=10, pady=5)
        self.meal_btn.pack(side=tk.LEFT, padx=(2, 5))
    
    def show_caffeine_calculator(self):
        self.current_calculator = "caffeine"
        self.protein_frame.pack_forget()
        self.meal_frame.pack_forget()
        self.caffeine_frame.pack(fill=tk.BOTH, expand=True)
        self.update_button_styles()
    
    def show_protein_calculator(self):
        self.current_calculator = "protein"
        self.caffeine_frame.pack_forget()
        self.meal_frame.pack_forget()
        self.protein_frame.pack(fill=tk.BOTH, expand=True)
        self.update_button_styles()
    
    def show_meal_planner(self):
        self.current_calculator = "meal"
        self.caffeine_frame.pack_forget()
        self.protein_frame.pack_forget()
        self.meal_frame.pack(fill=tk.BOTH, expand=True)
        self.update_button_styles()
    
    def update_button_styles(self):
        # Reset all buttons to default style
        self.caffeine_btn.configure(bg='#f0f0f0', fg='black', relief='raised')
        self.protein_btn.configure(bg='#f0f0f0', fg='black', relief='raised')
        self.meal_btn.configure(bg='#f0f0f0', fg='black', relief='raised')
        
        # Set active button style
        if self.current_calculator == "caffeine":
            self.caffeine_btn.configure(bg='#0078D7', fg='white', relief='sunken')
        elif self.current_calculator == "protein":
            self.protein_btn.configure(bg='#0078D7', fg='white', relief='sunken')
        elif self.current_calculator == "meal":
            self.meal_btn.configure(bg='#0078D7', fg='white', relief='sunken')

def main():
    root = tk.Tk()
    app = HealthCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
