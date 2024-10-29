# AnemoI

The way I'm doing this for now...

For each of the subpackages (e.g. anemoi-datasets)
create a yaml with all the dependencies for this, including dependencies from
anemoi subdependencies

So e.g. for anemoi-datasets, this yaml includes dependencies for

- anemoi-datasets
- anemoi-utils
- anemoi-transform

For anemoi-graphs, this would have

- anemoi-graphs
- anemoi-datasets
- anemoi-utils
- anemoi-transform

## Versions

I'm not restricting versions, since pip installing anemoi-datasets caused fsspec
problems with gcsfs... need to raise this issue


## Work environment

The idea is that each environment is installed as editable, while the
subpackages are installed with pip and no-deps.

So for example:

- anemoi-datasets
    - First, remove the zarr restriction from pyproject.toml, then
    - `pip install --no-deps ./anemoi-utils[provenance]`
    - `pip install --no-deps ./anemoi-transform`
    - `pip install -e anemoi-datasets
    - Interestingly, this removed:
        - some earthkit-data and earthkit meteo version 0.0.0
        - my local install of anemoi-utils (but not anemoi-transform), probably
          because the local install has some 0.1.dirty version, not >0.4.1 as
          required
        - This is because of the way the version is handled, somehow. The
          "dev" version is out of sync with the pip version.

- anemoi-graphs
    - Copy the conda/dataset.yaml, add all dependencies from anemoi-graphs to it
        * `conda env create -f conda/graphs.yaml`
        * only conflicting package versions from what they specified is with h3
          and torch geometric (both above the version the specify as max)
    - Remove the version requirements on anemoi-utils and anemoi-datasets from
      pyproject.toml
    - Remove all version requirements...
    - `pip install --no-deps ./anemoi-utils[all]`
    - `pip install --no-deps ./anemoi-transform`
    - `pip install --no-deps ./anemoi-datasets[all]`
    - `pip install -e anemoi-graphs`
