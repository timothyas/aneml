#!/bin/bash

#SBATCH -J era5-1.00
#SBATCH -o slurm/processes.3mo.%j.out
#SBATCH -e slurm/processes.3mo.%j.err
#SBATCH --nodes=1
#SBATCH --tasks=1
#SBATCH --cpus-per-task=256
#SBATCH --qos=debug
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 00:30:00

log_dir=$COMMUNITY/aneml/era5-1.00-degree/logs-3mo
output_path=$WORK/aneml/era5-1.00-degree/3mo.processes.zarr

mkdir -p $log_dir

conda activate anemoi-datasets
time anemoi-datasets create recipe.dataset.yaml "$output_path" --overwrite --processes 12 > "$log_dir/processes.log" 2>&1
