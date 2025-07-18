#!/bin/bash

#SBATCH -J era5-1.00
#SBATCH -o slurm/mpi.1yr.%j.out
#SBATCH -e slurm/mpi.1yr.%j.err
#SBATCH --nodes=2
#SBATCH --tasks-per-node=6
#SBATCH --cpus-per-task=20
#SBATCH --qos=regular
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 03:00:00

log_dir=$COMMUNITY/aneml/era5-1.00-degree/logs-1yr-mpi
output_path=$WORK/aneml/era5-1.00-degree/mpi.1yr.zarr

mkdir -p $log_dir

conda activate anemoi-datasets
module swap PrgEnv-nvidia PrgEnv-gnu
srun anemoi-datasets create recipe.dataset.yaml "$output_path" --overwrite --mpi > "$log_dir/mpi.log" 2>&1
