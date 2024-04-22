import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load data
# Find Data from https://www.eia.gov/electricity/data/eia860/
excel_file_path = '3_4_Energy_Storage_Y2022.xlsx'
df = pd.read_excel(excel_file_path, header=1, sheet_name=0)
df = df[df['Storage Technology 1']=='LIB']
df = df[['County', 'State', 'Storage Technology 1', 'Nameplate Energy Capacity (MWh)']]
df.dropna(subset=['Nameplate Energy Capacity (MWh)'], inplace=True)
df['Nameplate Energy Capacity (MWh)'] = pd.to_numeric(df['Nameplate Energy Capacity (MWh)'], errors='coerce')
df.dropna(subset=['Nameplate Energy Capacity (MWh)'], inplace=True)
grouped_df = df.groupby(['County', 'State'])['Nameplate Energy Capacity (MWh)'].sum().reset_index()

# Get county location data
shp_data = gpd.read_file('/Users/gebingbing/Downloads/tl_2022_us_county/tl_2022_us_county.shp')
merged_data = shp_data.merge(grouped_df, how='left', left_on='NAME', right_on='County')

# Plot data
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
shp_data.boundary.plot(ax=ax, linewidth=0.1, color='lightgray')
merged_data.plot(column='Nameplate Energy Capacity (MWh)', cmap='Blues', linewidth=0.1, ax=ax, edgecolor='lightgray', legend=True, k=5)
ax.set_xlim([-130, -60])
ax.set_ylim([25, 50])
plt.title('Nameplate Energy Capacity by County in United States')
plt.show()
