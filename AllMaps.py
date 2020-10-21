#!/usr/bin/env python
# coding: utf-8

from netCDF4 import Dataset
from ncdump import ncdump
import numpy as np
import pandas as pd
import xarray as xr
import json

#for plotting
import hvplot.xarray # fancy plotting for xarray
import holoviews as hv
import matplotlib.pyplot as plt

#for stats
import statistics
from statistics import mean, median, mode, stdev, median_high

#for datetime
import datetime
from datetime import datetime as dt
import matplotlib.dates as mdates
from matplotlib.dates import date2num

#for cartopy
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature

#open flexpart output netcdf file
nc_file = '/home/macc/flexpart10.4/flexpart_v10.4_3d7eebf/src/exercises/LNOx_plumes/output/grid_time_20150525201100.nc'
df = Dataset(nc_file, mode='r')

#set up and fill variables
time = df.variables['time'][:]
lons = df.variables['longitude'][:]
lats = df.variables['latitude'][:]
hgt = df.variables['height'][:]
relcom = df.variables['RELCOM'][:]
rellng1 = df.variables['RELLNG1'][:]
rellng2 = df.variables['RELLNG2'][:]
rellat1 = df.variables['RELLAT1'][:]
rellat2 = df.variables['RELLAT2'][:]
relzz1 = df.variables['RELZZ1'][:]
relzz2 = df.variables['RELZZ2'][:]
relkindz = df.variables['RELKINDZ'][:]
relstart = df.variables['RELSTART'][:]
relend = df.variables['RELEND'][:]
relpart = df.variables['RELPART'][:]
relxmass = df.variables['RELXMASS'][:]
lage = df.variables['LAGE'][:]
oro = df.variables['ORO'][:]
spec = df.variables['spec001_mr'][:]

#create dictionaries for each release

for m in range(len(relcom)):
    
    dlons = {}
    dlats = {}
    dspec = {}
    for i in range(len(time)):
        dlons[ "data_lons_" + str( i ) ] = []
        dlats[ "data_lats_" + str( i ) ] = []
        dspec[ "data_spec_" + str( i ) ] = []

    keyslon=dlons.keys()
    keyslat=dlats.keys()
    keyspec=dspec.keys()

    for l in range(len(time)): 
        print(l)
        for k in range(len(hgt)):
            for j in range(len(lats)):
                for i in range(len(lons)): 
                    if spec[:, [0], [l], [k], [j], [i]]>0:
                    
                        list(dlons.values())[l].append(lons[i])
                        list(dlats.values())[l].append(lats[j])
                        list(dspec.values())[l].append(spec[:, [0], [l], [k], [j], [i]])    
    
    
    for l in range(len(time)):
        vallons = list(dlons.values())[l]
        #print(vallons)
        vallats = list(dlats.values())[l]
        #print(vallats)
        valspec = list(dspec.values())[l]
        #print(valspec)
        ccrs.PlateCarree()
        plt.figure()
        fig = plt.figure(figsize=(20,20))
        ax = plt.axes(projection=ccrs.PlateCarree())

        #ax.set_extent([-25, 25, 40, 70])
    
        ax.gridlines(draw_labels=True, color='black', alpha=0.2, linestyle='--')
        ax.stock_img()
        cb = ax.scatter(vallons, vallats, c=valspec, s = 0.5)
        ax.set_aspect('equal', adjustable='box')    
        plt.colorbar(cb, shrink=0.4)
        plt.title("LNOx_plumes time = "+str(l)+", release = "+str(m))
        plt.savefig("plots/LNOx_plumes_EU/rel"+str(m)+"time_"+str(l)+".png")   
        plt.show()
        #plt.title("LNOx_plumes_time = "+str(l))
        

df.close()
