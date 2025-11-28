import os
import sys

# aggiungo manualmente la cartella principale al path
# così posso importare i file del progetto anche se eseguo questo script direttamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crop_p.models import Garden, PlantInfoRetriever
from crop_p.database import plants_df


def run_simulation(total_area, season, people, max_categories=5, exclude_plants=None):
    """
    it executes a simulation of the garden, it contains all the parameters needed to run the tests
    """

    garden = Garden(
        total_area=total_area,
        season=season,
        people=people,
        max_categories=max_categories,
        excluded_plants=exclude_plants,
    )

    # stampa il riassunto direttamente
    garden.summary()
    return garden

if __name__ == "__main__":
    # test of the garden
    print("\n=== TEST GARDEN ===\n")
    
    run_simulation(
        total_area=15,
        season="Summer",
        people=2,
        max_categories=4,
        exclude_plants=[""]   # here plants to avoid
    )

    # test of the inforetriever
    print("\n=== TEST PLANT INFO ===\n")

    retriever = PlantInfoRetriever(plants_df)

    info = retriever.get_info("Carrot")  # random plant

    # print the info
    for key, value in info.items():
        print(f"{key}: {value}")