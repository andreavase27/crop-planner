
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from crop_p.database import plants_df, category_area, category_growth_days, category_yield

class Plant:
    
    def __init__(self, name, category, season, area_per_plant, growth_days, shelf_life, yield_per_plant):
        self.name = name 
        self.category = category
        self.season = season
        self.area_per_plant = area_per_plant
        self.growth_days = growth_days
        self.shelf_life = shelf_life
        self.yield_per_plant = yield_per_plant
        
    def show_description(self):
        return f"{self.name} ({self.category}) grows in {self.season} and takes {self.growth_days} days."
    
    def estimate_area(self):
        """Estimate area per plant based on its category."""
        key = self.category.capitalize()
        self.area_per_plant = category_area.get(key, 0.3)        # get the value corrresponding to the key, if not found return 0.3
        return self.area_per_plant
    
    def estimate_growth_time(self):
        """Estimate total growth time (in days) based on category and shelf life."""
        base_days = category_growth_days.get(self.category, 60)

        # shelf_life per regolare la stima
        if self.shelf_life is None:
            shelf_life_days = 0
        else:
            try:
                shelf_life_days = float(self.shelf_life)
            except (TypeError, ValueError):
                shelf_life_days = 0

        # Regolazione: piante con shelf life lunga crescono un po' più lentamente
        if shelf_life_days > 30:
            growth_time = base_days * 1.1
        elif shelf_life_days < 10:
            growth_time = base_days * 0.9
        else:
            growth_time = base_days

        return round(growth_time, 1)
    
    def estimate_yield(self):
        """
        Estimate plant yield (kg per plant) based on category and growth time.
        Uses growth time (estimated from shelf life and category) to adjust productivity.
        """

        # Base yield per plant from category (default small plant = 0.2 kg)
        base_yield = category_yield.get(self.category, 0.2)

        # growth time from the existing method
        growth_time = self.estimate_growth_time()

        # Normalization factor
        growth_factor = growth_time / 100

        # Plants that grow longer generally produce slightly more yield
        if growth_time > 70:
            estimated_yield = base_yield * 1.1
        elif growth_time < 30:
            estimated_yield = base_yield * 0.9
        else:
            estimated_yield = base_yield
        return (estimated_yield)
    
# Test
if __name__ == "__main__":
    tomato = Plant(
        "Tomato", "Fruit", "Summer", 0.3,
        50, 20, 2.5
    )

    print(f"{tomato.name} requires {tomato.estimate_area()} m² per plant.")
    print(f"Estimated yield: {tomato.estimate_yield()} kg per plant.")
    print(f"Estimated growth time: {tomato.estimate_growth_time()} days.")

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
            
        # Statistiche finali
        self.plan = []
        total_growth_for_avg = 0.0
        total_units = 0

        for (plant, area, ykg, days, dens), u in zip(selected, units):
            if u == 0:
                continue
            self.plan.append((plant.name, plant.category, u, ykg, area, days))
            total_units += u
            total_growth_for_avg += days

        avg_growth = round(total_growth_for_avg / len(self.plan), 1) if self.plan else 0.0
        ypp = round(total_yield / self.people, 2) if self.people else 0.0

        self.stats = {
            "Plant types": len(self.plan),
            "Total plants": total_units,
            "Used area (m²)": round(used_area, 2),
            "Total yield (kg)": round(total_yield, 2),
            "Yield per person (kg)": ypp,
            "Average growth time (days)": avg_growth,
        }

        return self.stats

    # Metodo per casi vuoti
    def _empty_results(self):
        self.plan = []
        self.stats = {
            "Plant types": 0,
            "Total plants": 0,
            "Used area (m²)": 0.0,
            "Total yield (kg)": 0.0,
            "Yield per person (kg)": 0.0,
            "Average growth time (days)": 0.0,
        }

    # Stampa riepilogo finale
    def summary(self):
        stats = self.plan_garden()

        print("🌿 GARDEN SUMMARY 🌿")
        print(f"Season: {self.season}")
        print(f"Total area: {self.total_area} m²")
        print(f"People: {self.people}")
        print(f"Max categories: {self.max_categories}")
        if self.excluded_plants:
            print(f"Excluded plants: {', '.join(self.excluded_plants)}")
        print("-" * 95)
        print(f"{'Plant':<20}{'Category':<15}{'Units':<8}{'Area (m²)':<12}"
              f"{'Yield/plant (kg)':<17}{'Growth (days)':<15}")
        print("-" * 95)

        for name, category, u, ykg, area, days in self.plan:
            print(f"{name:<20}{category:<15}{u:<8}{area:<12.2f}"
                  f"{ykg:<17.2f}{days:<15.1f}")

        print("-" * 95)
        for k, v in stats.items():
            print(f"{k}: {v}")
        print("-" * 95)


