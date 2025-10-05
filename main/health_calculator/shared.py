# Shared constants and utilities
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import numpy as np

# Caffeine parameters
CAFFEINE_HALF_LIFE = 5.0
SLEEP_THRESHOLD_MG = 50
LETHAL_DOSE_MG = 10000
DANGER_DOSE_MG = 1000
MAX_SAFE_DOSE_MG = 400

# Protein parameters
PROTEIN_PER_KG = 1.6
PROTEIN_PER_LB = 0.72

# Food database
FOOD_DATABASE = {
    # Animal Based Proteins
    'Chicken Breast': {'protein': 31, 'calories': 165, 'category': 'animal', 'serving': '100g'},
    'Eggs': {'protein': 13, 'calories': 155, 'category': 'animal', 'serving': '2 large eggs'},
    'Salmon': {'protein': 25, 'calories': 206, 'category': 'animal', 'serving': '100g'},
    'Greek Yogurt': {'protein': 10, 'calories': 59, 'category': 'animal', 'serving': '100g'},
    'Beef Steak': {'protein': 26, 'calories': 271, 'category': 'animal', 'serving': '100g'},
    'Tuna': {'protein': 30, 'calories': 132, 'category': 'animal', 'serving': '100g'},
    'Whey Protein': {'protein': 24, 'calories': 120, 'category': 'animal', 'serving': '1 scoop'},
    
    # Plant Based Proteins
    'Tofu': {'protein': 8, 'calories': 76, 'category': 'plant', 'serving': '100g'},
    'Lentils': {'protein': 9, 'calories': 116, 'category': 'plant', 'serving': '100g cooked'},
    'Chickpeas': {'protein': 9, 'calories': 139, 'category': 'plant', 'serving': '100g cooked'},
    'Kidney Beans': {'protein': 9, 'calories': 127, 'category': 'plant', 'serving': '100g cooked'},
    'Almonds': {'protein': 21, 'calories': 579, 'category': 'plant', 'serving': '100g'},
    'Peanut Butter': {'protein': 25, 'calories': 588, 'category': 'plant', 'serving': '100g'},
    'Quinoa': {'protein': 4, 'calories': 120, 'category': 'plant', 'serving': '100g cooked'},
    
    # Vegetarian Proteins
    'Paneer': {'protein': 18, 'calories': 265, 'category': 'vegetarian', 'serving': '100g'},
    'Milk': {'protein': 3, 'calories': 42, 'category': 'vegetarian', 'serving': '100ml'},
    'Cottage Cheese': {'protein': 11, 'calories': 98, 'category': 'vegetarian', 'serving': '100g'},
    'Cheese': {'protein': 25, 'calories': 402, 'category': 'vegetarian', 'serving': '100g'}
}