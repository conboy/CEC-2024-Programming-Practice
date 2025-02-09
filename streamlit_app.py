import streamlit as st
import plotly.express as px
from modules.combine_data import combine_data
from modules.calculate_mineability import calculate_mineability

dataset_folder = "./data"                               # Folder containing the material dataset files
combined_data_file = "./data/combined_data.csv"         # File to store the combined data from the dataset_folder
mineability_data_file = "./data/mineability_data.csv"   # File to store the mineability data
materials = ["coral", "species", "ship", "oil", "metal", "helium"]

st.set_page_config(layout="wide")

st.title("Mineability Calculator")

# User inputs for preserve and obtain lists on the sidebar
st.sidebar.header("Material Selection")
preserve_list = st.sidebar.multiselect(
    "Select materials to preserve:",
    options=["coral", "species", "ship"],
    default=["coral", "species"]
)

obtain_list = st.sidebar.multiselect(
    "Select materials to obtain:",
    options=["oil", "metal", "helium", "ship"],
    default=["oil", "metal", "helium", "ship"]
)

# Ensure 'ship' is only in one of the lists
if "ship" in preserve_list and "ship" in obtain_list:
    st.error("The 'ship' material can only be in preserve or obtain.\nIt is currently not being considered in the mineability calculation to avoid unexpected behavior.")
    preserve_list.remove("ship")
    obtain_list.remove("ship")

# User inputs for scaling factors on the sidebar
st.sidebar.header("Scaling Factors")
st.sidebar.text("Used to adjust the importance of each desirable material in the mineability calculation")

scaling_factors = {}
for material in obtain_list:
    scaling_factors[material] = st.sidebar.slider(
        f"{material}",
        min_value=0.0,
        max_value=100.0,
        value=1.0,
        step=0.1
    )


# Combine all the material datasets that end with '_array_data.csv' into a single CSV file and Dataframe
combined_material_df = combine_data(
    dataset_folder = dataset_folder, 
    output_file = combined_data_file,
    scaling_factors = scaling_factors
)

# Calculate the mineability of each coordinate based on the preserve and obtain lists
mineability_df = calculate_mineability(
    combined_df = combined_material_df, 
    preserve_list = preserve_list, 
    obtain_list = obtain_list,
    output_file = mineability_data_file
)

st.subheader("Mineability Equation")
st.text("This is the equation used to calculate the mineability of each coordinate based on the selected materials and scaling factors.")

preserve_eq = "\\text{{ or }}".join([f"\\text{{{{{material}}}}} > 0 \\text{{ or }} \\text{{{{{material}}}}} \\text{{ is NaN}}" for material in preserve_list])
obtain_eq = " + ".join([f"\\text{{{{{material}}}}} * {scaling_factors[material]}" for material in obtain_list])

equation = f"""
\\text{{mineability}} = \\begin{{cases}} 0 & \\text{{if }} {preserve_eq} \\\\
{obtain_eq} & \\text{{otherwise}}
\\end{{cases}}
"""
st.latex(equation)

st.subheader("Grid Visualization")
st.text("""
This is the mineability visualization of the 100x100 grid. Darker colors represent higher mineability.
💡 You can fullscreen this plot to see the grid in more detail.        
""")

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
st.subheader("Results Dataframe")
st.text("""
This is the dataframe containing the calculated mineability data as well as material values for their respective coordinate.
💡 Click the 'mineability' column header to sort to see the least and most mineable coordinates.
""")
st.dataframe(mineability_df, use_container_width=True)