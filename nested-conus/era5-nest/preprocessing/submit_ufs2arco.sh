#!/bin/bash

#SBATCH -J era5-nest
#SBATCH -o /pscratch/sd/t/timothys/aneml/nested-conus/era5-nest/slurm/preprocessing.%j.out
#SBATCH -e /pscratch/sd/t/timothys/aneml/nested-conus/era5-nest/slurm/preprocessing.%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=4
#SBATCH --qos=debug
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 00:30:00

conda activate ufs2arco
export PYTHONPATH=""
python create_global_grid.py
srun ufs2arco recipe.global.yaml
srun ufs2arco recipe.conus.yaml
