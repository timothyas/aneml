import numpy as np
import xarray as xr
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

import cmocean
import xmovie

import cartopy.crs as ccrs

from graphufs.spatialmap import get_extend

_projection = ccrs.Orthographic(
    central_longitude = -120,
    central_latitude = 20,
)

def get_precip_kwargs():
    n = 1
    levels = np.concatenate(
        [
            np.linspace(0, .1, 2*n),
            np.linspace(.1, 1, 5*n),
            np.linspace(1, 10, 5*n),
            np.linspace(10, 50, 3*n),
            #np.linspace(50, 80, 2),
        ],
    )
    norm = BoundaryNorm(levels, len(levels)+1)
    cmap = plt.get_cmap("cmo.rain", len(levels)+1)
    return {"norm": norm, "cmap": cmap, "cbar_kwargs": {"ticks": [0, 1, 10, 50]}}

def nested_scatter(ax, xds, varname, **kwargs):
    n_conus = 38_829
    mappables = []
    for slc, s in zip(
        [slice(None, n_conus), slice(n_conus, None)],
        [8/16, 8],
    ):

        p = ax.scatter(
            xds.longitudes.isel(values=slc),
            xds.latitudes.isel(values=slc),
            c=xds[varname].isel(values=slc),
            s=s,
            transform=ccrs.PlateCarree(),
            **kwargs
        )
        mappables.append(p)

    # Define bounding box corners
    lons = 225, 300
    lats = 21, 53

    kw = {
        "c": "gray",
        "transform": ccrs.PlateCarree(),
        "s": 1,
        "alpha": .3,
    }

    for lon in lons:
        yL = np.arange(*lats, .25)
        xL = np.full_like(yL, lon)
        ax.scatter(xL, yL, **kw)
    for lat in lats:
        xL = np.arange(*lons, .25)
        yL = np.full_like(xL, lat)
        ax.scatter(xL, yL, **kw)
    return mappables

def movie_func(xds, fig, time, *args, **kwargs):

    axs = []
    dalist = []

    truthname = [y for y in list(xds.data_vars) if y in ("ERA5", "Replay")][0]
    vtime = xds["time"].isel(time=time).values
    stime = str(vtime)[:13]

    # Create axes
    ax = fig.add_subplot(1, 2, 1, projection=_projection)

    cbar_kwargs = kwargs.pop("cbar_kwargs", {})

    # Plot Truth
    plotme = xds[truthname].isel(time=time)
    p = plotme.plot(ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False, **kwargs)
    ax.set(title="ERA5")

    axs.append(ax)
    dalist.append(plotme)

    # Plot model
    ax = fig.add_subplot(1, 2, 2, projection=_projection)

    pp = nested_scatter(ax, xds.isel(time=time), "PSL Nested", **kwargs)
    ax.set(title="PSL Nested")

    axs.append(ax)
    dalist.append(plotme)

    # now the colorbar
    [ax.set(xlabel="", ylabel="") for ax in axs]
    [ax.coastlines("50m") for ax in axs]
    extend, kwargs["vmin"], kwargs["vmax"] = get_extend(
        dalist,
        kwargs.get("vmin", None),
        kwargs.get("vmax,", None),
    )
    label = xds.attrs.get("label", "")
    label += f"\n{stime}"
    fig.colorbar(
        p,
        ax=axs,
        orientation="horizontal",
        shrink=.8,
        pad=0.05,
        aspect=35,
        label=label,
        extend=extend,
        **cbar_kwargs,
    )
    fig.set_constrained_layout(True)

    return None, None

def calc_wind_speed(xds):
    if "ugrd10m" in xds:
        ws = np.sqrt(xds["ugrd10m"]**2 + xds["vgrd10m"]**2)
    else:
        ws = np.sqrt(xds["10m_u_component_of_wind"]**2 + xds["10m_v_component_of_wind"]**2)
    ws.attrs["units"] = "m/sec"
    ws.attrs["long_name"] = "10m Wind Speed"
    return ws

