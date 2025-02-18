import os

def generate_slurm_scripts(job_name, recipe_path, log_dir, output_path, load_options=None):

    slurm_dir = f"{log_dir}/slurm"
    for d in [log_dir, slurm_dir, "job-scripts"]:
        os.makedirs(d, exist_ok=True)

    print("Creating scripts for ...")
    print(f"\tjob_name = {job_name}")
    print(f"\trecipe_path = {recipe_path}")
    print(f"\tlog_dir = {log_dir}")
    print(f"\toutput_path = {output_path}")

    load_options = dict() if load_options is None else load_options
    n_nodes = load_options.get("nodes", 1)
    n_array_tasks = load_options.get("array_tasks", 1)
    array = f"1-{n_array_tasks}"
    load_time = load_options.get("time", "03:00:00")

    scripts = {
        "submit_dataset_init.sh": f"""#!/bin/bash

#SBATCH -J {job_name}
#SBATCH -o {slurm_dir}/dataset_init.%j.out
#SBATCH -e {slurm_dir}/dataset_init.%j.err
#SBATCH --nodes=1
#SBATCH --tasks=1
#SBATCH --cpus-per-task=64
#SBATCH --qos=debug
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 00:30:00

conda activate anemoi-datasets
anemoi-datasets init {recipe_path} {output_path} --overwrite > "{log_dir}/init.log" 2>&1
""",

        "submit_dataset_load.sh": f"""#!/bin/bash

#SBATCH -J {job_name}
#SBATCH -o {slurm_dir}/dataset_load.%j.out
#SBATCH -e {slurm_dir}/dataset_load.%j.err
#SBATCH --nodes={n_nodes}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --array={array}
#SBATCH --qos=regular
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t {load_time}

conda activate anemoi-datasets
srun anemoi-datasets load {output_path} --part "$SLURM_ARRAY_TASK_ID/{n_array_tasks}" > "{log_dir}/part_$SLURM_ARRAY_TASK_ID.log" 2>&1
""",

        "submit_dataset_finalise.sh": f"""#!/bin/bash

#SBATCH -J {job_name}
#SBATCH -o {slurm_dir}/dataset_finalise.%j.out
#SBATCH -e {slurm_dir}/dataset_finalise.%j.err
#SBATCH --nodes=1
#SBATCH --tasks=1
#SBATCH --cpus-per-task=64
#SBATCH --qos=debug
#SBATCH --account=m4718
#SBATCH --constraint=cpu
#SBATCH -t 00:30:00

conda activate anemoi-datasets

# these take 1 sec for 1 yr of data
anemoi-datasets finalise {output_path} > "{log_dir}/finalise.log" 2>&1
anemoi-datasets init-additions {output_path} --delta 6h > "{log_dir}/init_additions.log" 2>&1

# this could be split into parts, but took ~1min on 1 yr of data
anemoi-datasets load-additions {output_path} --delta 6h > "{log_dir}/load_additions.log" 2>&1

# these were again trivial
anemoi-datasets finalise-additions {output_path} > {log_dir}/finalise_additions.log 2>&1
anemoi-datasets cleanup {output_path}
"""
    }

    for filename, content in scripts.items():
        filepath = os.path.join("job-scripts", filename)
        with open(filepath, "w") as file:
            file.write(content)
        print(f"Generated {filepath}")
