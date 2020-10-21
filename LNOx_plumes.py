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

nc_file = '/home/macc/flexpart10.4/flexpart_v10.4_3d7eebf/src/exercises/LNOx_plumes/output/grid_time_20150525201100.nc'
df = Dataset(nc_file, mode='r')

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

#for a given release, 0,
data_lons=[]
data_lats=[]
data_spec=[]

for l in range(len(time)):
    for k in range(len(hgt)):
        for j in range(len(lats)):
            for i in range(len(lons)): 
            
                if spec[:, 0, [l], [k], [j], [i]]>0:
                    data_lons.append(lons[i])
                    data_lats.append(lats[j])
                    data_spec.append(spec[:, 1, [l], [k], [j], [i]])
                    #print(spec[:, 1, [l], [k], [j], [i]], time[l], hgt[k] ,lons[i], lats[j])


min_spec = min(data_spec)
max_spec = max(data_spec)
print("Min spec value: ", min_spec)
print("Max spec value: ", max_spec)
                    
ccrs.PlateCarree()
plt.figure()
fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection=ccrs.PlateCarree())

#ax.set_extent([-180, -1, 30, 90])
ax.gridlines(draw_labels=True,
             color='black', alpha=0.2, linestyle='--')
ax.stock_img()
cb = ax.scatter(data_lons, data_lats, c=data_spec, vmin=min_spec, vmax=max_spec)
#cb = ax.scatter(lons[0:100], lats[0:100], spec[0:100], s = 0.5, vmin=5, vmax=25)
ax.set_aspect('equal', adjustable='box')    
plt.colorbar(cb) 
plt.savefig("plots/LNOx_plumes/plumes.png")

df.close()

