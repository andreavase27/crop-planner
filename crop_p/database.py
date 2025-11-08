import pandas as pd

# loading the dataset
file_path = '/Users/andreavaselli/Projects/crop-planner/datasets/vegetables.dataset.csv'
plants_df = pd.read_csv(file_path)

# understanding the dataset
print(plants_df.head())
plants_df.info()
print(plants_df.describe())

# creating the list of vegetables categories
official_categories = plants_df['Category'].dropna().unique().tolist()
print(official_categories)

# Estimated area required per category (in m² per plant)
category_area = {
    'Root': 0.25,        # es. carote, rape → fitte ma con radice sottoterra
    'Leafy': 0.20,       # es. lattuga, spinaci → fitte ma richiedono spazio per foglie
    'Fruit': 0.50,       # es. pomodoro, zucchina, peperone → richiedono supporto e spazio
    'Flower': 0.40,      # es. cavolfiore, broccoli → medie dimensioni
    'Tuber': 0.45,       # es. patate, topinambur → più distanziate
    'Legume': 0.35,      # es. fagioli, piselli → necessitano spazio verticale
    'Bulb': 0.20,        # es. cipolla, aglio → compatte ma con distanza radici
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

