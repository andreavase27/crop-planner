class Plant:
    """
    Modello per una singola specie di pianta.
    """

    def __init__(self, name, season, growth_days, area_per_plant, yield_per_plant):
        self.name = name
        self.season = season
        self.growth_days = growth_days
        self.area_per_plant = area_per_plant
        self.yield_per_plant = yield_per_plant
        self.technique = None
        self.adjusted_area = area_per_plant
        self.adjusted_yield = yield_per_plant

    def adjust_for_technique(self, technique):
        factors = {
            "tradizionale": {"area": 1.0, "yield": 1.0},
            "serra": {"area": 1.0, "yield": 1.2},
            "idroponica": {"area": 0.5, "yield": 1.4},
        }
        if technique not in factors:
            technique = "tradizionale"

        f = factors[technique]
        self.technique = technique
        self.adjusted_area = self.area_per_plant * f["area"]
        self.adjusted_yield = self.yield_per_plant * f["yield"]

    def yield_for_quantity(self, quantity):
        return quantity * self.adjusted_yield

    def area_for_quantity(self, quantity):
        return quantity * self.adjusted_area

    def describe(self):
        base = f"{self.name} ({self.season}) - {self.growth_days} giorni"
        if self.technique:
            base += f" | tecnica: {self.technique}"
        base += f" | area/pianta: {self.adjusted_area:.2f} m² | resa: {self.adjusted_yield:.2f} kg"
        return base

    def __repr__(self):
        return f"Plant({self.name}, {self.season})"



