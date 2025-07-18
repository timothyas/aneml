# 1 degree test setup


It's hard to get this to scale, and the issues are tangled:
* building incrementally relies on running completely different jobs
    * inside the same slurm script, had trouble running each part in the
      background
    * using a slurm job array amounts to submitting many small slurm jobs,
      which is really suboptimal for perlmutter
* the `--threads` and `--processes` options don't map to the incremental build
  and it's not clear how much these help, and they do not map onto the slurm
  infrastructure
