#!/bin/bash

#SBATCH -J era5-1.00
#SBATCH -o slurm/dataset_finalise.1yr.%j.out
#SBATCH -e slurm/dataset_finalise.1yr.%j.err
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

# these take 1 sec for 1 yr of data
anemoi-datasets finalise "$output_path" > "$log_dir/finalise.log" 2>&1
anemoi-datasets init-additions "$output_path" > "$log_dir/init_additions.log" 2>&1

# this could be split into parts, but took ~1min on 1 yr of data
anemoi-datasets load-additions $output_path > $log_dir/load_additions.log 2>&1

# these were again trivial
anemoi-datasets finalise-additions $output_path > $log_dir/finalise_additions.log 2>&1
anemoi-datasets cleanup $output_path 
