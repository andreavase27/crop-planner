
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crop_p.database import plants_df, category_area, category_growth_days, category_yield

class Plant:
    
    def __init__(self, name, category, season, shelf_life):
        self.name = name.strip()
        self.category = category.strip().capitalize()
        self.season = season.strip().capitalize()
        try:
            self.shelf_life = float(shelf_life)
        except (TypeError, ValueError):
            self.shelf_life = 0.0

        # these will be computed
        self.area_per_plant = None
        self.growth_days = None
        self.yield_per_plant = None

    def show_description(self):
        return f"{self.name} ({self.category}) grows in {self.season} and takes {self.growth_days} days."
    
    def estimate_area(self):
        """Estimate area per plant based on its category."""
        key = self.category
        self.area_per_plant = category_area.get(key, 0.3)        # get the value corrresponding to the key, if not found return 0.3
        return self.area_per_plant
    
    def estimate_growth_time(self):
        """Estimate total growth time (in days) based on category and shelf life."""
        base_days = category_growth_days.get(self.category, 60)

        # Adjustment: plants with a long shelf life grow a little slower
        if self.shelf_life > 30:
            growth_time = base_days * 1.1
        elif self.shelf_life < 10:
            growth_time = base_days * 0.9
        else:
            growth_time = base_days

        self.growth_days = round(growth_time, 2)
        return self.growth_days
    
    def estimate_yield(self):
        """
        Estimate plant yield (kg per plant) based on category and growth time.
        Uses growth time (estimated from shelf life and category) to adjust productivity.
        """

        # Base yield per plant from category (default small plant = 0.2 kg)
        base_yield = category_yield.get(self.category, 0.2)

        # growth time from the existing method
        growth_time = self.estimate_growth_time()

        # Plants that grow longer generally produce slightly more yield
        if growth_time > 70:
            estimated_yield = base_yield * 1.1
        elif growth_time < 30:
            estimated_yield = base_yield * 0.9
        else:
            estimated_yield = base_yield
        
        self.yield_per_plant = round(estimated_yield, 2)
        return self.yield_per_plant
    
