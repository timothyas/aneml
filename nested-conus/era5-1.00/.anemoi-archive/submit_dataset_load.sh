#!/bin/bash

#SBATCH -J era5-1.00
#SBATCH -o slurm/dataset_load.1yr.%j.out
#SBATCH -e slurm/dataset_load.1yr.%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --array=1-12
#SBATCH --qos=regular
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 03:00:00

log_dir=$COMMUNITY/aneml/era5-1.00-degree/logs-slurm-1yr
output_path=$WORK/aneml/era5-1.00-degree/slurm.1yr.zarr

mkdir -p $log_dir

conda activate anemoi-datasets
srun anemoi-datasets load "$output_path" --part "$SLURM_ARRAY_TASK_ID/12" > "$log_dir/part_$SLURM_ARRAY_TASK_ID.log" 2>&1
