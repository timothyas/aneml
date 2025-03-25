# Preprocessing

1. Create the dataset using `submit_ufs2arco.sh`

2. Create the graph with
  ```
  workdir=/pscratch/sd/t/timothys/aneml/nested-conus/era5-1.00
  anemoi-graphs create recipe.multi_scale_graph.yaml ${workdir}/multi_scale_graph.pt
  ```
