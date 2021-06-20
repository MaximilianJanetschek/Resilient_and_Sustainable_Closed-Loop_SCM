import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

plz_shape_df = gpd.read_file('Data/plz-gebiete.shp', dtype={'plz': str})

plz_shape_df.head()
plt.rcParams['figure.figsize'] = [16, 11]

# Get lat and lng of Germany's main cities.
top_cities = {
    'Berlin': (13.404954, 52.520008),
    'Cologne': (6.953101, 50.935173),
    'Düsseldorf': (6.782048, 51.227144),
    'Frankfurt am Main': (8.682127, 50.110924),
    'Hamburg': (9.993682, 53.551086),
    'Leipzig': (12.387772, 51.343479),
    'Munich': (11.576124, 48.137154),
    'Dortmund': (7.468554, 51.513400),
    'Stuttgart': (9.181332, 48.777128),
    'Nuremberg': (11.077438, 49.449820),
    'Hannover': (9.73322, 52.37052)
}

fig, ax = plt.subplots()

plz_shape_df.plot(ax=ax, color='orange', alpha=0.8)

fig, ax = plt.subplots()

plz_shape_df.plot(ax=ax, color='orange', alpha=0.8)

# Plot cities.
for c in top_cities.keys():
    # Plot city name.
    ax.text(
        x=top_cities[c][0],
        # Add small shift to avoid overlap with point.
        y=top_cities[c][1] + 0.08,
        s=c,
        fontsize=12,
        ha='center',
    )
    # Plot city location centroid.
    ax.plot(
        top_cities[c][0],
        top_cities[c][1],
        marker='o',
        c='black',
        alpha=0.5
    )

ax.set(
    title='Germany',
    aspect=1.3,
    facecolor='lightblue'
)

# Create feature.
plz_shape_df = plz_shape_df \
    .assign(first_dig_plz = lambda x: x['plz'].str.slice(start=0, stop=1))

fig, ax = plt.subplots()

plz_shape_df.plot(
    ax=ax,
    column='first_dig_plz',
    categorical=True,
    legend=True,
    legend_kwds={'title':'First Digit', 'loc':'lower right'},
    cmap='tab20',
    alpha=0.9
)

# Merge data.
plz_region_df = pd.read_csv(
    'Data/zuordnung_plz_ort.csv',
    sep=',',
    dtype={'plz': str}
)

plz_region_df.drop('osm_id', axis=1, inplace=True)

germany_df = pd.merge(
    left=plz_shape_df,
    right=plz_region_df,
    on='plz',
    how='inner'
)

germany_df.drop(['note'], axis=1, inplace=True)

plz_einwohner_df = pd.read_csv(
    'Data/plz_einwohner.csv',
    sep=',',
    dtype={'plz': str, 'einwohner': int}
)

# Merge data.
germany_df = pd.merge(
    left=germany_df,
    right=plz_einwohner_df,
    on='plz',
    how='left'
)

germany_df.head()

fig, ax = plt.subplots()

germany_df.plot(
    ax=ax,
    column='einwohner',
    categorical=False,
    legend=True,
    cmap='autumn_r',
    alpha=0.8
)

for c in top_cities.keys():
    ax.text(
        x=top_cities[c][0],
        y=top_cities[c][1] + 0.08,
        s=c,
        fontsize=12,
        ha='center',
    )

    ax.plot(
        top_cities[c][0],
        top_cities[c][1],
        marker='o',
        c='black',
        alpha=0.5
    )

ax.set(
    title='Germany: Number of Inhabitants per Postal Code',
    aspect=1.3,
    facecolor='lightblue'
);

