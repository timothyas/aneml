from plot_movie import main

if __name__ == "__main__":
    inference_dir = "/pscratch/sd/t/timothys/aneml/nested-conus/era5-nest/inference/c080c4bf-7c5a-4f8d-ae86-b070d4e432e1"
    main(
        read_path=f"{inference_dir}/forecast.240hr.2018-04-05T12.nc",
        store_dir=inference_dir,
        t0="2018-04-05T12",
        tf="2018-04-15T12",
        still_index=2,
    )
