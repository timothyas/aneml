import xarray as xr
import numpy as np

import pooch # needed for tutorial dataset

if __name__ == "__main__":

    ds = xr.tutorial.load_dataset("air_temperature")

    ds = ds.rename({"lat": "latitude", "lon": "longitude"})

    latlon = ds.air.transpose("time", "latitude", "longitude")
    lonlat = ds.air.transpose("time", "longitude", "latitude")

    latlon.to_dataset(name="temperature").to_zarr("latlon.zarr")
    lonlat.to_dataset(name="temperature").to_zarr("lonlat.zarr")
