import streamlit as st
import plotly.express as px
from modules.nav import Navbar
from modules.combine_data import combine_data
from modules.calculate_mineability import calculate_mineability

dataset_folder = "./data"                               # Folder containing the material dataset files
combined_data_file = "./data/combined_data.csv"         # File to store the combined data from the dataset_folder
mineability_data_file = "./data/mineability_data.csv"   # File to store the mineability data

Navbar()
st.title("Mineability Calculator")

# User inputs for preserve and obtain lists
preserve_list = st.multiselect(
    "Select materials to preserve:",
    options=["coral", "species", "ship"],
    default=["coral", "species"]
)

obtain_list = st.multiselect(
    "Select materials to obtain:",
    options=["oil", "metal", "helium", "ship"],
    default=["oil", "metal", "helium", "ship"]
)

# Ensure 'ship' is only in one of the lists
if "ship" in preserve_list and "ship" in obtain_list:
    st.error("The 'ship' material can only be in preserve or obtain.\nIt is currently not being considered in the mineability calculation.")
    preserve_list.remove("ship")
    obtain_list.remove("ship")

# Combine all the material datasets that end with '_array_data.csv' into a single CSV file and Dataframe
combined_material_df = combine_data(
    dataset_folder = dataset_folder, 
    output_file = combined_data_file
)

# Calculate the mineability of each coordinate based on the preserve and obtain lists
mineability_df = calculate_mineability(
    combined_df = combined_material_df, 
    preserve_list = preserve_list, 
    obtain_list = obtain_list,
    output_file = mineability_data_file
)

# Create a plotly express scatter plot with square markers
fig = px.scatter(
    mineability_df,
    x='x',
    y='y',
    color='mineability',
    hover_data=mineability_df.columns.to_list(),
    symbol_sequence=['square'],
)

# Update the layout to make the markers appear as pixels
fig.update_traces(marker=dict(size=5))
fig.update_layout(
    xaxis=dict(scaleanchor="y", scaleratio=1),
    yaxis=dict(scaleanchor="x", scaleratio=1)
)

# Display the plot in the Streamlit app
st.plotly_chart(fig)
st.subheader("Results")
st.text("This is the dataframe containing the calculated mineability data.")
st.text("Click the 'mineability' column header to see the most mineable coordinates.")
st.dataframe(mineability_df, use_container_width=True)