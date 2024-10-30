import xarray

if __name__=="__main__":
    ds = xarray.open_zarr("gs://gcp-public-data-arco-era5/ar/1959-2022-1h-360x181_equiangular_with_poles_conservative.zarr")
    ds = ds.sel(time=slice("2021-01-01T00", "2021-01-01T12:00:00"))
    ds = ds[["surface_pressure", "2m_temperature", "10m_u_component_of_wind", "10m_v_component_of_wind", "temperature"]]
    ds = ds.sel(level=[500, 1000])
    ds.to_zarr("era5.zarr")

