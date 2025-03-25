# Training

```
anemoi-training train --config-name=config
```

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

## TODO

- [ ] check global learning rate
- [ ] local `batch_size=2` for now... during training, larger in val
