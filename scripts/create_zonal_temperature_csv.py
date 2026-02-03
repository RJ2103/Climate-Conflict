import xarray as xr
import pandas as pd
import numpy as np

ds = xr.open_dataset(r"C:\Users\Admin\Desktop\TheObservable\Climate-Conflict\data\raw\temperature\gistemp250_GHCNv4.nc")

temp = ds['tempanomaly']

## Assign Year Coordinate

temp = temp.assign_coords(year=temp['time'].dt.year)

# Define latitude bands
lat_bands = {
    "90S_64S": (-90, -64),
    "64S_44S": (-64, -44),
    "44S_24S": (-44, -24),
    "24S_EQU": (-24, 0),
    "EQU_24N": (0, 24),
    "24N_44N": (24, 44),
    "44N_64N": (44, 64),
    "64N_90N": (64, 90),
}


rows = []


for band, (lat_min, lat_max) in lat_bands.items():
    band_data = temp.sel(lat=slice(lat_min, lat_max))

    # Area weights
    weights = np.cos(np.deg2rad(band_data["lat"]))

    
    # Annual, area-weighted mean
    annual_band = (band_data.weighted(weights).mean(dim=["lat", "lon"]).groupby("year").mean())

    
    df = annual_band.to_dataframe(name="temp_anomaly").reset_index()
    df["latitude_band"] = band

    rows.append(df)

# Combine all bands
zonal_df = pd.concat(rows, ignore_index=True)

# Save
output_path = "data/processed/temperature_zonal_annual.csv"
zonal_df.to_csv(output_path, index=False)

print(f"Saved: {output_path}")
print(zonal_df.head())


