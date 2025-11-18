import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))            # with these three lines Python will always recognize the root of the project (crop-planner/) and the sub-files.

import pandas as pd
import re 

# loading the dataset
file_path = '/Users/andreavaselli/Projects/crop-planner/datasets/vegetables.dataset.csv'
plants_df = pd.read_csv(file_path)

# understanding the dataset
print(plants_df.head())
plants_df.info()
print(plants_df.describe())

# extract nutritional values
def parse_nutrients(nutri_string):
    """
    Estrae kcal, proteine e fibre da una stringa come:
    '41 kcal, 0.9g protein, 2.8g fiber'
    """
    if pd.isna(nutri_string):
        return 0, 0.0, 0.0

    kcal_match = re.search(r"(\d+)\s*kcal", nutri_string)
    protein_match = re.search(r"([\d\.]+)\s*g protein", nutri_string)
    fiber_match = re.search(r"([\d\.]+)\s*g fiber", nutri_string)

    kcal = int(kcal_match.group(1)) if kcal_match else 0
    protein = float(protein_match.group(1)) if protein_match else 0.0
    fiber = float(fiber_match.group(1)) if fiber_match else 0.0

    return kcal, protein, fiber

# Applica il parser e crea colonne nel dataframe
plants_df[["kcal", "protein", "fiber"]] = plants_df[
    "Nutritional Value (per 100g)"
].apply(lambda x: pd.Series(parse_nutrients(x)))

# Copia la colonna Health Benefits con un nome più corto
plants_df["health"] = plants_df["Health Benefits"]

# creating the list of vegetables categories
official_categories = plants_df['Category'].dropna().unique().tolist()
print(official_categories)

# Estimated area required per category (in m² per plant)
category_area = {
    'Root': 0.25,        # es. carote, rape → fitte ma con radice sottoterra
    'Leafy': 0.20,       # es. lattuga, spinaci → fitte ma richiedono spazio per foglie
    'Fruit': 0.50,       # es. pomodoro, zucchina, peperone → richiedono supporto e spazio
    'Flower': 0.40,      # es. cavolfiore, broccoli → medie dimensioni
    'Tuber': 0.45,       # es. patate, → più distanziate
    'Legume': 0.35,      # es. fagioli, piselli → necessitano spazio verticale
    'Bulb': 0.20,        # es. cipolla, aglio → compatte 
    'Grain': 0.30,       # es. mais, orzo → più spazio tra file
    'Stem': 0.50,        # es. sedano, porro → mediamente alti, necessitano aria
    'Herb': 0.15,        # es. basilico, prezzemolo → molto fitti
    'Cactus': 0.80,      # piante lente e grandi, richiedono molto spazio
    'Succulent': 0.70,   # simili ai cactus
    'Fern': 0.60         # piante ornamentali o da ombra, più spazio laterale
}

# Estimated growth time (in days) per category
category_growth_days = {
    'Root': 90,
    'Leafy': 45,
    'Fruit': 80,
    'Flower': 70,
    'Tuber': 100,
    'Legume': 75,
    'Bulb': 110,
    'Grain': 120,
    'Stem': 60,
    'Herb': 40,
    'Cactus': 150,
    'Succulent': 180,
    'Fern': 90
}

# Estimated average yield (kg per plant) by category
category_yield = {        
    'Root': 0.4,
    'Leaf': 0.2,
    'Fruit': 2.0,
    'Flower': 0.6,
    'Tuber': 1.5,
    'Legume': 0.7,         
    'Bulb': 0.3,       
    'Grain': 0.8,    
    'Stem': 0.5,       
    'Herb': 0.1,                
    'Cactus': 0.3,     
    'Succulent': 0.2,  
    'Fern': 0.15       
}