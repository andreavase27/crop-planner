
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from crop_p.database import category_area, category_growth_days, category_yield

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
        


