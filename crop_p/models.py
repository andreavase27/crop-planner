class plant:
    def __init__(self, name, season, growth_days, area_per_plant, yield_per_plant):
        self.name = name
        self.season = season
        self.growth_days = growth_days
        self.area_per_plant = area_per_plant
        self.yield_per_plant = yield_per_plant

    def plant_description(self):
        print("the plant is called ", self.name, "and it grows in", self.season)

    
        
garlic = plant('garlic', 'summer', '40', '3', '2')