def get_truth(name):
    if name.lower() == "era5":
        url = "gs://weatherbench2/datasets/era5/1959-2023_01_10-wb13-6h-1440x721_with_derived_variables.zarr"
        rename = {}
    elif name.lower() == "replay":
        url = "gs://noaa-ufs-gefsv13replay/ufs-hr1/0.25-degree/03h-freq/zarr/fv3.zarr"
        rename = {"pfull": "level", "grid_yt": "lat", "grid_xt": "lon"}

    truth = xr.open_zarr(
        url,
        storage_options={"token": "anon"},
    )
    truth = truth.rename(rename)
    truth.attrs["name"] = name
    return truth


def main(
    read_path,
    store_dir,
    t0="2019-01-01T00",
    tf="2019-06-30T00",
    ifreq=1,
    still_index=None,
):

    psl = xr.open_dataset(read_path)
    psl = psl.sel(time=slice(t0, tf))
    psl = psl.isel(time=slice(None, None, ifreq))
    psl = psl.rename({"longitude": "longitudes", "latitude": "latitudes"})
    psl = psl.set_coords(["longitudes", "latitudes"])

    for tname in ["ERA5"]:

        truth = get_truth(tname)

        # Compute this
        psl["10m_wind_speed"] = calc_wind_speed(psl)
        truth["10m_wind_speed"] = calc_wind_speed(truth)

        # setup for each variable
        plot_options = {
            "2m_temperature": {
                "cmap": "cmo.thermal",
                "vmin": -10,
                "vmax": 30,
            },
            "10m_wind_speed": {
                "cmap": "cmo.tempo_r",
                "vmin": 0,
                "vmax": 25,
            },
            "total_column_water": {
                "cmap": "cmo.rain",
                "vmin": 0,
                "vmax": 60,
            },
            "total_precipitation_6hr": get_precip_kwargs(),
        }

        for varname, options in plot_options.items():

            ds = xr.Dataset({
                "PSL Nested": psl[varname].load(),
            })

            ds[truth.name] = truth[varname].sel(
                time=ds["PSL Nested"].time.values,
            ).load()

            # Convert to degC
            if varname[:3] == "tmp" or "temperature" in varname:
                for key in ds.data_vars:
                    ds[key] -= 273.15
                    ds[key].attrs["units"] = "degC"

            # Convert to mm->m
            if "total_precipitation" in varname:
                for key in ds.data_vars:
                    ds[key] *= 1000
                    ds[key].attrs["units"] = "m"


            label = " ".join([x.capitalize() for x in varname.split("_")])
            ds.attrs["label"] = f"{label} ({ds[truth.name].units})"

            dpi = 300
            pixelwidth = 10*dpi
            pixelheight = 6*dpi
            mov = xmovie.Movie(
                ds,
                movie_func,
                framedim="time",
                input_check=False,
                pixelwidth=pixelwidth,
                pixelheight=pixelheight,
                dpi=dpi,
                **options
            )
            if still_index is not None:
                vtime = ds["time"].isel(time=still_index).values
                stime = str(vtime)[:13]
                fig, ax, pp = mov.render_single_frame(still_index)
                fig.savefig(
                    f"{store_dir}/still.{truth.name.lower()}_vs_psl.{varname}.{t0}.{stime}.jpeg",
                    dpi=dpi,
                    bbox_inches="tight",
                )
    #        mov.save(
    #            f"{store_dir}/{truth.name.lower()}_vs_psl.{varname}.{t0}.{tf}.mp4",
    #            progress=True,
    #            overwrite_existing=True,
    #        )

if __name__ == "__main__":
    inference_dir = "/pscratch/sd/t/timothys/aneml/nested-conus/era5-nest/inference/c080c4bf-7c5a-4f8d-ae86-b070d4e432e1"
    main(
        read_path=f"{inference_dir}/forecast.4320hr.2019-01-01T00.nc",
        store_dir=inference_dir,
        t0="2019-01-01T00",
        tf="2019-06-30T00",
        still_index=1,
    )
