import xarray

if __name__=="__main__":

    # ERA5
    ds = xarray.open_zarr("gs://gcp-public-data-arco-era5/ar/1959-2022-1h-360x181_equiangular_with_poles_conservative.zarr")
    ds = ds.sel(time=slice("2017-01-01T00", "2017-01-02T18:00:00"))
    ds = ds[["land_sea_mask", "geopotential_at_surface", "surface_pressure", "2m_temperature", "temperature", "geopotential"]]
    ds.to_zarr("era5.zarr")


    # GEFS
    ds = xarray.open_zarr("/home/tsmith/work/ufs2arco/examples/gefs/sample-gefs.zarr")
    ds = ds.isel(t0=slice(8))
    ds = ds.sel(fhr=0, drop=True)
    ds = ds.sel(member=slice(2))
    ds = ds[["lsm", "orog", "sp", "t2m", "t", "gh"]]
    ds = ds.drop_vars("valid_time")
    ds = ds.rename({"t0": "time"})
    ds["time"].attrs = {}
    ds = ds.rename({"pressure": "level"})
    ds = ds.rename({"member": "number"})
    chunks = {"time": 1, "number": 1, "level": 1, "longitude": -1, "latitude": -1}
    ds = ds.chunk(chunks)
    for key in ds.data_vars:

        ds[key] = ds[key].chunk({k: c for k, c in chunks.items() if k in ds[key].dims})
        ds[key].encoding = {}
    ds.to_zarr("gefs.zarr")
