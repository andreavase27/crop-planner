# 🌱 Crop Planner

**[▶ Try the live app](https://crop-planner-av.streamlit.app)** — no installation required.

Crop Planner is a Python tool that helps you design a vegetable garden. Given your available area, the season, and how many people you want to feed, it estimates the crop mix that maximizes total yield — and lets you explore detailed information about each plant.

Built with **Python**, **pandas**, and **Streamlit**, with an object-oriented core (`Plant` and `Garden` classes).

---

## Features

### 1. Garden Planner

Plans an optimal vegetable garden based on land area, number of people, and growing season. Combining data on plant characteristics (required area, growing time, yield, seasonal suitability), the `Garden` class estimates the most efficient crop mix.

**Input** — season, available area (m²), number of vegetable categories (tuber, legume, fruit, leafy, …), number of people to feed, and any plants to exclude.

<img width="1431" height="655" alt="image" src="https://github.com/user-attachments/assets/3470ef32-e09a-47c8-9294-e62ca574e6b2" />

**Output** — the number of plants to grow per category (mix optimized to maximize total kg), yield per plant and total yield, and expected growing days.

<img width="1438" height="661" alt="image" src="https://github.com/user-attachments/assets/f0aa91cb-1da0-4c99-8451-efe0258f4846" />

### 2. Plant Explorer

Detailed information for each plant in the dataset: category, season, origin, availability, shelf life, storage requirements, growing conditions, and health benefits.

<img width="1437" height="784" alt="image" src="https://github.com/user-attachments/assets/039d3467-6844-4f50-8559-f936457a49ac" />

## How the Estimates Work (and Their Limits)

The plant data comes from the [Vegetables Dataset](https://www.kaggle.com/datasets/rudraprasadbhuyan/vegetables-dataset) by Rudra Prasad Bhuyan on Kaggle (category, origin, shelf life, storage, growing conditions, health benefits). The dataset does not provide agronomic values such as area per plant, growth time, or yield — to compensate, category-level indices were defined based on typical horticultural behavior, then refined using **shelf life as a biological proxy** (longer shelf life → slower growth, slightly higher yield). This yields realistic estimates even in the absence of plant-specific agronomic data — but they should be read as reasoned approximations, not agronomic ground truth.

## Run Locally

Requires Python ≥ 3.10 and Git.

```bash
# 1. Clone the repository
git clone https://github.com/andreavase27/crop-planner.git
cd crop-planner

# 2. Create and activate a virtual environment
python3 -m venv crop_env
source crop_env/bin/activate        # macOS / Linux
# crop_env\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
streamlit run web_app/app.py
```

The dataset is included in the repository (`datasets/vegetables.dataset.csv`), so no additional downloads are required.

## Repository Structure

```
├── crop_p/                        # Main Python package
│   ├── __init__.py
│   ├── models.py                  # Plant class (attributes and methods)
│   ├── core.py                    # Optimization / planning logic (Garden class)
│   └── database.py                # Data reading, cleaning, and transformation
├── web_app/
│   └── app.py                     # Streamlit web app
├── datasets/
│   └── vegetables.dataset.csv     # Vegetable dataset 
├── requirements.txt
└── README.md
```

## Author

**Andrea Vaselli** — M.Sc. student in Data Science for Economics and Health, Università degli Studi di Milano.
Dataset: [Vegetables Dataset](https://www.kaggle.com/datasets/rudraprasadbhuyan/vegetables-dataset) by Rudra Prasad Bhuyan, Kaggle.