class Garden:
    """
    The logic is:
    - filter plants by selected season
    - exclude unwanted plants
    - choose categories based on max_categories (those with higher yield for each category)
    - fill the available space in balanced way, that is, it circles adding an element for each category till there's space.
    """

    def __init__(self, total_area, season, people, max_categories=5, excluded_plants=None):
        self.total_area = float(total_area)
        self.season = season.capitalize()
        self.people = int(people)
        self.max_categories = int(max_categories)
        self.excluded_plants = [p.lower() for p in excluded_plants] if excluded_plants else []

        self.plan = []   # [(name, category, units, yield_kg, area, growth_days)]
        self.stats = {}  # final statistics

    # Filter by season
    def filterSeason(self) -> pd.DataFrame:    #?
        df = plants_df.copy()
        return df[df["Season"].astype(str).str.capitalize() == self.season]          #filter the rows only ehwere the season coincides
    
    # Method for empty cases
    def empty_results(self):                  # it works for example where there are no plants for the season or after the esclusion
        self.plan = []
        self.stats = {
            "Plant types": 0,
            "Total plants": 0,
            "Used area (m²)": 0.0,
            "Total yield (kg)": 0.0,
            "Yield per person (kg)": 0.0,
            "Average growth time (days)": 0.0,
        }

    # Plan the garden, main method
    def plan_garden(self):
        df = self.filterSeason()
        if df.empty:
            self.empty_results()
            return self.stats                  #if there are no plants in that period it returns empty stats
        # excludes unwanted plants
        if self.excluded_plants:
            df = df[~df["Name"].str.lower().isin(self.excluded_plants)]             # it creates a boolean serie with the names of the plants: if excluded =FALSE, then the rows of these plants are removed with df.

        # creates plants objects and computes some parameters
        candidates = []
        for _, row in df.iterrows():                      # it converts each row in a plant object and adds some parameters like area, ykg, days. Then all the tuples are inserted in the candidates list.
            plant = Plant(
                name=row["Name"],
                category=row["Category"],
                season=row["Season"],
                shelf_life=row.get("Shelf Life (days)", 0),
            )
            area = plant.estimate_area()
            ykg = plant.estimate_yield()
            days = plant.estimate_growth_time()
            density = ykg / area
            if area <= 0 or ykg <= 0:
                continue
            candidates.append((plant, area, ykg, days, density))
            
        if not candidates:
            self.empty_results()
            return self.stats

        # group by category and chose the plant with higher yield.
        bestCategory = {}
        for plant, area, ykg, days, dens in candidates:
            cat = plant.category           
            if cat not in bestCategory or ykg > bestCategory[cat][2]:          # for each candidate, it decides if adding it to best candidates if the yiled is higher
                bestCategory[cat] = (plant, area, ykg, days, dens)             # the result of this block is a dictionary, that has one plant for each category, that is the most productive of the category.

        # sort the best categories by yield per plant
        selected = sorted(bestCategory.values(), key=lambda x: x[2], reverse=True)[:self.max_categories]          # the result is a list that takes only the values of the bestCategory dictionary, in a decreasing order.

        # adds a unit for each category till there's space
        used_area = 0.0
        total_yield = 0.0
        units = [0] * len(selected)

        while True:
            placed_any = False
            for i, (plant, area, ykg, days, dens) in enumerate(selected):           # it iterates selected getting the index and the value
                if used_area + area <= self.total_area:
                    units[i] += 1
                    used_area += area
                    total_yield += ykg
                    placed_any = True
            if not placed_any:
                break
            
        # final stats
        self.plan = []                      # this list will be the final result for the user
        growth_days_category = 0.0
        total_units = 0

        for (plant, area, ykg, days, dens), u in zip(selected, units):            #for each category/plant this keeps togheter both the tuple and the unit number
            if u == 0:
                continue
            
            # gives the health statistics by taking them from the original dataset
            health = plants_df.loc[plants_df["Name"] == plant.name, "Health Benefits"].values         # this finds the health benefits for each plant selected in a numpy array.
            health = health[0] if len(health) > 0 else "N/A"                                          # check if tehre are no health benefits, return N/A

            self.plan.append((plant.name, plant.category, u, ykg, area, days, health))                # this tuple represents a row of the final result
            total_units += u
            growth_days_category += days                                                              # this is the sum of the grow days for each plant

        avg_growth = round(growth_days_category / len(self.plan), 1) if self.plan else 0.0            # this is the average growth days for each plant
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

    # print final summary
    def summary(self):
        stats = self.plan_garden()           

        print("\n=== GARDEN SUMMARY ===")
        print("Season:", self.season)
        print("Total area (m²):", self.total_area)
        print("People:", self.people)
        print("Max categories:", self.max_categories)
        if self.excluded_plants:
            print("Excluded plants:", ", ".join(self.excluded_plants))

        print("\nPlants chosen:")
        print("-----------------------------------------")
        for name, category, u, ykg, area, days, health in self.plan:
            print(f"{name} ({category}) - units={u}, area={area}, yield={ykg}, days={days}")
            print("  Health:", health)
        print("-----------------------------------------")

        print("\nStats:")
        for k, v in stats.items():
            print(f"{k}: {v}")

class PlantInfoRetriever:
    """
    Retrives some important information about a seleted plant.
    """

    def __init__(self, dataframe):
        self.df = dataframe                  # it will be necessary to specify the dataframe "plants_df"

    def get_info(self, plant_name: str) -> dict:
        """
        Returns a dictionary with some important information
        for a specific plant.
        """

        # Normalize to avoid mismatch
        name = plant_name.strip().lower()              # normalizing the name

        match = self.df[self.df["Name"].str.lower() == name]           # compares every name of plant of the dataframe and keeps only the row with the same name.

        if match.empty:
            return {"error": f"Plant '{plant_name}' not found in the dataset."}

        row = match.iloc[0]          # converts the first row of the filtered dataframe and converts it into a serie

        info = {
            "Name": row["Name"],
            "Category": row["Category"],
            "Season": row["Season"],
            "Origin": row["Origin"],
            "Availability": row["Availability"],
            "Shelf Life (days)": row["Shelf Life (days)"],
            "Storage Requirements": row["Storage Requirements"],
            "Growing Conditions": row["Growing Conditions"],
            "Health Benefits": row["Health Benefits"],
        }

        return info


