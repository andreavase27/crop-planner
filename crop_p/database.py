import pandas as pd
# loading the dataset
file_path = '/Users/andreavaselli/Projects/crop-planner/datasets/vegetables.dataset.csv'
plants_df = pd.read_csv(file_path)

print(plants_df.head())
plants_df.info()
print(plants_df.describe())

# creating the list of vegetables categories
categories = plants_df['Category']
official_categories = list()
for c in categories:
    if c in official_categories:
        continue
    else:
        official_categories.append(c)
print(official_categories)
