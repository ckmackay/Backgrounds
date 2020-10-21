# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
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
import statistics.mean as mean
import statistics.median as median
import statistics.mode as mode
import statistics.stdev as stdev
import statistics.median_high as median_high

#for datetime
import datetime
import datetime.datetime as dt
import matplotlib.dates as mdates
import matplotlib.dates.date2num as date2num

#for cartopy
import cartopy.crs as ccrs
#from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
# -

df = pd.read_hdf'/o3p/wolp/catalogues/iagos.h5', key='sources'

#df.head(3)

#prints out the sorted list of variables
#sorted(list(df)) 

co_p1_vars = [c for c in df if c.startswith "data_vars_" and "CO_P1" in c] #selects only IAGOS-CORE flights (17247 in total)
co_p1_vars

flights_with_CO_P1 = df.loc[(df[co_p1_vars] > 0).any(axis="columns")]

flights_with_CO_P1
flights_with_CO_P1.shape
print(len(flights_with_CO_P1))

#co_pc2_vars = [c for c in df if c.startswith "data_vars_" and "CO_PC2" in c] #selects only IAGOS-CARIBIC flights (459 in total)
#co_pc2_vars

#flights_with_CO_PC2 = df.loc[(df[co_pc2_vars] > 0).any(axis="columns")]

#flights_with_CO_PC2
#flights_with_CO_PC2.shape
#print(len(flights_with_CO_PC2))

#co_pc1_vars = [c for c in df if c.startswith("data_vars_") and ("CO_PC1") in c] #selects only IAGOS-CARIBIC flights (459 in total)
#co_pc1_vars

#flights_with_CO_PC1 = df.loc[(df[co_pc1_vars] > 0).any(axis="columns")]

#flights_with_CO_PC1
#flights_with_CO_PC1.shape
#print(len(flights_with_CO_PC1))

# +
#flights_with_CO_P1 = flights_with_CO_P1.where(flights_with_CO_P1.data_vars_CO_P1!="nan")
# -

#flights_with_CO_P1.head(3)

# +
#
#       Count flights in each season (DJF, MAM, JJA, SON) 
#       For each area (NA=North America, AT=Atlantic, EU=Europe) 
#       Find median, mean and 3rd quartile vals of CO in upper troposphere (< 300hPa)
#       Find median, mean and 3rd quartile vals of NOx in upper troposphere (< 300hPa)
#       

# Set counters to zero

flights_DJF = 0
flights_DJF_EU = 0
flights_DJF_AT = 0
flights_DJF_NA = 0
flights_MAM = 0
flights_MAM_EU = 0
flights_MAM_AT = 0
flights_MAM_NA = 0
flights_JJA = 0
flights_JJA_EU = 0
flights_JJA_AT = 0
flights_JJA_NA = 0
flights_SON = 0
flights_SON_EU = 0
flights_SON_AT = 0
flights_SON_NA = 0

flight_no=0

# Define geographic zones NA, AT, EU

NA_lat_max=60
NA_lat_min=30
NA_long_max=-60
NA_long_min=-120

AT_lat_max=60
AT_lat_min=0
AT_long_max=-25
AT_long_min=-60

EU_lat_max=70
EU_lat_min=35
EU_long_max=40
EU_long_min=25

# Define lists

CO_DJF_EU=[]
CO_DJF_AT=[]
CO_DJF_NA=[]

CO_MAM_EU=[]
CO_MAM_AT=[]
CO_MAM_NA=[]

CO_JJA_EU=[]
CO_JJA_AT=[]
CO_JJA_NA=[]

CO_SON_EU=[]
CO_SON_AT=[]
CO_SON_NA=[]

nof=100 # limit to nof flights
for i in range(len(flights_with_CO_P1)):
#for i in range(10000,11000):    
#for i in range(nof):
    flights_with_CO_P1.drivers_load_args.iloc[i]
    ds = xr.load_dataset(*json.loads(flights_with_CO_P1.drivers_load_args.iloc[i])["args"])
#    ds=ds.notnull()
    
    
    
    ds['data_vars_cruise'] = xr.where(ds["air_press_AC"]<30000, True, False)
        
    t=ds.UTC_time
    lon=ds.lon
    lat=ds.lat
    
#    for dates from 2015 onwards

    start_datetime=(ds.departure_UTC_time)
    date_time = start_datetime.split("T")
    date = date_time[0]
    time = datetime.datetime.strptime(date, "%Y-%m-%d")
