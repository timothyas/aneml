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

### anemoi-datasets

```
cd ..
conda env create -f conda/datasets.yaml
conda activate anemoi-datasets

pip install --no-deps ./anemoi-utils[all]
pip install --no-deps ./anemoi-transform
```

Remove the zarr restriction from anemoi-datasets/pyproject.toml, then

```
pip install -e ./anemoi-datasets
```

### anemoi-graphs

First, copy the conda/datasets.yaml to conda/graphs.yaml, add all dependencies from anemoi-graphs to it


```
cd ..
conda env create -f conda/graphs.yaml
conda activate anemoi-graphs`

pip install --no-deps ./anemoi-utils[all]`
pip install --no-deps ./anemoi-transform`
pip install --no-deps ./anemoi-datasets[all]`
```

Remove all version restrictions on anemoi-graphs/pyproject.toml

```
pip install -e ./anemoi-graphs
```

Note, after first step, only conflicting package versions from what they specified is with h3
and torch geometric (both above the version the specify as max)
