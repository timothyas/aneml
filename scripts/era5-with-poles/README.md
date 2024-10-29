# Testing with ERA5

```
anemoi-datasets create gcp-era5-recipe.yaml dataset.zarr
anemoi-graphs create graph.yaml data_nodes.pt
```

Using this version of ERA5:

```
"gs://gcp-public-data-arco-era5/ar/1959-2022-1h-360x181_equiangular_with_poles_conservative.zarr"
```

As it turns out, this is not a good idea because it has nodes at the poles,
which are defined for all longitudes.
This gives the graph generation process trouble, resulting in the following
error

```python
  File
"/home/tsmith/work/anemoi/anemoi-graphs/src/anemoi/graphs/nodes/attributes.py",
line 149, in get_raw_values
    sv = SphericalVoronoi(points, self.radius, self.centre, threshold=1e-16)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File
"/home/tsmith/miniconda3/envs/anemoi-graphs/lib/python3.11/site-packages/scipy/spatial/_spherical_voronoi.py",
line 189, in __init__
    raise ValueError("Duplicate generators present.")
ValueError: Duplicate generators present.
```

Removing the poles (and bumping the threshold of the SphericalVoronoi
calculations) fixes the issues.

## Timing

There is a serious issue with pulling remote data.
For reference I'm pulling 13 timestamps of 5x2D variables and a single 2 level 3D variable at
1 degree resolution.
The looks like


### Local

Pull the data, then transform it
```
python pull_data.py
anemoi-datasets create local-era5-recipe.yaml dataset.zarr
```

Takes < 1 minute to pull the data, and 7 seconds to create the dataset.

### Remote

Using the command at the top (just using the remote recipe), I killed it at 2
hours.
