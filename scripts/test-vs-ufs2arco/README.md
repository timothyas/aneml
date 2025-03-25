# Test setup for new anemoi-datasets creation

1. Use `pull_data.py` to pull in a tiny sample dataset
2. Run anemoi datasets to create the anemoi datasets
  ```
  anemoi-datasets create recipe.era5.yaml anemoi.era5.zarr --overwrite
  anemoi-datasets create recipe.gefs.yaml anemoi.gefs.zarr --overwrite
  ```

This culminated in
[this ufs2arco feature](https://github.com/NOAA-PSL/ufs2arco/pull/32)
