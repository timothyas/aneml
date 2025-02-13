#!/bin/bash

#SBATCH -J era5-1.00
#SBATCH -o slurm/dataset_init.1yr.%j.out
#SBATCH -e slurm/dataset_init.1yr.%j.err
#SBATCH --nodes=1
#SBATCH --tasks=1
#SBATCH --cpus-per-task=64
#SBATCH --qos=debug
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 00:30:00

log_dir=$COMMUNITY/aneml/era5-1.00-degree/logs-slurm-1yr
output_path=$WORK/aneml/era5-1.00-degree/slurm.1yr.zarr

mkdir -p $log_dir

conda activate anemoi-datasets
anemoi-datasets init recipe.dataset.yaml "$output_path" --overwrite > "$log_dir/init.log" 2>&1
