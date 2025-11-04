
import pandas as pd

class Plant:
    
    def __init__(self, name, category, season, growth_days, health_benefits, nutritional_values, yield_per_plant, area_per_plant):
        self.name = name 
        self.category = category
        self.season = season
        self.growth_days = growth_days
        self.health_benefits = health_benefits
        self.nutritional_values = nutritional_values
        self.yield_per_plant = yield_per_plant
        self.area_per_plant = area_per_plant

    def show_description(self):
        print(f"the {self.name} grows during {self.season} for about {self.growth_days}")
    
    def space_required(self, category):
        if 
    



