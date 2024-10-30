# ERA5 Light

Testing setup, reading from the ~3 degree dataset here: `"gs://gcp-public-data-arco-era5/ar/1959-2022-6h-128x64_equiangular_conservative.zarr"`


Created dataset and graph with

```
python pull_data.py
anemoi-datasets create recipe.dataset.yaml dataset.zarr
anemoi-graphs create recipe.graph.yaml data_nodes.pt
```
