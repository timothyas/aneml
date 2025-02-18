import os
import sys
sys.path.append("/global/homes/t/timothys/aneml")
from aneml.utils import generate_slurm_scripts

if __name__ == "__main__":

    COMMUNITY = os.getenv('COMMUNITY')
    WORK = os.getenv('WORK')
    pwd = os.getenv("PWD")

    job_name = "era5-1.00-degree-with-forcings"
    this_work = f"{WORK}/aneml/{job_name}"

    recipe_path = f"{pwd}/recipe.dataset.yaml"
    log_dir = f"{this_work}/logs-slurm-1yr"
    output_path = f"{this_work}/slurm.1yr.zarr"

    load_options = {
        "nodes": 1,
        "array_tasks": 12,
        "cpus-per-task": 20,
        "time": "04:00:00",
    }

    generate_slurm_scripts(job_name, recipe_path, log_dir, output_path, load_options)
