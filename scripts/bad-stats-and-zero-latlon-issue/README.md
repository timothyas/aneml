# Bad Stats and Zero Lat/Lon Issue


1. The statistics / metrics values computed by anemoi-datasets are not what I
   would expect, particularly true with the forcing variables (my scratch notebooks in the
   test-vs-ufs2arco dir show that this is also true with the data variables).
2. Zero values in Latitude / Longitude arrays get replaced with NaNs.

Both of these are documented more fully
[in this issue](https://github.com/ecmwf/anemoi-datasets/issues/251)
