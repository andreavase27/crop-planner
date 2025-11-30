import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))            # with these three lines Python will always recognize the root of the project (crop-planner/) and the sub-files.

# loading the dataset
file_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "datasets",
    "vegetables.dataset.csv"                
)
file_path = os.path.abspath(file_path)         # this is made so that every machine can run the programm, because the dataset is found automatically.

plants_df = pd.read_csv(file_path)

# creating the list of vegetables categories
official_categories = plants_df['Category'].dropna().unique().tolist()

# Estimated area required per category (in m² per plant)
category_area = {
    'Root': 0.25,        # carrots, turnips → dense spacing but roots grow underground
    'Leafy': 0.20,       # lettuce, spinach → compact but need room for leaves
    'Fruit': 0.50,       # tomatoes, zucchini, peppers → need support and space
    'Flower': 0.40,      # cauliflower, broccoli → medium-sized plants
    'Tuber': 0.45,       # potatoes → require wider spacing
    'Legume': 0.35,      # beans, peas → need vertical space/trellises
    'Bulb': 0.20,        # onions, garlic → compact but need root spacing
    'Grain': 0.30,       # corn, barley → more space between rows
    'Stem': 0.50,        # celery, leek → taller plants, need airflow
    'Herb': 0.15,        # basil, parsley → can grow very densely
    'Cactus': 0.80,      # slow-growing, large plants → require plenty of space
    'Succulent': 0.70,   # similar to cactus in spacing needs
    'Fern': 0.60         # ornamental/shade plants → need more lateral space
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