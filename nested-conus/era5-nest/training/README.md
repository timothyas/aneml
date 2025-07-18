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

## Model

```
[2025-04-14 16:06:30,021][pytorch_lightning.callbacks.model_summary][INFO] -
  | Name    | Type                 | Params | Mode
---------------------------------------------------------
0 | model   | AnemoiModelInterface | 66.9 M | train
1 | loss    | WeightedMSELoss      | 0      | train
2 | metrics | ModuleList           | 0      | train
---------------------------------------------------------
66.9 M    Trainable params
0         Non-trainable params
66.9 M    Total params
267.663   Total estimated model params size (MB)
305       Modules in train mode
0         Modules in eval mode
```
