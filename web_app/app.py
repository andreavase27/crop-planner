import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# adding the root path so it finds Garden, PlantInfoRetriver and plants_df, that are in another folder (crop_p)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crop_p.models import Garden, PlantInfoRetriever
from crop_p.database import plants_df

st.set_page_config(page_title="Crop Planner", page_icon="🌱", layout="wide")

st.title("🌱 Crop Planner")

st.write(
    """
    This app lets you:

    - plan a vegetable garden depending on area, season and people
    - explore details about each plant
    """
)

# lateral bar to select the section
section = st.sidebar.radio("Choose a section:", ["🌿 Garden Planner", "🔍 Plant Explorer"])

# 1) GARDEN PLANNER

if section == "🌿 Garden Planner":
    st.header("Plan your garden")

    col1, col2 = st.columns(2)               # creates two columns

    with col1:
        people = st.number_input("Number of people", 1, 1000000, 2)
        season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])

    with col2:
        max_categories = st.number_input("Max categories", 1, 13, 5)
        total_area = st.number_input("Available area (m²)", 1.0, 1000000.0, 20.0)

    exclude_plants = st.multiselect(               # creates a widget that allows to selecct elements from a lista
        "Exclude some plants (optional):",
        sorted(plants_df["Name"].unique()))                 # this is the list of plant sorted alphebetically

    if st.button("Create plan"):            # the block below works only if the button is pressed
        garden = Garden(
            total_area=total_area,
            season=season,
            people=people,
            max_categories=max_categories,
            excluded_plants=exclude_plants
        )

        stats = garden.plan_garden()

        if not garden.plan:
            st.error("No plants found for this configuration.")
        else:
            st.success("Garden plan created!")

            st.subheader("Garden results")

            rows = []                                   # this block creates a list and append dictionaries, so we have a list of dictioaries
            for row in garden.plan:
                name, cat, units, y, area, days, health = row
                rows.append({
                    "Plant": name,
                    "Category": cat,
                    "Units": units,
                    "Area per plant (m²)": area,
                    "Yield/plant (kg)": y,
                    "Growth days": days,
                    "Health benefits": health
                })

            df = pd.DataFrame(rows)                            
            df.insert(0, "#", range(1, len(df) + 1))          # converts the list rows in a dataframe and add a column with index, and a range

            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("General statistics")   

            c1, c2, c3 = st.columns(3)                          
            c1.metric("Plant types", stats["Plant types"])
            c2.metric("Total plants", stats["Total plants"])
            c3.metric("Used area (m²)", stats["Used area (m²)"])

            c4, c5, c6 = st.columns(3)
            c4.metric("Total yield (kg)", stats["Total yield (kg)"])
            c5.metric("Yield/person", stats["Yield per person (kg)"])
            c6.metric("Avg. growth days", stats["Average growth time (days)"])

            # graph for the yield
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(df["Plant"], df["Yield/plant (kg)"], color="green")
            ax.set_title("Yield per plant")
            plt.xticks(rotation=30)                        # roteates a bit the names of the plants because are too long
            st.pyplot(fig)


# 2) PLANT EXPLORER

else:
    st.header("Plant Explorer")

    retriever = PlantInfoRetriever(plants_df)

    plant_choice = st.selectbox("Choose a plant:", sorted(plants_df["Name"].unique()))           # it creates a menu with the plants alphabetically sorted
    info = retriever.get_info(plant_choice)

    if "error" in info:
        st.error(info["error"])
    else:
        st.subheader(f"Information about {info['Name']}")

        st.write(f"**Category:** {info['Category']}")
        st.write(f"**Season:** {info['Season']}")
        st.write(f"**Origin:** {info['Origin']}")
        st.write(f"**Availability:** {info['Availability']}")
        st.write(f"**Shelf life:** {info['Shelf Life (days)']} days")
        st.write(f"**Storage:** {info['Storage Requirements']}")
        st.write(f"**Growing conditions:** {info['Growing Conditions']}")
        st.write(f"**Health benefits:** {info['Health Benefits']}")