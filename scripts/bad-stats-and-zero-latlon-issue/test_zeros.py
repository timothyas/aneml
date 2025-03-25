import xarray as xr
import numpy as np

if __name__ == "__main__":

    og = xr.open_zarr("zero-vals.zarr")
    ds = xr.open_zarr("anemoi.zeros.zarr")
    meshlats, meshlons = np.meshgrid(og.latitude, og.longitude)

    for key in ["latitudes", "longitudes"]:

        print(f"First 5 values in {key}")
        print(f"\t {ds[key].values[:5]}")

    print(f"\n\n --- Checking array values --- ")
    for key, expected in zip(
        ["latitude", "cos_latitude", "sin_latitude"],
        [
            meshlats.flatten(),
            np.cos(np.deg2rad(meshlats)).flatten(),
            np.sin(np.deg2rad(meshlats)).flatten(),
        ],
    ):

        idx = ds.attrs["variables"].index(key)

        array = ds["data"].sel(variable=idx).values.flatten()
        print(f"First 5 values in {key}")
        print(f"\tIn AnemoI: {array[:5]}")
        print(f"\tExpected: {expected[:5]}")


    for metric, func in zip(
        [
            "minimum",
            "maximum",
            "sums",
            "count",
        ],
        [
            np.nanmin,
            np.nanmax,
            np.nansum,
            lambda x : np.sum(~np.isnan(x)),
        ],
    ):
        print(f"\n\n --- Checking metric = {metric} --- ")
        for key, expected in zip(
            ["latitude", "cos_latitude", "sin_latitude"],
            [
                func(ds["latitudes"].values),
                func(np.cos(np.deg2rad(ds["latitudes"].values))),
                func(np.sin(np.deg2rad(ds["latitudes"].values))),
            ],
        ):

            idx = ds.attrs["variables"].index(key)

            array = ds[metric].sel(variable=idx).values
            print(f"{key}")
            print(f"\t Anemoi: {array}, Expected: {expected}")
