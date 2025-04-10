# Training

```
srun --jobid $SLURM_JOB_ID ~/aneml/slurm2ddp.sh anemoi-training train --config-name=config
```

These are taken from the working global era5 1 degree setup, but with:
* `graphs/stretched_grid.yaml`
* `models/graphtransformer.yaml`
* and other mods to the main config/debug yaml files

Anything marked with a `#???` means I have no idea what that should be, likely
stemming from the stretched/nested setup defaults.
