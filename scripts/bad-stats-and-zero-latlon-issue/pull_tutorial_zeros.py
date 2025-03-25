import xarray as xr
import numpy as np

import pooch # needed for tutorial dataset

if __name__ == "__main__":

    ds = xr.tutorial.load_dataset("air_temperature")

    ds = ds.rename({"lat": "latitude", "lon": "longitude", "air": "temperature"})

    ds = ds.transpose("time", "longitude", "latitude")

    # shift the data so that we get a zero value in longitude and latitude
    ds["zlon"] = xr.DataArray(
        ds.longitude.values - ds.longitude.values[0],
        coords=ds["longitude"].coords,
    )
    ds["zlat"] = xr.DataArray(
        ds.latitude.values - ds.latitude.values[0],
        coords=ds["latitude"].coords,
    )
    for key, val in zip(["zlon", "zlat"], ["longitude", "latitude"]):
        ds = ds.set_coords(key)
        ds = ds.swap_dims({val: key})
        ds = ds.drop(val)
        ds = ds.rename({key: val})

    ds.to_zarr("zero-vals.zarr")
