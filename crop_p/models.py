class Plant:
    """
    Modello per una singola specie di pianta.
    """
    total_plants = 0

    def __init__(self, name, season, growth_days, area_per_plant, yield_per_plant):
        self.name = name
        self.season = season
        self.growth_days = growth_days
        self.area_per_plant = area_per_plant
        self.yield_per_plant = yield_per_plant
        self.technique = None
        self.adjusted_area = area_per_plant
        self.adjusted_yield = yield_per_plant

        Plant.total_plants += 1        # incrementa ogni volta che si crea una nuova pianta


    def plant_description(self):
        print(f"plant's name: {self.name}, plant's season: {self.season}")

    def get_total_plants(cls):
        return cls.total_plants
    

