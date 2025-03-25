#!/bin/bash

#SBATCH -J era5-1.00-1year
#SBATCH -o /pscratch/sd/t/timothys/aneml/nested-conus/era5-1.00/slurm/1year.%j.out
#SBATCH -e /pscratch/sd/t/timothys/aneml/nested-conus/era5-1.00/slurm/1year.%j.err
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=2
#SBATCH --qos=debug
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 00:30:00

conda activate /global/common/software/m4718/timothys/graphufs
export PYTHONPATH=~/ufs2arco
srun python -c "from ufs2arco.driver import Driver; Driver('recipe.ufs2arco.yaml').run()"