#    print(time.year)
#    print(time.month)
    
    if time.year >= 2015:
#    if time.year == 2015:  
        flight_no=flight_no+1
        print(flight_no)
#        split data into seasons and then into zones
    
        if time.month==12 or time.month==1 or time.month==2:
            flights_DJF +=1
            for j in range(len(ds.lon)):
            # Europe
                if ds.lon[j]<= EU_long_max and ds.lon[j] >= EU_long_min and ds.lat[j]<= EU_lat_max and ds.lat[j] >= EU_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_DJF_EU.append(temp)
                        flights_DJF_EU +=1
                # Atlantic
                if ds.lon[j]<= AT_long_max and ds.lon[j] >= AT_long_min and ds.lat[j]<= AT_lat_max and ds.lat[j] >= AT_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_DJF_AT.append(temp)
                        flights_DJF_AT +=1
                # North America
                if ds.lon[j]<= NA_long_max and ds.lon[j] >= NA_long_min and ds.lat[j]<= NA_lat_max and ds.lat[j] >= NA_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_DJF_NA.append(temp) 
                        flights_DJF_NA +=1
        if time.month==3 or time.month==4 or time.month==5:
            flights_MAM +=1
            for j in range(len(ds.lon)):
            # Europe
                if ds.lon[j]<= EU_long_max and ds.lon[j] >= EU_long_min and ds.lat[j]<= EU_lat_max and ds.lat[j] >= EU_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_MAM_EU.append(temp)
                        flights_MAM_EU +=1
                # Atlantic
                if ds.lon[j]<= AT_long_max and ds.lon[j] >= AT_long_min and ds.lat[j]<= AT_lat_max and ds.lat[j] >= AT_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_MAM_AT.append(temp)
                        flights_MAM_AT +=1
                # North America
                if ds.lon[j]<= NA_long_max and ds.lon[j] >= NA_long_min and ds.lat[j]<= NA_lat_max and ds.lat[j] >= NA_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_MAM_NA.append(temp) 
                        flights_MAM_NA +=1
        if time.month==6 or time.month==7 or time.month==8:
            flights_JJA +=1
            for j in range(len(ds.lon)):
                # Europe
                if ds.lon[j]<= EU_long_max and ds.lon[j] >= EU_long_min and ds.lat[j]<= EU_lat_max and ds.lat[j] >= EU_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_JJA_EU.append(temp)
                        flights_JJA_EU +=1
                # Atlantic
                if ds.lon[j]<= AT_long_max and ds.lon[j] >= AT_long_min and ds.lat[j]<= AT_lat_max and ds.lat[j] >= AT_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_JJA_AT.append(temp)
                        flights_JJA_AT +=1
                # North America
                if ds.lon[j]<= NA_long_max and ds.lon[j] >= NA_long_min and ds.lat[j]<= NA_lat_max and ds.lat[j] >= NA_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_JJA_NA.append(temp)
                        flights_JJA_NA +=1
        if time.month==9 or time.month==10 or time.month==11:
            flights_SON +=1
            for j in range(len(ds.lon)):
                # Europe
                if ds.lon[j]<= EU_long_max and ds.lon[j] >= EU_long_min and ds.lat[j]<= EU_lat_max and ds.lat[j] >= EU_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_SON_EU.append(temp)
                        flights_SON_EU +=1
                # Atlantic
                if ds.lon[j]<= AT_long_max and ds.lon[j] >= AT_long_min and ds.lat[j]<= AT_lat_max and ds.lat[j] >= AT_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_SON_AT.append(temp)
                        flights_SON_AT +=1
                # North America
                if ds.lon[j]<= NA_long_max and ds.lon[j] >= NA_long_min and ds.lat[j]<= NA_lat_max and ds.lat[j] >= NA_lat_min and ds.data_vars_cruise[j]==True:
                    if ds.CO_P1[j] > 0.00:
                        temp=ds.CO_P1[j]
                        CO_SON_NA.append(temp)
                        flights_SON_NA +=1
            
print('Total flights in DJF ',flights_DJF)
print('Total flights in MAM ',flights_MAM)
print('Total flights in JJA ',flights_JJA)
print('Total flights in SON ',flights_SON)

#Results for DJF in Europe
    
