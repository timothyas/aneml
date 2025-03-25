import xarray as xr
import numpy as np

if __name__ == "__main__":

    lonlat = xr.open_zarr("anemoi.lonlat.zarr")
    latlon = xr.open_zarr("anemoi.latlon.zarr")

    for key in ["latitudes", "longitudes"]:

        print(f"First 10 values in {key}")
        print(f"\t in lonlat = {lonlat[key].values[:10]}")
        print(f"\t in latlon = {latlon[key].values[:10]}")
        isequal = (lonlat[key] == latlon[key]).all().values
        print(f"{key} is equal = {isequal}")

    for key in ["cos_latitude", "cos_longitude", "temperature"]:

        ilonlat = lonlat.attrs["variables"].index(key)
        ilatlon = latlon.attrs["variables"].index(key)

        isclose = np.allclose(
            lonlat["data"].sel(variable=ilonlat),
            latlon["data"].sel(variable=ilatlon),
        )
        print(f"{key} is close = {isclose}")
