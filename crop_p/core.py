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

    def __init__(self, total_area, season, people, max_categories=5, excluded_plants=None):
        self.total_area = float(total_area)
        self.season = season.capitalize()
        self.people = int(people)
        self.max_categories = int(max_categories)
        self.excluded_plants = [p.lower() for p in excluded_plants] if excluded_plants else []

        self.plan = []   # [(name, category, units, yield_kg, area, growth_days)]
        self.stats = {}  # riassunto finale

    # 1 Filtra le piante per stagione
    def _filter_by_season(self) -> pd.DataFrame:
        df = plants_df.copy()
        return df[df["Season"].astype(str).str.capitalize() == self.season]

    # 2 Pianifica l’orto
    def plan_garden(self):
        df = self._filter_by_season()
        if df.empty:
            self._empty_results()
            return self.stats
        # Esclude piante indesiderate
        if self.excluded_plants:
            df = df[~df["Name"].str.lower().isin(self.excluded_plants)]

        # Crea oggetti Plant e calcola rese e parametri
        candidates = []
        for _, row in df.iterrows():
            plant = Plant(
                name=row["Name"],
                category=row["Category"],
                season=row["Season"],
                area_per_plant=None,
                growth_days=None,
                shelf_life=row.get("Shelf Life (days)", 0),
                yield_per_plant=None,
            )
            area = plant.estimate_area()
            ykg = plant.estimate_yield()
            days = plant.estimate_growth_time()
            if area <= 0 or ykg <= 0:
                continue
            density = ykg / area
            candidates.append((plant, area, ykg, days, density))
            
        if not candidates:
            self._empty_results()
            return self.stats

        # Raggruppa per categoria e sceglie la pianta con yield più alto
        best_by_category = {}
        for plant, area, ykg, days, dens in candidates:
            cat = plant.category
            if cat not in best_by_category or ykg > best_by_category[cat][2]:
                best_by_category[cat] = (plant, area, ykg, days, dens)

        # ordina le migliori categorie per resa per pianta
        selected = sorted(best_by_category.values(), key=lambda x: x[2], reverse=True)[:self.max_categories]

        # aggiunge una unità di ogni tipo finché c'è spazio
        used_area = 0.0
        total_yield = 0.0
        units = [0] * len(selected)

        while True:
            placed_any = False
            for i, (plant, area, ykg, days, dens) in enumerate(selected):
                if used_area + area <= self.total_area:
                    units[i] += 1
                    used_area += area
                    total_yield += ykg
                    placed_any = True
            if not placed_any:
                break