CO_DJF_EU_list = [float(n) for n in CO_DJF_EU]
mean_CO_DJF_EU = statistics.mean(CO_DJF_EU_list) 
CO_DJF_EU_list=sorted(CO_DJF_EU_list)
median_CO_DJF_EU = statistics.median(CO_DJF_EU_list)
upper_quartile_CO_DJF_EU = statistics.median_high(CO_DJF_EU_list)
 
print("Mean for DJF_EU is :", mean_CO_DJF_EU) 
print("Median for DJF_EU is :", median_CO_DJF_EU) 
print("Quantiles for DJF_EU is :", upper_quartile_CO_DJF_EU) 
print("Total flights in DJF in EU is :", flights_DJF_EU)

#Results for DJF in Atlantic
    
CO_DJF_AT_list = [float(n) for n in CO_DJF_AT]
mean_CO_DJF_AT = statistics.mean(CO_DJF_AT_list) 
CO_DJF_AT_list=sorted(CO_DJF_AT_list)
median_CO_DJF_AT = statistics.median(CO_DJF_AT_list)
upper_quartile_CO_DJF_AT = statistics.median_high(CO_DJF_AT_list)
 
print("Mean for DJF_AT is :", mean_CO_DJF_AT) 
print("Median for DJF_AT is :", median_CO_DJF_AT) 
print("Quantiles for DJF_AT is :", upper_quartile_CO_DJF_AT) 
print("Total flights in DJF in AT is :", flights_DJF_AT)

#Results for DJF in North America
   
CO_DJF_NA_list = [float(n) for n in CO_DJF_NA]
mean_CO_DJF_NA = statistics.mean(CO_DJF_NA_list) 
CO_DJF_NA_list=sorted(CO_DJF_NA_list)
median_CO_DJF_NA = statistics.median(CO_DJF_NA_list)
upper_quartile_CO_DJF_NA = statistics.median_high(CO_DJF_NA_list)
 
print("Mean for DJF_NA is :", mean_CO_DJF_NA) 
print("Median for DJF_NA is :", median_CO_DJF_NA) 
print("Quantiles for DJF_NA is :", upper_quartile_CO_DJF_NA) 
print("Total flights in DJF in NA is :", flights_DJF_NA)

#Results for MAM in Europe
    
CO_MAM_EU_list = [float(n) for n in CO_MAM_EU]
mean_CO_MAM_EU = statistics.mean(CO_MAM_EU_list) 
CO_MAM_EU_list=sorted(CO_MAM_EU_list)
median_CO_MAM_EU = statistics.median(CO_MAM_EU_list)
upper_quartile_CO_MAM_EU = statistics.median_high(CO_MAM_EU_list)
 
print("Mean for MAM_EU is :", mean_CO_MAM_EU) 
print("Median for MAM_EU is :", median_CO_MAM_EU) 
print("Quantiles for MAM_EU is :", upper_quartile_CO_MAM_EU) 
print("Total flights in MAM in EU is :", flights_MAM_EU)

#Results for MAM in Atlantic
    
CO_MAM_AT_list = [float(n) for n in CO_MAM_AT]
mean_CO_MAM_AT = statistics.mean(CO_MAM_AT_list) 
CO_MAM_AT_list=sorted(CO_MAM_AT_list)
median_CO_MAM_AT = statistics.median(CO_MAM_AT_list)
upper_quartile_CO_MAM_AT = statistics.median_high(CO_MAM_AT_list)
 
print("Mean for MAM_AT is :", mean_CO_MAM_AT) 
print("Median for MAM_AT is :", median_CO_MAM_AT) 
print("Quantiles for MAM_AT is :", upper_quartile_CO_MAM_AT) 
print("Total flights in MAM in AT is :", flights_MAM_AT)

#Results for MAM in North America
    
CO_MAM_NA_list = [float(n) for n in CO_MAM_NA]
mean_CO_MAM_NA = statistics.mean(CO_MAM_NA_list) 
CO_MAM_NA_list=sorted(CO_MAM_NA_list)
median_CO_MAM_NA = statistics.median(CO_MAM_NA_list)
upper_quartile_CO_MAM_NA = statistics.median_high(CO_MAM_NA_list)
 
print("Mean for MAM_NA is :", mean_CO_MAM_NA) 
print("Median for MAM_NA is :", median_CO_MAM_NA) 
print("Quantiles for MAM_NA is :", upper_quartile_CO_MAM_NA) 
print("Total flights in MAM in NA is :", flights_MAM_NA)

