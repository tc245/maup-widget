import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns

# Set up the app layout
st.title("Modifiable Areal Unit Problem (MAUP) Demonstration")

# Create a synthetic dataset
np.random.seed(0)
num_points = 100
x = np.random.uniform(0, 100, num_points)
y = np.random.uniform(0, 100, num_points)
values = np.random.uniform(0, 100, num_points)

df = pd.DataFrame({'x': x, 'y': y, 'value': values})

# Sidebar for user input
st.sidebar.header("Settings")
num_units = st.sidebar.slider("Number of Grid Units", min_value=5, max_value=20, value=10)

# Create a grid and aggregate data
def aggregate_data(df, num_units):
    grid_size = 100 / num_units
    df['grid_x'] = (df['x'] // grid_size).astype(int)
    df['grid_y'] = (df['y'] // grid_size).astype(int)
    grouped = df.groupby(['grid_x', 'grid_y']).agg({'value': 'mean'}).reset_index()
    return grouped, grid_size

grouped_df, grid_size = aggregate_data(df, num_units)

# Visualization
fig, ax = plt.subplots(figsize=(10, 10))
scatter = ax.scatter(df['x'], df['y'], c=df['value'], cmap='viridis', s=50, alpha=0.7, edgecolors='w')
plt.colorbar(scatter, ax=ax, label='Point Value')

# Draw grid
for i in range(num_units):
    for j in range(num_units):
        rect = Rectangle((i * grid_size, j * grid_size), grid_size, grid_size, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

# Draw aggregated values
for _, row in grouped_df.iterrows():
    rect = Rectangle((row['grid_x'] * grid_size, row['grid_y'] * grid_size), grid_size, grid_size, 
                     linewidth=1, edgecolor='black', facecolor=sns.color_palette("viridis", as_cmap=True)(row['value'] / 100))
    ax.add_patch(rect)

ax.set_title('Point Values and Aggregated Grid Cells')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
st.pyplot(fig)

# Display aggregated statistics
mean_value = grouped_df['value'].mean()
st.write(f"Mean Aggregated Value: {mean_value:.2f}")

# Additional insights
st.markdown("### Insights:")
st.markdown("As the number of grid units increases, you can observe how the aggregation of point values changes. This demonstrates the Modifiable Areal Unit Problem (MAUP), where the results of spatial analyses can vary depending on how the geographic units are defined.")