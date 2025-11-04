# Crop-planner

The Crop Planner project is a Python-based analytical tool designed to help users plan an optimal vegetable garden based on available land area, number of people, and growing season.
By combining data on plant characteristics (such as required area, growing time, yield, and seasonal suitability), the program estimates the most efficient crop mix that maximizes total yield and provides an estimated amount of vegetables per person.

INPUTS:

The user will be asked to give three information:
- season in which the user wants to start the garden;
- how many squared meters are avaiable for the garden;
- number of types of vegetables to be grown;  (as type we mean the specific vegetable, as eggplant or lattuce)
- how many people are espected to be fed with that harvest.

OUTPUTS:

The program will present:
- the exact number of plants that can be planted, divided on the number of types desired;
  the number of plants and the mix of vegetables is made to maximise the quantity(kg) and the nutritional values;
- better soil conditions;
- better climate;
- health benefits;
- shelf life;
- quantity/nutritional value avaiable for person.

# Repository structure
```
│
├── crop_p/                     # Main Python package
│   ├── init.py                 # Marks the folder as a Python package
│   ├── models.py               # Defines the Plant class (attributes and methods)
│   ├── utils.py                # Utility functions for reading, cleaning, and transforming data
│   ├── core.py                 # Core logic
│   └── database.py             # Eventual database connection
│
├── datasets/                   # Raw data files
│   └── vegetables.csv          # Vegetable dataset used for calculations
│
├── presentation/               # Presentation and analysis
│   └── crop_analysis.ipynb     # Jupyter Notebook for testing, visualization, and reporting
│
├── tests/                      # Unit tests
│   └── test_core.py            # Tests
│
├── .gitignore                  # Git configuration to exclude virtual environments and cache files
├── requirements.txt            # List of required Python dependencies
├── README.md                   # Project documentation and usage guide
└── crop_env/                   # Virtual environment for isolated package management
```