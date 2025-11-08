
import pandas as pd
from database import category_area, category_growth_days
class Plant:
    
    def __init__(self, name, category, season, growth_days, health_benefits, nutritional_values, yield_per_plant, area_per_plant, shelf_life):
        self.name = name 
        self.category = category
        self.season = season
        self.growth_days = growth_days
        self.health_benefits = health_benefits
        self.nutritional_values = nutritional_values
        self.yield_per_plant = yield_per_plant
        self.area_per_plant = area_per_plant
        self.shelf_life = shelf_life

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

        # Usa shelf_life se disponibile per regolare la stima
        try:
            shelf_life_days = float(self.shelf_life) if self.shelf_life is not None else 0
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
        """Estimate yield (kg) based on estimated growth time and shelf life."""

        # Stima tempo di crescita medio per categoria
        estimated_growth_days = category_growth_days.get(self.category, 60)

        # Aggiunge shelf life come indicatore di vigore
        try:
            shelf_life_days = float(self.shelf_life) if self.shelf_life is not None else 0
        except (TypeError, ValueError):
            shelf_life_days = 0

        # Combina i due fattori per stimare un "tempo di crescita effettivo"
        effective_growth_time = estimated_growth_days + shelf_life_days / 2

        # Normalizza e calcola la resa stimata
        growth_factor = effective_growth_time / 100
        base_yield = self.yield_per_plant or 0.2
        estimated_yield = base_yield * (1 + growth_factor * 0.1)                     # se una pianta cresce più lentamente (base_days alto), probabilmente produrrà più biomassa (resa più alta).

        return round(estimated_yield, 2)

# --- Test ---
if __name__ == "__main__":
    tomato = Plant(
        "Tomato", "Fruit", "Summer", 90,
        "Rich in vitamin C", "High nutrition",
        2.5, "area", shelf_life=20
    )

    print(f"{tomato.name} requires {tomato.estimate_area()} m² per plant.")
    print(f"Estimated yield: {tomato.estimate_yield()} kg per plant.")
    print(f"Estimated growth time: {tomato.estimate_growth_time()} days.")
        


