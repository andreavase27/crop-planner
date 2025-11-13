import os, sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))                           # aggiunge la directory crop_p (dove sta core.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))       # La prima sys.path.append aggiunge la directory crop_p (dove sta core.py)

from crop_p.models import Plant
from crop_p.database import plants_df

class Garden:
    """
    Simula un orto:
    - filtra le piante per stagione
    - esclude piante non desiderate
    - sceglie fino a max_categories tipi diversi (quelle con resa stimata più alta per categoria)
    - riempie lo spazio in modo bilanciato 
    """

    def __init__(self, total_area, season, people, max_categories, excluded_plants):
        self.total_area = float(total_area)
        self.season = season.capitalize()
        self.people = int(people)
        self.max_categories = int(max_categories)
        self.excluded_plants = excluded_plants

        self.plan = []   # [(name, category, units, yield_kg, area, growth_days)]
        self.stats = {}  # riassunto finale

  