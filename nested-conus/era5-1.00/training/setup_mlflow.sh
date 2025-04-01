#!/bin/bash

# this will setup a filesystem based mlflow server and run it in the background
# it's all a bit dirty though, because this has to be running and it's suggested to do it
# separately from the GPU compute job (???)
# #
# it'll be cleaner with a dedicated server, but this is good enough for debugging I guess

# make sure this is activated
#conda activate anemoi-core

mywork=/pscratch/sd/t/timothys/aneml/nested-conus/era5-1.00
data_dir=$mywork/mlflow-data
artifact_dir=$mywork/mlflow-artifacts

mkdir -p $data_dir
mkdir -p $artifact_dir

nohup mlflow server --backend-store-uri file:$data_dir --default-artifact-root file:$artifact_dir --host 0.0.0.0 --port 5000 > mlflow.log 2>&1 &
