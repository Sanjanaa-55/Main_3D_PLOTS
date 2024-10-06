import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data
data = pd.read_csv('large_ocean_depletion_factors.csv')

# Streamlit page layout
st.title('Ocean Depletion Factors Dashboard')

# Dropdown to select region
selected_region = st.selectbox('Select Region', data['Region'].unique())

# Range slider for CO2 levels
co2_range = st.slider(
    'Select CO2 Level Range', 
    float(data['CO2_level'].min()), 
    float(data['CO2_level'].max()), 
    (float(data['CO2_level'].min()), float(data['CO2_level'].max()))  # Set default range
)

# Filter data based on user input
filtered_data = data[
    (data['Region'] == selected_region) & 
    (data['CO2_level'] >= co2_range[0]) & 
    (data['CO2_level'] <= co2_range[1])
]

# Display filtered data
st.write('Filtered Data', filtered_data)

# Plotting with Plotly for interactivity (3D plot) with custom color scale (Pink, Yellow, etc.)
fig = px.scatter_3d(filtered_data, 
                    x='Latitude', 
                    y='Longitude', 
                    z='CO2_level', 
                    color='Water_temperature', 
                    size='Chemical_contamination',
                    hover_name='Region', 
                    title=f'Ocean Depletion Factors in {selected_region}: CO2 Levels vs Water Temperature and Contamination',
                    color_continuous_scale=[
                        [0, "pink"],  # lower end (water temperature)
                        [0.5, "yellow"],  # mid-range
                        [1, "red"]  # upper end
                    ],
                    labels={
                        'Latitude': 'Latitude',
                        'Longitude': 'Longitude',
                        'CO2_level': 'CO2 Level',
                        'Water_temperature': 'Water Temperature (°C)',
                        'Chemical_contamination': 'Chemical Contamination (mg/L)'
                    })

# Customize Plotly layout
fig.update_layout(scene=dict(
                    xaxis_title='Latitude',
                    yaxis_title='Longitude',
                    zaxis_title='CO2 Level'),
                  coloraxis_colorbar=dict(title="Water Temperature"))

# Show Plotly interactive plot in Streamlit
st.plotly_chart(fig)