#Results for JJA in Europe
    
CO_JJA_EU_list = [float(n) for n in CO_JJA_EU]
mean_CO_JJA_EU = statistics.mean(CO_JJA_EU_list) 
CO_JJA_EU_list=sorted(CO_JJA_EU_list)
median_CO_JJA_EU = statistics.median(CO_JJA_EU_list)
upper_quartile_CO_JJA_EU = statistics.median_high(CO_JJA_EU_list)
 
print("Mean for JJA_EU is :", mean_CO_JJA_EU) 
print("Median for JJA_EU is :", median_CO_JJA_EU) 
print("Quantiles for JJA_EU is :", upper_quartile_CO_JJA_EU) 
print("Total flights in JJA in EU is :", flights_JJA_EU)

#Results for JJA in Atlantic
    
CO_JJA_AT_list = [float(n) for n in CO_JJA_AT]
mean_CO_JJA_AT = statistics.mean(CO_JJA_AT_list) 
CO_JJA_AT_list=sorted(CO_JJA_AT_list)
median_CO_JJA_AT = statistics.median(CO_JJA_AT_list)
upper_quartile_CO_JJA_AT = statistics.median_high(CO_JJA_AT_list)
 
print("Mean for JJA_AT is :", mean_CO_JJA_AT) 
print("Median for JJA_AT is :", median_CO_JJA_AT) 
print("Quantiles for JJA_AT is :", upper_quartile_CO_JJA_AT) 
print("Total flights in JJA in AT is :", flights_JJA_AT)

#Results for JJA in North America
    
CO_JJA_NA_list = [float(n) for n in CO_JJA_NA]
mean_CO_JJA_NA = statistics.mean(CO_JJA_NA_list) 
CO_JJA_NA_list=sorted(CO_JJA_NA_list)
median_CO_JJA_NA = statistics.median(CO_JJA_NA_list)
upper_quartile_CO_JJA_NA = statistics.median_high(CO_JJA_NA_list)
 
print("Mean for JJA_NA is :", mean_CO_JJA_NA) 
print("Median for JJA_NA is :", median_CO_JJA_NA) 
print("Quantiles for JJA_NA is :", upper_quartile_CO_JJA_NA) 
print("Total flights in JJA in NA is :", flights_JJA_NA)

#Results for SON in Europe
    
CO_SON_EU_list = [float(n) for n in CO_SON_EU]
mean_CO_SON_EU = statistics.mean(CO_SON_EU_list) 
CO_SON_EU_list=sorted(CO_SON_EU_list)
median_CO_SON_EU = statistics.median(CO_SON_EU_list)
upper_quartile_CO_SON_EU = statistics.median_high(CO_SON_EU_list)
 
print("Mean for SON_EU is :", mean_CO_SON_EU) 
print("Median for SON_EU is :", median_CO_SON_EU) 
print("Quantiles for SON_EU is :", upper_quartile_CO_SON_EU) 
print("Total flights in SON in EU is :", flights_SON_EU)

#Results for SON in Atlantic
    
CO_SON_AT_list = [float(n) for n in CO_SON_AT]
mean_CO_SON_AT = statistics.mean(CO_SON_AT_list) 
CO_SON_AT_list=sorted(CO_SON_AT_list)
median_CO_SON_AT = statistics.median(CO_SON_AT_list)
upper_quartile_CO_SON_AT = statistics.median_high(CO_SON_AT_list)
 
print("Mean for SON_AT is :", mean_CO_SON_AT) 
print("Median for SON_AT is :", median_CO_SON_AT) 
print("Quantiles for SON_AT is :", upper_quartile_CO_SON_AT) 
print("Total flights in SON in AT is :", flights_SON_AT)

#Results for SON in North America
    
CO_SON_NA_list = [float(n) for n in CO_SON_NA]
mean_CO_SON_NA = statistics.mean(CO_SON_NA_list) 
CO_SON_NA_list=sorted(CO_SON_NA_list)
median_CO_SON_NA = statistics.median(CO_SON_NA_list)
upper_quartile_CO_SON_NA = statistics.median_high(CO_SON_NA_list)
 
print("Mean for SON_NA is :", mean_CO_SON_NA) 
print("Median for SON_NA is :", median_CO_SON_NA) 
print("Quantiles for SON_NA is :", upper_quartile_CO_SON_NA) 
print("Total flights in SON in NA is :", flights_SON_NA)

# -


