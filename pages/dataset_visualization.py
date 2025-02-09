import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from modules.nav import Navbar

Navbar()

display_rows = ["coral_value", "helium_value", "metal_value", "oil_value", "ship_value", "species_value"]

# Load csv
df = pd.read_csv("data/combined_data.csv")

for display_row in display_rows:
    # Create 100x100 matrix
    matrix = np.zeros((100, 100))

    # Populate matrix
    for _, row in df.iterrows():
        x, y, value = int(row["x"]), int(row["y"]), row[display_row]
        matrix[x, y] = value

    # Display the matrix using plotly imshow
    fig = px.imshow(matrix, labels=dict(color=display_row), title=display_row)
    st.plotly_chart(fig)