# Crop-planner

## Overview

Crop-planner is a Python-based analytical tool that helps the user in developing a vegetable garden.
The user can interact with the program through a web app developed with Streamlit in app.py. 
It is divided into two section:

### 1. Garden Planner

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

### 2. Plant Explorer

The Plant Explorer section provides information about a specific plant selected by the user.
The available information includes: Category, Season, Origin, Availability, Shelf life, Storage requirements, Growing conditions, and Health benefits.

### Limitations

The dataset does not provide agronomic values such as area per plant, growth time, or yield.
To compensate, category-level area, growth time, and yield indices were defined based on typical horticultural behavior.
These values are then refined using shelf life as a biological proxy (longer shelf life → slower growth, slightly higher yield).
This method ensures almost realistic estimates even in the absence of detailed plant-specific data.

## Installation 

Assuming Python is installed in the machine, from the shell:

1. Clone the repository.
```
git clone https://github.com/andreavase27/crop-planner.git
cd crop-planner
```

2. Create a virtual environment to keep dependencies isolated.
```
python3 -m venv crop_env
```

Activate it:

macOS / Linux
```
source crop_env/bin/activate
```

Windows
```
crop_env\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run the Streamlit web app
```
streamlit run web_app/app.py
```

The dataset is already included in the repository (datasets/vegetables.dataset.csv), so no additional downloads are required.

## Repository structure
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