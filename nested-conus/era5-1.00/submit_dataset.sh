#!/bin/bash

#SBATCH -J era5-1.00
#SBATCH -o slurm/dataset.%j.out
#SBATCH -e slurm/dataset.%j.err
#SBATCH --nodes=1
#SBATCH --tasks-per-node=12
#SBATCH --cpus-per-task=20
#SBATCH --qos=regular
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 24:00:00

log_dir=$COMMUNITY/aneml/logs
output_path=$WORK/aneml/one-year.era5-1.00-degree.zarr

mkdir -p $log_dir

conda activate anemoi-datasets
anemoi-datasets init recipe.dataset.yaml $output_path --overwrite > "$log_dir/init.log" 2>&1

for i in $(seq 1 $SLURM_NTASKS); do
  srun -n 1 anemoi-datasets load "$output_path" --part "$i/$SLURM_NTASKS" > "$log_dir/part_${i}.log" 2>&1 &
done

wait
