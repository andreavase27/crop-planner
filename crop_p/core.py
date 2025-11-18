
import sys, os

# Aggiunge la directory crop_p al path (necessario per l'esecuzione diretta)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crop_p.models import Garden


def run_simulation(total_area, season, people, max_categories=5, exclude_plants=None):
    """
    Esegue una simulazione completa dell’orto:

    - total_area (float): area totale disponibile in m²
    - season (str): stagione (Spring, Summer, Autumn, Winter)
    - people (int): numero di persone da nutrire
    - max_categories (int): numero massimo di categorie diverse da usare
    - exclude_plants (list[str]): lista di piante da escludere

    Return: oggetto Garden già calcolato
    """

    garden = Garden(
        total_area=total_area,
        season=season,
        people=people,
        max_categories=max_categories,
        excluded_plants=exclude_plants,
    )

    garden.summary()
    return garden


# ESECUZIONE DIRETTA DI TEST
if __name__ == "__main__":
    run_simulation(
        total_area=20,
        season="Spring",
        people=2,
        max_categories=4,
        exclude_plants=[""]   # esempio
    )