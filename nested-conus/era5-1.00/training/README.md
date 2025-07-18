# Training

```
srun --jobid $SLURM_JOB_ID ~/aneml/slurm2ddp.sh anemoi-training train --config-name=config
```

* It's unclear if the `--jobid` flag is necessary, but it's used
  [here](https://github.com/stas00/ml-engineering/blob/master/orchestration/slurm/launchers/lightning-launcher.slurm)
  so why not
* the `slurm2ddp.sh` script maps SLURM environment variables to the PyTorch and
  PyTorch Lightning equivalents
* this works fine in `sbatch` but not in `salloc`, and I've tried manually
  passing the following flags to `srun` (suggested by chatgpt)
  * `ntasks`
  * `ntasks-per-node`
  * `cpus-per-task`
  * `gpus-per-node`
* Note that it's not clear to me how much of the specifications (`jobid`, and
  stuff in `slurm2ddp.sh`) is truly necessary, since I was debugging
  interactively and it magically worked with `sbatch`...

## Configuration

Using config.yaml to overwrite for:

- diagnostics
- hardware
- graph

These required enough modifications that I went in and changed their specific
yamls:
- data/zarr.yaml
- dataloader (although this one I also made some changes to the defaults)
- training/default.yaml

Note that graph is a bit confusing... I'm using the generated one, which is the
same as the graph that I created beforehand... but what if they were to be
inconsistent?

## Other TODO

- [ ] slurm `srun` command doesn't appear to be recognized...
    * when using `srun`, we still get the pytorch distributed warning that says
      `srun` is available but not used, and it looks like 4 independent training
      runs get launched...
- [ ] check global learning rate
- [ ] local `batch_size=2` for now... during training, larger in val
- [ ] outputs/ dir is getting written locally rather than in scratch... OK if
  it's just logs.
