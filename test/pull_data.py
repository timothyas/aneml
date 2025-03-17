import xarray

if __name__=="__main__":

    # ERA5
    #ds = xarray.open_zarr("gs://gcp-public-data-arco-era5/ar/1959-2022-1h-360x181_equiangular_with_poles_conservative.zarr")
    #ds = ds.sel(time=slice("2021-01-01T00", "2021-01-01T12:00:00"))
    #ds = ds[["surface_pressure", "2m_temperature", "10m_u_component_of_wind", "10m_v_component_of_wind", "temperature"]]
    #ds.to_zarr("era5.zarr")


    # GEFS
    ds = xarray.open_zarr("/home/tsmith/work/ufs2arco/examples/gefs/sample-gefs.zarr")
    ds = ds.isel(t0=slice(8))
    ds = ds.sel(fhr=0, drop=True)
    ds = ds.sel(member=slice(2))
    ds = ds[["sp", "t2m", "u10", "v10", "t"]]
    ds = ds.drop_vars("valid_time")
    ds = ds.rename({"t0": "time"})
    ds["time"].attrs = {}
    ds = ds.rename({"pressure": "level"})
    ds = ds.rename({"member": "number"})
    ds.to_zarr("gefs.zarr")
