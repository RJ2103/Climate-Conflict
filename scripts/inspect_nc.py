import xarray as xr

nc_path = r"data\raw\temperature\gistemp250_GHCNv4.nc"

ds = xr.open_dataset(nc_path)

print("DATASET OVERVIEW")
print(ds)
print("\nVARIABLES")
print(ds.data_vars)
print("\nCOORDINATES")
print(ds.coords)