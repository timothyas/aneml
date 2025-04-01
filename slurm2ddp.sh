#! /bin/bash
export RANK=$SLURM_PROCID
export WORLD_RANK=$SLURM_PROCID
export GLOBAL_RANK=$SLURM_PROCID
export LOCAL_RANK=$SLURM_LOCALID
export WORLD_SIZE=$SLURM_NTASKS
export MASTER_PORT=29500 # default from torch launcher
export MASTER_ADDR=$(scontrol show hostnames $SLURM_NODELIST | head -n 1)
exec $*
