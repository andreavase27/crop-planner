# Crop-planner

Crop-planner is a Python-based analytical tool that helps the user in developing a vegetable garden.
The user can interact with the program through a web app developed with Streamlit in app.py. 
It is divided into two section:

# 1. Garden Planner

The Garden Planner section is designed to help users plan an optimal vegetable garden based on available land area, number of people, and growing season.
By combining data on plant characteristics (such as required area, growing time, yield, and seasonal suitability), defined in the class "Plant", the program, thanks to the class "Garden", estimates the most efficient crop mix that maximizes total yield and provides an estimated amount of vegetables per person.

INPUT:

The user will be asked to give the following information:
- season in which the user wants to start the garden;
- how many square meters are available for the garden;
- number of categories of vegetables to be grown (as category we mean tuber, legume, fruit, leafy, etc...);
- how many people are expected to be fed with that harvest;
- any unwanted plants.

OUTPUT:

The program will present:
- the exact number of plants that can be planted, organized by the number of categories desired;
  the number of plants and the mix of vegetables are designed to maximize the quantity (kg);
- yield per plant and total yield;
- expected growth days.

# 2. Plant Explorer

The Plant Explorer section provides information about a specific plant selected by the user.
The available information includes: Category, Season, Origin, Availability, Shelf life, Storage requirements, Growing conditions, and Health benefits.


# Repository structure
```
│
├── crop_p/                     # Main Python package
│   ├── init.py                 # Marks the folder as a Python package
│   ├── models.py               # Defines the Plant class (attributes and methods)
│   ├── core.py                 # Core logic
│   └── database.py             # Utility functions for reading, cleaning, and transforming data
│
├── datasets/                   # Raw data files
│   └── vegetables.csv          # Vegetable dataset used for calculations
│
├── .gitignore                  # Git configuration to exclude virtual environments and cache files
├── requirements.txt            # List of required Python dependencies
├── README.md                   # Project documentation and usage guide
└── crop_env/                   # Virtual environment for isolated package management
```