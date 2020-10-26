#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import xarray as xr
import json

#for plotting
import hvplot.xarray # fancy plotting for xarray
import holoviews as hv
import matplotlib.pyplot as plt

#for stats
import math
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

df = pd.read_hdf('/o3p/wolp/catalogues/iagos.h5', key='sources')

nox_vars = [c for c in df if c.startswith("data_vars_") and ("NOx") in c and not "_err" in c and not "_stat" in c and not "CO2" in c] #selects only IAGOS-CORE flights (17247 in total)

flights_with_NOx = df.loc[(df[nox_vars] > 0).any(axis="columns")]

# Define geographic zones NA, AT, EU (for now)

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
EU_long_min=-25

#create counters for number of entries in each month
months=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

for i in range(len(months)):
    locals()['flights_{}'.format(months[i])] = 0

#create counters for number of entries in each month in each zone

zones=['EU', 'AT', 'NA']
for i in range(len(months)):
    for j in range(len(zones)):
        locals()['flights_{}_{}'.format(months[i],zones[j])] = 0

#create lists for each month in each zone for NOx values

for i in range(len(months)):
    for j in range(len(zones)):
        locals()['NOx_{}_{}'.format(months[i],zones[j])] = []

        #create corresponding lists for each month in each zone for counts of NOx values for plotting

for i in range(len(months)):
    for j in range(len(zones)):
        locals()['counts_{}_{}'.format(months[i],zones[j])] = []

flight_no=0

nof=100 # limit to nof flights
for i in range(len(flights_with_NOx)):
  
    flights_with_NOx.drivers_load_args.iloc[i]
    ds = xr.load_dataset(*json.loads(flights_with_NOx.drivers_load_args.iloc[i])["args"])
  
    start_datetime=(ds.departure_UTC_time)
    date_time = start_datetime.split("T")
    date = date_time[0]
    time = datetime.datetime.strptime(date, "%Y-%m-%d")
            
    ds['data_vars_cruise'] = xr.where(ds["air_press_AC"]<30000, True, False)
    
    if ds.source=='IAGOS-MOZAIC':
        #print('Selected MOZAIC')
        data_NOx = ds.NOx_PM.where(ds.data_vars_cruise==True)
    elif ds.source=='IAGOS-CORE':
        #print("Selected CORE")
        
        data_NOx = ds.NOx_P2b.where(ds.data_vars_cruise==True)
        
        ################################select NO and NO2 for CARIBIC and add together
        
    elif ds.source=="IAGOS-CARIBIC":
        #print("Selected CARIBIC")
        if date < '2005-05-19':
            #print('Using NO_PC1')
            data_NO = ds.NO_PC1.where(ds.data_vars_cruise==True)
            data_NO2 = ds.NO2_PC1.where(ds.data_vars_cruise==True)
            data_NOx = data_NO+data_NO2
        elif date >= '2005-05-19':
            #print('Using NO_PC2')
            data_NO = ds.NO_PC2.where(ds.data_vars_cruise==True)
            data_NO2 = ds.NO2_PC2.where(ds.data_vars_cruise==True)
            data_NOx = data_NO+data_NO2
        else:
            print('Did not find CARIBIC data:', ds.source)
    else: 
        print('Did not find source:', ds.source)    
        
    t=ds.UTC_time.where(ds.data_vars_cruise==True)
    lon=ds.lon.where(ds.data_vars_cruise==True)
    lat=ds.lat.where(ds.data_vars_cruise==True)
        
    flight_no+=1
    
    #        split data into months and zones
    k = 0
    for k in range(len(months)):
        if time.month==k+1:
            locals()['flights_{}'.format(months[k])] += 1
            for j in range(len(lon)):
                for l in range(len(zones)):
                    if lon[j]<= locals()['{}_long_max'.format(zones[l])] and lon[j] >= globals()['{}_long_min'.format(zones[l])] and lat[j]<= globals()['{}_lat_max'.format(zones[l])] and lat[j] >= globals()['{}_lat_min'.format(zones[l])]:
                        if data_NOx[j] > 0.00:
                            if ds.NOx_P2b_val[j]==0:
                                temp=data_NOx[j]
                                locals()['NOx_{}_{}'.format(months[k],zones[l])].append(temp)
                                locals()['flights_{}_{}'.format(months[k],zones[l])] += 1
                                locals()['counts_{}_{}'.format(months[k],zones[l])].append(locals()['flights_{}_{}'.format(months[k],zones[l])])

print("Total number of flights analysed: ", flight_no)                        
print("flights_JAN", flights_JAN)
print("flights_FEB",flights_FEB)
print("flights_MAR",flights_MAR)
print("flights_APR",flights_APR)
print("flights_MAY",flights_MAY)
print("flights_JUN",flights_JUN)
print("flights_JUL",flights_JUL)
print("flights_AUG",flights_AUG)
print("flights_SEP",flights_SEP)
print("flights_OCT",flights_OCT)
print("flights_NOV",flights_NOV)
print("flights_DEC",flights_DEC)

print("Entries for MAY_EU", flights_MAY_EU)
if len(NOx_MAY_EU) > 1:
    NOx_MAY_EU_list = [float(n) for n in NOx_MAY_EU]
    mean_NOx_MAY_EU = statistics.mean(NOx_MAY_EU_list) 
    std_NOx_MAY_EU = statistics.stdev(NOx_MAY_EU_list) 
    NOx_MAY_EU_list=sorted(NOx_MAY_EU_list)
    median_NOx_MAY_EU = statistics.median(NOx_MAY_EU_list)
    upper_NOx_MAY_EU_list = []
    lower_NOx_MAY_EU_list = []

    for i in range(len(NOx_MAY_EU_list)):
        if NOx_MAY_EU_list[i]>median_NOx_MAY_EU:
            upper_NOx_MAY_EU_list.append(NOx_MAY_EU_list[i])
        if NOx_MAY_EU_list[i]<median_NOx_MAY_EU:
            lower_NOx_MAY_EU_list.append(NOx_MAY_EU_list[i])
        
    upper_quartile_NOx_MAY_EU = statistics.median(upper_NOx_MAY_EU_list)
    lower_quartile_NOx_MAY_EU = statistics.median(lower_NOx_MAY_EU_list)
if flights_MAY_EU > 0:
    print("Number of entries MAY_EU :",len(NOx_MAY_EU))
    print("             Mean MAY_EU :",mean_NOx_MAY_EU)
    print("            Stdev MAY_EU :",std_NOx_MAY_EU)
    print("           Median MAY_EU :",median_NOx_MAY_EU)
    print("               Q3 MAY_EU :",upper_quartile_NOx_MAY_EU)
    print("               Q1 MAY_EU :",lower_quartile_NOx_MAY_EU)
#MAY_AT
print("Entries for MAY_AT", flights_MAY_AT)
if len(NOx_MAY_AT) > 1:
    NOx_MAY_AT_list = [float(n) for n in NOx_MAY_AT]
    mean_NOx_MAY_AT = statistics.mean(NOx_MAY_AT_list)
    std_NOx_MAY_AT = statistics.stdev(NOx_MAY_AT_list)
    NOx_MAY_AT_list=sorted(NOx_MAY_AT_list)
    median_NOx_MAY_AT = statistics.median(NOx_MAY_AT_list)
    upper_NOx_MAY_AT_list = []
    lower_NOx_MAY_AT_list = []
    
    for i in range(len(NOx_MAY_AT_list)):
        if NOx_MAY_AT_list[i]>median_NOx_MAY_AT:
            upper_NOx_MAY_AT_list.append(NOx_MAY_AT_list[i])
        if NOx_MAY_AT_list[i]<median_NOx_MAY_AT:
            lower_NOx_MAY_AT_list.append(NOx_MAY_AT_list[i])
                
    upper_quartile_NOx_MAY_AT = statistics.median(upper_NOx_MAY_AT_list)
    lower_quartile_NOx_MAY_AT = statistics.median(lower_NOx_MAY_AT_list)
if flights_MAY_AT > 0:
    print("Number of entries MAY_AT :",len(NOx_MAY_AT))
    print("             Mean MAY_AT :",mean_NOx_MAY_AT)
    print("            Stdev MAY_AT :",std_NOx_MAY_AT)
    print("           Median MAY_AT :",median_NOx_MAY_AT)
    print("               Q3 MAY_AT :",upper_quartile_NOx_MAY_AT)
    print("               Q1 MAY_AT :",lower_quartile_NOx_MAY_AT)
#MAY_NA
print("Entries for MAY_NA", flights_MAY_NA)
if len(NOx_MAY_NA) > 1:
    NOx_MAY_NA_list = [float(n) for n in NOx_MAY_NA]
    #print(NOx_JUN_NA_list)
    mean_NOx_MAY_NA = statistics.mean(NOx_MAY_NA_list) 
    std_NOx_MAY_NA = statistics.stdev(NOx_MAY_NA_list) 
    NOx_MAY_NA_list=sorted(NOx_MAY_NA_list)
    median_NOx_MAY_NA = statistics.median(NOx_MAY_NA_list)
    upper_NOx_MAY_NA_list = []
    lower_NOx_MAY_NA_list = []
    
    for i in range(len(NOx_MAY_NA_list)):
        if NOx_MAY_NA_list[i]>median_NOx_MAY_NA:
            upper_NOx_MAY_NA_list.append(NOx_MAY_NA_list[i])
        if NOx_MAY_NA_list[i]<median_NOx_MAY_NA:
            lower_NOx_MAY_NA_list.append(NOx_MAY_NA_list[i])
                
    upper_quartile_NOx_MAY_NA = statistics.median(upper_NOx_MAY_NA_list)
    lower_quartile_NOx_MAY_NA = statistics.median(lower_NOx_MAY_NA_list)
if flights_MAY_NA > 0:                
    print("Number of entries MAY_NA :", len(NOx_MAY_NA))
    print("             Mean MAY_NA :",mean_NOx_MAY_NA)
    print("            Stdev MAY_NA :",std_NOx_MAY_NA)
    print("           Median MAY_NA :",median_NOx_MAY_NA)
    print("               Q3 MAY_NA :",upper_quartile_NOx_MAY_NA)
    print("               Q1 MAY_NA :",lower_quartile_NOx_MAY_NA)
###########################################################################
############################################################################print("Entries for JUN_EU", flights_JUN_EU)
if len(NOx_JUN_EU) > 1:
    NOx_JUN_EU_list = [float(n) for n in NOx_JUN_EU]
    mean_NOx_JUN_EU = statistics.mean(NOx_JUN_EU_list) 
    std_NOx_JUN_EU = statistics.stdev(NOx_JUN_EU_list) 
    NOx_JUN_EU_list=sorted(NOx_JUN_EU_list)
    median_NOx_JUN_EU = statistics.median(NOx_JUN_EU_list)
    upper_NOx_JUN_EU_list = []
    lower_NOx_JUN_EU_list = []

    for i in range(len(NOx_JUN_EU_list)):
        if NOx_JUN_EU_list[i]>median_NOx_JUN_EU:
            upper_NOx_JUN_EU_list.append(NOx_JUN_EU_list[i])
        if NOx_JUN_EU_list[i]<median_NOx_JUN_EU:
            lower_NOx_JUN_EU_list.append(NOx_JUN_EU_list[i])
        
    upper_quartile_NOx_JUN_EU = statistics.median(upper_NOx_JUN_EU_list)
    lower_quartile_NOx_JUN_EU = statistics.median(lower_NOx_JUN_EU_list)
if flights_JUN_EU > 0:
    print("Number of entries JUN_EU :",len(NOx_JUN_EU))
    print("             Mean JUN_EU :",mean_NOx_JUN_EU)
    print("            Stdev JUN_EU :",std_NOx_JUN_EU)
    print("           Median JUN_EU :",median_NOx_JUN_EU)
    print("               Q3 JUN_EU :",upper_quartile_NOx_JUN_EU)
    print("               Q1 JUN_EU :",lower_quartile_NOx_JUN_EU)
#JUN_AT
print("Entries for JUN_AT", flights_JUN_AT)
if len(NOx_JUN_AT) > 1:
    NOx_JUN_AT_list = [float(n) for n in NOx_JUN_AT]
    mean_NOx_JUN_AT = statistics.mean(NOx_JUN_AT_list)
    std_NOx_JUN_AT = statistics.stdev(NOx_JUN_AT_list)
    NOx_JUN_AT_list=sorted(NOx_JUN_AT_list)
    median_NOx_JUN_AT = statistics.median(NOx_JUN_AT_list)
    upper_NOx_JUN_AT_list = []
    lower_NOx_JUN_AT_list = []
    
    for i in range(len(NOx_JUN_AT_list)):
        if NOx_JUN_AT_list[i]>median_NOx_JUN_AT:
            upper_NOx_JUN_AT_list.append(NOx_JUN_AT_list[i])
        if NOx_JUN_AT_list[i]<median_NOx_JUN_AT:
            lower_NOx_JUN_AT_list.append(NOx_JUN_AT_list[i])
                
    upper_quartile_NOx_JUN_AT = statistics.median(upper_NOx_JUN_AT_list)
    lower_quartile_NOx_JUN_AT = statistics.median(lower_NOx_JUN_AT_list)
if flights_JUN_AT > 0:
    print("Number of entries JUN_AT :",len(NOx_JUN_AT))
    print("             Mean JUN_AT :",mean_NOx_JUN_AT)
    print("            Stdev JUN_AT :",std_NOx_JUN_AT)
    print("           Median JUN_AT :",median_NOx_JUN_AT)
    print("               Q3 JUN_AT :",upper_quartile_NOx_JUN_AT)
    print("               Q1 JUN_AT :",lower_quartile_NOx_JUN_AT)
#JUN_NA
print("Entries for JUN_NA", flights_JUN_NA)
if len(NOx_JUN_NA) > 1:
    NOx_JUN_NA_list = [float(n) for n in NOx_JUN_NA]
    #print(NOx_JUN_NA_list)
    mean_NOx_JUN_NA = statistics.mean(NOx_JUN_NA_list) 
    std_NOx_JUN_NA = statistics.stdev(NOx_JUN_NA_list) 
    NOx_JUN_NA_list=sorted(NOx_JUN_NA_list)
    median_NOx_JUN_NA = statistics.median(NOx_JUN_NA_list)
    upper_NOx_JUN_NA_list = []
    lower_NOx_JUN_NA_list = []
    
    for i in range(len(NOx_JUN_NA_list)):
        if NOx_JUN_NA_list[i]>median_NOx_JUN_NA:
            upper_NOx_JUN_NA_list.append(NOx_JUN_NA_list[i])
        if NOx_JUN_NA_list[i]<median_NOx_JUN_NA:
            lower_NOx_JUN_NA_list.append(NOx_JUN_NA_list[i])
                
    upper_quartile_NOx_JUN_NA = statistics.median(upper_NOx_JUN_NA_list)
    lower_quartile_NOx_JUN_NA = statistics.median(lower_NOx_JUN_NA_list)
if flights_JUN_NA > 0:                
    print("Number of entries JUN_NA :", len(NOx_JUN_NA))
    print("             Mean JUN_NA :",mean_NOx_JUN_NA)
    print("            Stdev JUN_NA :",std_NOx_JUN_NA)
    print("           Median JUN_NA :",median_NOx_JUN_NA)
    print("               Q3 JUN_NA :",upper_quartile_NOx_JUN_NA)
    print("               Q1 JUN_NA :",lower_quartile_NOx_JUN_NA)
###########################################################################
############################################################################
#JUL_EU
print("Entries for JUL_EU", flights_JUL_EU)
if len(NOx_JUL_EU) > 1:
    NOx_JUL_EU_list = [float(n) for n in NOx_JUL_EU]
    mean_NOx_JUL_EU = statistics.mean(NOx_JUL_EU_list) 
    std_NOx_JUL_EU = statistics.stdev(NOx_JUL_EU_list) 
    NOx_JUL_EU_list=sorted(NOx_JUL_EU_list)
    median_NOx_JUL_EU = statistics.median(NOx_JUL_EU_list)
    upper_NOx_JUL_EU_list = []
    lower_NOx_JUL_EU_list = []
    
    for i in range(len(NOx_JUL_EU_list)):
        if NOx_JUL_EU_list[i]>median_NOx_JUL_EU:
            upper_NOx_JUL_EU_list.append(NOx_JUL_EU_list[i])
        if NOx_JUL_EU_list[i]<median_NOx_JUL_EU:
            lower_NOx_JUL_EU_list.append(NOx_JUL_EU_list[i])
                
    upper_quartile_NOx_JUL_EU = statistics.median(upper_NOx_JUL_EU_list)
    lower_quartile_NOx_JUL_EU = statistics.median(lower_NOx_JUL_EU_list)
if flights_JUL_EU > 0:                
    print("Number of entries JUL_EU :",len(NOx_JUL_EU))
    print("             Mean JUL_EU :",mean_NOx_JUL_EU)
    print("            Stdev JUL_EU :",std_NOx_JUL_EU)
    print("           Median JUL_EU :",median_NOx_JUL_EU)
    print("               Q3 JUL_EU :",upper_quartile_NOx_JUL_EU)
    print("               Q1 JUL_EU :",lower_quartile_NOx_JUL_EU)
#JUL_AT
print("Entries for JUL_AT", flights_JUL_AT)
if len(NOx_JUL_AT) > 1:
    NOx_JUL_AT_list = [float(n) for n in NOx_JUL_AT]
    mean_NOx_JUL_AT = statistics.mean(NOx_JUL_AT_list) 
    std_NOx_JUL_AT = statistics.stdev(NOx_JUL_AT_list) 
    NOx_JUL_AT_list=sorted(NOx_JUL_AT_list)
    median_NOx_JUL_AT = statistics.median(NOx_JUL_AT_list)
    upper_NOx_JUL_AT_list = []
    lower_NOx_JUL_AT_list = []
    
    for i in range(len(NOx_JUL_AT_list)):
        if NOx_JUL_AT_list[i]>median_NOx_JUL_AT:
            upper_NOx_JUL_AT_list.append(NOx_JUL_AT_list[i])
        if NOx_JUL_AT_list[i]<median_NOx_JUL_AT:
            lower_NOx_JUL_AT_list.append(NOx_JUL_AT_list[i])
                
    upper_quartile_NOx_JUL_AT = statistics.median(upper_NOx_JUL_AT_list)
    lower_quartile_NOx_JUL_AT = statistics.median(lower_NOx_JUL_AT_list)
if flights_JUL_AT > 0:                            
    print("Number of entries JUL_AT :",len(NOx_JUL_AT))
    print("             Mean JUL_AT :",mean_NOx_JUL_AT)
    print("            Stdev JUL_AT :",std_NOx_JUL_AT)
    print("           Median JUL_AT :",median_NOx_JUL_AT)
    print("               Q3 JUL_AT :",upper_quartile_NOx_JUL_AT)
    print("               Q1 JUL_AT :",lower_quartile_NOx_JUL_AT)
#JUL_NA
print("Entries for JUL_NA", flights_JUL_NA)
if len(NOx_JUL_NA) > 1:
    NOx_JUL_NA_list = [float(n) for n in NOx_JUL_NA]
    mean_NOx_JUL_NA = statistics.mean(NOx_JUL_NA_list) 
    std_NOx_JUL_NA = statistics.stdev(NOx_JUL_NA_list) 
    NOx_JUL_NA_list=sorted(NOx_JUL_NA_list)
    median_NOx_JUL_NA = statistics.median(NOx_JUL_NA_list)
    upper_NOx_JUL_NA_list = []
    lower_NOx_JUL_NA_list = []
    
    for i in range(len(NOx_JUL_NA_list)):
        if NOx_JUL_NA_list[i]>median_NOx_JUL_NA:
            upper_NOx_JUL_NA_list.append(NOx_JUL_NA_list[i])
        if NOx_JUL_NA_list[i]<median_NOx_JUL_NA:
            lower_NOx_JUL_NA_list.append(NOx_JUL_NA_list[i])
                
    upper_quartile_NOx_JUL_NA = statistics.median(upper_NOx_JUL_NA_list)
    lower_quartile_NOx_JUL_NA = statistics.median(lower_NOx_JUL_NA_list)
if flights_JUL_NA > 0:
    print("Number of entries JUL_NA :", len(NOx_JUL_NA))
    print("             Mean JUL_NA :",mean_NOx_JUL_NA)
    print("            Stdev JUL_NA :",std_NOx_JUL_NA)
    print("           Median JUL_NA :",median_NOx_JUL_NA)
    print("               Q3 JUL_NA :",upper_quartile_NOx_JUL_NA)
    print("               Q1 JUL_NA :",lower_quartile_NOx_JUL_NA)
###########################################################################
############################################################################
#AUG_EU
print("Entries for AUG_EU", flights_AUG_EU)
if len(NOx_AUG_EU) > 1:
    NOx_AUG_EU_list = [float(n) for n in NOx_AUG_EU]
    mean_NOx_AUG_EU = statistics.mean(NOx_AUG_EU_list) 
    std_NOx_AUG_EU = statistics.stdev(NOx_AUG_EU_list) 
    NOx_AUG_EU_list=sorted(NOx_AUG_EU_list)
    median_NOx_AUG_EU = statistics.median(NOx_AUG_EU_list)
    upper_NOx_AUG_EU_list = []
    lower_NOx_AUG_EU_list = []
    
    for i in range(len(NOx_AUG_EU_list)):
        if NOx_AUG_EU_list[i]>median_NOx_AUG_EU:
            upper_NOx_AUG_EU_list.append(NOx_AUG_EU_list[i])
        if NOx_AUG_EU_list[i]<median_NOx_AUG_EU:
            lower_NOx_AUG_EU_list.append(NOx_AUG_EU_list[i])
                
    upper_quartile_NOx_AUG_EU = statistics.median(upper_NOx_AUG_EU_list)
    lower_quartile_NOx_AUG_EU = statistics.median(lower_NOx_AUG_EU_list)
if flights_AUG_EU > 0:                
    print("Number of entries AUG_EU :",len(NOx_AUG_EU))
    print("             Mean AUG_EU :",mean_NOx_AUG_EU)
    print("            Stdev AUG_EU :",std_NOx_AUG_EU)
    print("           Median AUG_EU :",median_NOx_AUG_EU)
    print("               Q3 AUG_EU :",upper_quartile_NOx_AUG_EU)
    print("               Q1 AUG_EU :",lower_quartile_NOx_AUG_EU)
#AUG_AT
print("Entries for AUG_AT", flights_AUG_AT)
if len(NOx_AUG_AT) > 1:
    NOx_AUG_AT_list = [float(n) for n in NOx_AUG_AT]
    mean_NOx_AUG_AT = statistics.mean(NOx_AUG_AT_list) 
    std_NOx_AUG_AT = statistics.stdev(NOx_AUG_AT_list) 
    NOx_AUG_AT_list=sorted(NOx_AUG_AT_list)
    median_NOx_AUG_AT = statistics.median(NOx_AUG_AT_list)
    upper_NOx_AUG_AT_list = []
    lower_NOx_AUG_AT_list = []
    
    for i in range(len(NOx_AUG_AT_list)):
        if NOx_AUG_AT_list[i]>median_NOx_AUG_AT:
            upper_NOx_AUG_AT_list.append(NOx_AUG_AT_list[i])
        if NOx_AUG_AT_list[i]<median_NOx_AUG_AT:
            lower_NOx_AUG_AT_list.append(NOx_AUG_AT_list[i])
                
    upper_quartile_NOx_AUG_AT = statistics.median(upper_NOx_AUG_AT_list)
    lower_quartile_NOx_AUG_AT = statistics.median(lower_NOx_AUG_AT_list)
if flights_AUG_AT > 0:                
    print("Number of entries AUG_AT :",len(NOx_AUG_AT))
    print("             Mean AUG_AT :",mean_NOx_AUG_AT)
    print("            Stdev AUG_AT :",std_NOx_AUG_AT)
    print("           Median AUG_AT :",median_NOx_AUG_AT)
    print("               Q3 AUG_AT :",upper_quartile_NOx_AUG_AT)
    print("               Q1 AUG_AT :",lower_quartile_NOx_AUG_AT)
#AUG_NA
print("Entries for AUG_NA", flights_AUG_NA)
if len(NOx_AUG_NA) > 1:
    NOx_AUG_NA_list = [float(n) for n in NOx_AUG_NA]
    mean_NOx_AUG_NA = statistics.mean(NOx_AUG_NA_list) 
    std_NOx_AUG_NA = statistics.stdev(NOx_AUG_NA_list) 
    NOx_AUG_NA_list=sorted(NOx_AUG_NA_list)
    median_NOx_AUG_NA = statistics.median(NOx_AUG_NA_list)
    upper_NOx_AUG_NA_list = []
    lower_NOx_AUG_NA_list = []
    
    for i in range(len(NOx_AUG_NA_list)):
        if NOx_AUG_NA_list[i]>median_NOx_AUG_NA:
            upper_NOx_AUG_NA_list.append(NOx_AUG_NA_list[i])
        if NOx_AUG_NA_list[i]<median_NOx_AUG_NA:
            lower_NOx_AUG_NA_list.append(NOx_AUG_NA_list[i])
                
    upper_quartile_NOx_AUG_NA = statistics.median(upper_NOx_AUG_NA_list)
    lower_quartile_NOx_AUG_NA = statistics.median(lower_NOx_AUG_NA_list)
if flights_AUG_NA > 0:                
    print("Number of entries AUG_NA :", len(NOx_AUG_NA))
    print("             Mean AUG_NA :",mean_NOx_AUG_NA)
    print("            Stdev AUG_NA :",std_NOx_AUG_NA)
    print("           Median AUG_NA :",median_NOx_AUG_NA)
    print("               Q3 AUG_NA :",upper_quartile_NOx_AUG_NA)
    print("               Q1 AUG_NA :",lower_quartile_NOx_AUG_NA)
###########################################################################
############################################################################
#SEP_EU
print("Entries for SEP_EU", flights_SEP_EU)
print("len of sep EU", len(NOx_SEP_EU))
if len(NOx_SEP_EU) > 1:
    NOx_SEP_EU_list = [float(n) for n in NOx_SEP_EU]
    mean_NOx_SEP_EU = statistics.mean(NOx_SEP_EU_list) 
    std_NOx_SEP_EU = statistics.stdev(NOx_SEP_EU_list) 
    NOx_SEP_EU_list=sorted(NOx_SEP_EU_list)
    median_NOx_SEP_EU = statistics.median(NOx_SEP_EU_list)
    upper_NOx_SEP_EU_list = []
    lower_NOx_SEP_EU_list = []
    
    for i in range(len(NOx_SEP_EU_list)):
        if NOx_SEP_EU_list[i]>median_NOx_SEP_EU:
            upper_NOx_SEP_EU_list.append(NOx_SEP_EU_list[i])
        if NOx_SEP_EU_list[i]<median_NOx_SEP_EU:
            lower_NOx_SEP_EU_list.append(NOx_SEP_EU_list[i])
                
    upper_quartile_NOx_SEP_EU = statistics.median(upper_NOx_SEP_EU_list)
    lower_quartile_NOx_SEP_EU = statistics.median(lower_NOx_SEP_EU_list)
if flights_SEP_EU > 0:                
    print("Number of entries SEP_EU :",len(NOx_SEP_EU))
    print("             Mean SEP_EU :",mean_NOx_SEP_EU)
    print("            Stdev SEP_EU :",std_NOx_SEP_EU)
    print("           Median SEP_EU :",median_NOx_SEP_EU)
    print("               Q3 SEP_EU :",upper_quartile_NOx_SEP_EU)
    print("               Q1 SEP_EU :",lower_quartile_NOx_SEP_EU)
#SEP_AT
print("Entries for SEP_AT", flights_SEP_AT)
if len(NOx_SEP_AT) > 1:
    NOx_SEP_AT_list = [float(n) for n in NOx_SEP_AT]
    mean_NOx_SEP_AT = statistics.mean(NOx_SEP_AT_list) 
    std_NOx_SEP_AT = statistics.stdev(NOx_SEP_AT_list) 
    NOx_SEP_AT_list=sorted(NOx_SEP_AT_list)
    median_NOx_SEP_AT = statistics.median(NOx_SEP_AT_list)
    upper_NOx_SEP_AT_list = []
    lower_NOx_SEP_AT_list = []
    
    for i in range(len(NOx_SEP_AT_list)):
        if NOx_SEP_AT_list[i]>median_NOx_SEP_AT:
            upper_NOx_SEP_AT_list.append(NOx_SEP_AT_list[i])
        if NOx_SEP_AT_list[i]<median_NOx_SEP_AT:
            lower_NOx_SEP_AT_list.append(NOx_SEP_AT_list[i])
                
    upper_quartile_NOx_SEP_AT = statistics.median(upper_NOx_SEP_AT_list)
    lower_quartile_NOx_SEP_AT = statistics.median(lower_NOx_SEP_AT_list)
if flights_SEP_AT > 0:
    print("Number of entries SEP_AT :",len(NOx_SEP_AT))
    print("             Mean SEP_AT :",mean_NOx_SEP_AT)
    print("            Stdev SEP_AT :",std_NOx_SEP_AT)
    print("           Median SEP_AT :",median_NOx_SEP_AT)
    print("               Q3 SEP_AT :",upper_quartile_NOx_SEP_AT)
    print("               Q1 SEP_AT :",lower_quartile_NOx_SEP_AT)
#SEP_NA
print("Entries for SEP_NA", flights_SEP_NA)
if len(NOx_SEP_NA) > 1:
    NOx_SEP_NA_list = [float(n) for n in NOx_SEP_NA]
    mean_NOx_SEP_NA = statistics.mean(NOx_SEP_NA_list) 
    std_NOx_SEP_NA = statistics.stdev(NOx_SEP_NA_list) 
    NOx_SEP_NA_list=sorted(NOx_SEP_NA_list)
    median_NOx_SEP_NA = statistics.median(NOx_SEP_NA_list)
    upper_NOx_SEP_NA_list = []
    lower_NOx_SEP_NA_list = []
    
    for i in range(len(NOx_SEP_NA_list)):
        if NOx_SEP_NA_list[i]>median_NOx_SEP_NA:
            upper_NOx_SEP_NA_list.append(NOx_SEP_NA_list[i])
        if NOx_SEP_NA_list[i]<median_NOx_SEP_NA:
            lower_NOx_SEP_NA_list.append(NOx_SEP_NA_list[i])
                
    upper_quartile_NOx_SEP_NA = statistics.median(upper_NOx_SEP_NA_list)
    lower_quartile_NOx_SEP_NA = statistics.median(lower_NOx_SEP_NA_list)
if flights_SEP_NA > 0:            
    print("Number of entries SEP_NA :", len(NOx_SEP_NA))
    print("             Mean SEP_NA :",mean_NOx_SEP_NA)
    print("            Stdev SEP_NA :",std_NOx_SEP_NA)
    print("           Median SEP_NA :",median_NOx_SEP_NA)
    print("               Q3 SEP_NA :",upper_quartile_NOx_SEP_NA)
    print("               Q1 SEP_NA :",lower_quartile_NOx_SEP_NA)
###########################################################################
############################################################################
#OCT_EU
print("Entries for OCT_EU", flights_OCT_EU)
if len(NOx_OCT_EU) > 1:
    NOx_OCT_EU_list = [float(n) for n in NOx_OCT_EU]
    mean_NOx_OCT_EU = statistics.mean(NOx_OCT_EU_list) 
    std_NOx_OCT_EU = statistics.stdev(NOx_OCT_EU_list) 
    NOx_OCT_EU_list=sorted(NOx_OCT_EU_list)
    median_NOx_OCT_EU = statistics.median(NOx_OCT_EU_list)
    upper_NOx_OCT_EU_list = []
    lower_NOx_OCT_EU_list = []
    
    for i in range(len(NOx_OCT_EU_list)):
        if NOx_OCT_EU_list[i]>median_NOx_OCT_EU:
            upper_NOx_OCT_EU_list.append(NOx_OCT_EU_list[i])
        if NOx_OCT_EU_list[i]<median_NOx_OCT_EU:
            lower_NOx_OCT_EU_list.append(NOx_OCT_EU_list[i])
                
    upper_quartile_NOx_OCT_EU = statistics.median(upper_NOx_OCT_EU_list)
    lower_quartile_NOx_OCT_EU = statistics.median(lower_NOx_OCT_EU_list)
if flights_OCT_EU > 0:                
    print("Number of entries OCT_EU :",len(NOx_OCT_EU))
    print("             Mean OCT_EU :",mean_NOx_OCT_EU)
    print("            Stdev OCT_EU :",std_NOx_OCT_EU)
    print("           Median OCT_EU :",median_NOx_OCT_EU)
    print("               Q3 OCT_EU :",upper_quartile_NOx_OCT_EU)
    print("               Q1 OCT_EU :",lower_quartile_NOx_OCT_EU)
#OCT_AT
print("Entries for OCT_AT", flights_OCT_AT)
if len(NOx_OCT_AT) > 1:
    NOx_OCT_AT_list = [float(n) for n in NOx_OCT_AT]
    mean_NOx_OCT_AT = statistics.mean(NOx_OCT_AT_list) 
    std_NOx_OCT_AT = statistics.stdev(NOx_OCT_AT_list) 
    NOx_OCT_AT_list=sorted(NOx_OCT_AT_list)
    median_NOx_OCT_AT = statistics.median(NOx_OCT_AT_list)
    upper_NOx_OCT_AT_list = []
    lower_NOx_OCT_AT_list = []
    
    for i in range(len(NOx_OCT_AT_list)):
        if NOx_OCT_AT_list[i]>median_NOx_OCT_AT:
            upper_NOx_OCT_AT_list.append(NOx_OCT_AT_list[i])
        if NOx_OCT_AT_list[i]<median_NOx_OCT_AT:
            lower_NOx_OCT_AT_list.append(NOx_OCT_AT_list[i])
                
    upper_quartile_NOx_OCT_AT = statistics.median(upper_NOx_OCT_AT_list)
    lower_quartile_NOx_OCT_AT = statistics.median(lower_NOx_OCT_AT_list)
if flights_OCT_AT > 0:                
    print("Number of entries OCT_AT :",len(NOx_OCT_AT))
    print("             Mean OCT_AT :",mean_NOx_OCT_AT)
    print("            Stdev OCT_AT :",std_NOx_OCT_AT)
    print("           Median OCT_AT :",median_NOx_OCT_AT)
    print("               Q3 OCT_AT :",upper_quartile_NOx_OCT_AT)
    print("               Q1 OCT_AT :",lower_quartile_NOx_OCT_AT)
#OCT_NA
print("Entries for OCT_NA", flights_OCT_NA)
if len(NOx_OCT_NA) > 1:
    NOx_OCT_NA_list = [float(n) for n in NOx_OCT_NA]
    mean_NOx_OCT_NA = statistics.mean(NOx_OCT_NA_list) 
    std_NOx_OCT_NA = statistics.stdev(NOx_OCT_NA_list) 
    NOx_OCT_NA_list=sorted(NOx_OCT_NA_list)
    median_NOx_OCT_NA = statistics.median(NOx_OCT_NA_list)
    upper_NOx_OCT_NA_list = []
    lower_NOx_OCT_NA_list = []
    
    for i in range(len(NOx_OCT_NA_list)):
        if NOx_OCT_NA_list[i]>median_NOx_OCT_NA:
            upper_NOx_OCT_NA_list.append(NOx_OCT_NA_list[i])
        if NOx_OCT_NA_list[i]<median_NOx_OCT_NA:
            lower_NOx_OCT_NA_list.append(NOx_OCT_NA_list[i])
                
    upper_quartile_NOx_OCT_NA = statistics.median(upper_NOx_OCT_NA_list)
    lower_quartile_NOx_OCT_NA = statistics.median(lower_NOx_OCT_NA_list)
if flights_OCT_NA > 0:
    print("Number of entries OCT_NA :", len(NOx_OCT_NA))
    print("             Mean OCT_NA :",mean_NOx_OCT_NA)
    print("            Stdev OCT_NA :",std_NOx_OCT_NA)
    print("           Median OCT_NA :",median_NOx_OCT_NA)
    print("               Q3 OCT_NA :",upper_quartile_NOx_OCT_NA)
    print("               Q1 OCT_NA :",lower_quartile_NOx_OCT_NA)
###########################################################################
############################################################################
#NOV_EU
print("Entries for NOV_EU", flights_NOV_EU)
if len(NOx_NOV_EU) > 1:
    NOx_NOV_EU_list = [float(n) for n in NOx_NOV_EU]
    mean_NOx_NOV_EU = statistics.mean(NOx_NOV_EU_list) 
    std_NOx_NOV_EU = statistics.stdev(NOx_NOV_EU_list) 
    NOx_NOV_EU_list=sorted(NOx_NOV_EU_list)
    median_NOx_NOV_EU = statistics.median(NOx_NOV_EU_list)
    upper_NOx_NOV_EU_list = []
    lower_NOx_NOV_EU_list = []
    
    for i in range(len(NOx_NOV_EU_list)):
        if NOx_NOV_EU_list[i]>median_NOx_NOV_EU:
            upper_NOx_NOV_EU_list.append(NOx_NOV_EU_list[i])
        if NOx_NOV_EU_list[i]<median_NOx_NOV_EU:
            lower_NOx_NOV_EU_list.append(NOx_NOV_EU_list[i])
                
    upper_quartile_NOx_NOV_EU = statistics.median(upper_NOx_NOV_EU_list)
    lower_quartile_NOx_NOV_EU = statistics.median(lower_NOx_NOV_EU_list)
if flights_NOV_EU > 0:                
    print("Number of entries NOV_EU :",len(NOx_NOV_EU))
    print("             Mean NOV_EU :",mean_NOx_NOV_EU)
    print("            Stdev NOV_EU :",std_NOx_NOV_EU)
    print("           Median NOV_EU :",median_NOx_NOV_EU)
    print("               Q3 NOV_EU :",upper_quartile_NOx_NOV_EU)
    print("               Q1 NOV_EU :",lower_quartile_NOx_NOV_EU)
#NOV_AT
print("Entries for NOV_AT", flights_NOV_AT)
if len(NOx_NOV_AT) > 1:
    NOx_NOV_AT_list = [float(n) for n in NOx_NOV_AT]
    mean_NOx_NOV_AT = statistics.mean(NOx_NOV_AT_list) 
    std_NOx_NOV_AT = statistics.stdev(NOx_NOV_AT_list) 
    NOx_NOV_AT_list=sorted(NOx_NOV_AT_list)
    median_NOx_NOV_AT = statistics.median(NOx_NOV_AT_list)
    upper_NOx_NOV_AT_list = []
    lower_NOx_NOV_AT_list = []
    
    for i in range(len(NOx_NOV_AT_list)):
        if NOx_NOV_AT_list[i]>median_NOx_NOV_AT:
            upper_NOx_NOV_AT_list.append(NOx_NOV_AT_list[i])
        if NOx_NOV_AT_list[i]<median_NOx_NOV_AT:
            lower_NOx_NOV_AT_list.append(NOx_NOV_AT_list[i])
                
    upper_quartile_NOx_NOV_AT = statistics.median(upper_NOx_NOV_AT_list)
    lower_quartile_NOx_NOV_AT = statistics.median(lower_NOx_NOV_AT_list)
if flights_NOV_AT > 0:
    print("Number of entries NOV_AT :",len(NOx_NOV_AT))
    print("             Mean NOV_AT :",mean_NOx_NOV_AT)
    print("            Stdev NOV_AT :",std_NOx_NOV_AT)
    print("           Median NOV_AT :",median_NOx_NOV_AT)
    print("               Q3 NOV_AT :",upper_quartile_NOx_NOV_AT)
    print("               Q1 NOV_AT :",lower_quartile_NOx_NOV_AT)
#NOV_NA
print("Entries for NOV_NA", flights_NOV_NA)
if len(NOx_NOV_NA) > 1:
    NOx_NOV_NA_list = [float(n) for n in NOx_NOV_NA]
    mean_NOx_NOV_NA = statistics.mean(NOx_NOV_NA_list) 
    std_NOx_NOV_NA = statistics.stdev(NOx_NOV_NA_list) 
    NOx_NOV_NA_list=sorted(NOx_NOV_NA_list)
    median_NOx_NOV_NA = statistics.median(NOx_NOV_NA_list)
    upper_NOx_NOV_NA_list = []
    lower_NOx_NOV_NA_list = []
    
    for i in range(len(NOx_NOV_NA_list)):
        if NOx_NOV_NA_list[i]>median_NOx_NOV_NA:
            upper_NOx_NOV_NA_list.append(NOx_NOV_NA_list[i])
        if NOx_NOV_NA_list[i]<median_NOx_NOV_NA:
            lower_NOx_NOV_NA_list.append(NOx_NOV_NA_list[i])
                
    upper_quartile_NOx_NOV_NA = statistics.median(upper_NOx_NOV_NA_list)
    lower_quartile_NOx_NOV_NA = statistics.median(lower_NOx_NOV_NA_list)
if flights_NOV_NA > 0:                
    print("Number of entries NOV_NA :", len(NOx_NOV_NA))
    print("             Mean NOV_NA :",mean_NOx_NOV_NA)
    print("            Stdev NOV_NA :",std_NOx_NOV_NA)
    print("           Median NOV_NA :",median_NOx_NOV_NA)
    print("               Q3 NOV_NA :",upper_quartile_NOx_NOV_NA)
    print("               Q1 NOV_NA :",lower_quartile_NOx_NOV_NA)
###########################################################################
############################################################################
#DEC_EU
print("Entries for DEC_EU", flights_DEC_EU)
if len(NOx_DEC_EU) > 1:
    NOx_DEC_EU_list = [float(n) for n in NOx_DEC_EU]
    mean_NOx_DEC_EU = statistics.mean(NOx_DEC_EU_list) 
    std_NOx_DEC_EU = statistics.stdev(NOx_DEC_EU_list) 
    NOx_DEC_EU_list=sorted(NOx_DEC_EU_list)
    median_NOx_DEC_EU = statistics.median(NOx_DEC_EU_list)
    upper_NOx_DEC_EU_list = []
    lower_NOx_DEC_EU_list = []
    
    for i in range(len(NOx_DEC_EU_list)):
        if NOx_DEC_EU_list[i]>median_NOx_DEC_EU:
            upper_NOx_DEC_EU_list.append(NOx_DEC_EU_list[i])
        if NOx_DEC_EU_list[i]<median_NOx_DEC_EU:
            lower_NOx_DEC_EU_list.append(NOx_DEC_EU_list[i])
                
    upper_quartile_NOx_DEC_EU = statistics.median(upper_NOx_DEC_EU_list)
    lower_quartile_NOx_DEC_EU = statistics.median(lower_NOx_DEC_EU_list)
if flights_DEC_EU > 0:                
    print("Number of entries DEC_EU :",len(NOx_DEC_EU))
    print("             Mean DEC_EU :",mean_NOx_DEC_EU)
    print("            Stdev DEC_EU :",std_NOx_DEC_EU)
    print("           Median DEC_EU :",median_NOx_DEC_EU)
    print("               Q3 DEC_EU :",upper_quartile_NOx_DEC_EU)
    print("               Q1 DEC_EU :",lower_quartile_NOx_DEC_EU)
#DEC_AT
print("Entries for DEC_AT", flights_DEC_AT)
if len(NOx_DEC_AT) > 1:
    NOx_DEC_AT_list = [float(n) for n in NOx_DEC_AT]
    mean_NOx_DEC_AT = statistics.mean(NOx_DEC_AT_list) 
    std_NOx_DEC_AT = statistics.stdev(NOx_DEC_AT_list) 
    NOx_DEC_AT_list=sorted(NOx_DEC_AT_list)
    median_NOx_DEC_AT = statistics.median(NOx_DEC_AT_list)
    upper_NOx_DEC_AT_list = []
    lower_NOx_DEC_AT_list = []
    
    for i in range(len(NOx_DEC_AT_list)):
        if NOx_DEC_AT_list[i]>median_NOx_DEC_AT:
            upper_NOx_DEC_AT_list.append(NOx_DEC_AT_list[i])
        if NOx_DEC_AT_list[i]<median_NOx_DEC_AT:
            lower_NOx_DEC_AT_list.append(NOx_DEC_AT_list[i])
                
    upper_quartile_NOx_DEC_AT = statistics.median(upper_NOx_DEC_AT_list)
    lower_quartile_NOx_DEC_AT = statistics.median(lower_NOx_DEC_AT_list)
if flights_DEC_AT > 0:                
    print("Number of entries DEC_AT :",len(NOx_DEC_AT))
    print("             Mean DEC_AT :",mean_NOx_DEC_AT)
    print("            Stdev DEC_AT :",std_NOx_DEC_AT)
    print("           Median DEC_AT :",median_NOx_DEC_AT)
    print("               Q3 DEC_AT :",upper_quartile_NOx_DEC_AT)
    print("               Q1 DEC_AT :",lower_quartile_NOx_DEC_AT)
#DEC_NA
print("Entries for DEC_NA", flights_DEC_NA)
if len(NOx_DEC_NA) > 1:
    NOx_DEC_NA_list = [float(n) for n in NOx_DEC_NA]
    mean_NOx_DEC_NA = statistics.mean(NOx_DEC_NA_list) 
    std_NOx_DEC_NA = statistics.stdev(NOx_DEC_NA_list) 
    NOx_DEC_NA_list=sorted(NOx_DEC_NA_list)
    median_NOx_DEC_NA = statistics.median(NOx_DEC_NA_list)
    upper_NOx_DEC_NA_list = []
    lower_NOx_DEC_NA_list = []
    
    for i in range(len(NOx_DEC_NA_list)):
        if NOx_DEC_NA_list[i]>median_NOx_DEC_NA:
            upper_NOx_DEC_NA_list.append(NOx_DEC_NA_list[i])
        if NOx_DEC_NA_list[i]<median_NOx_DEC_NA:
            lower_NOx_DEC_NA_list.append(NOx_DEC_NA_list[i])
                
    upper_quartile_NOx_DEC_NA = statistics.median(upper_NOx_DEC_NA_list)
    lower_quartile_NOx_DEC_NA = statistics.median(lower_NOx_DEC_NA_list)
if flights_DEC_NA > 0:
    print("Number of entries DEC_NA :", len(NOx_DEC_NA))
    print("             Mean DEC_NA :",mean_NOx_DEC_NA)
    print("            Stdev DEC_NA :",std_NOx_DEC_NA)
    print("           Median DEC_NA :",median_NOx_DEC_NA)
    print("               Q3 DEC_NA :",upper_quartile_NOx_DEC_NA)
    print("               Q1 DEC_NA :",lower_quartile_NOx_DEC_NA)
###########################################################################

#print(len(counts_JUL_NA))
#print(len(NOx_JUL_NA))
NOx_JUL_NA_list = [float(n) for n in NOx_JUL_NA]

#set plot parameters
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (20, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.rcParams.update(params)
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_ylabel('NOx (ppb)')       
ax1.set_xlabel('No of measurements')       
ax1.plot(counts_JUL_NA, NOx_JUL_NA_list, color='tab:red', label='NOx')  
ax1.tick_params(axis='y', labelcolor=color)
plt.axhline(y=median_NOx_JUL_NA, linestyle='-.', color='tab:red')
legend = ax1.legend(loc='upper left', shadow=True, fontsize='large')
fig.suptitle('NOx_JUL_NA')
#plt.show()
plt.savefig("plots/backgrounds/NOx_JUL_NA.png")
plt.clf()

#print(len(counts_AUG_NA))
#print(len(NOx_AUG_NA))
NOx_AUG_NA_list = [float(n) for n in NOx_AUG_NA]

#set plot parameters
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (20, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.rcParams.update(params)
fig, ax1 = plt.subplots()
#color = 'tab:red'
ax1.set_ylabel('NOx (ppb)')       
ax1.set_xlabel('No of measurements')       
ax1.plot(counts_AUG_NA, NOx_AUG_NA_list, color='tab:red', label='NOx')  
ax1.tick_params(axis='y', labelcolor=color)
plt.axhline(y=median_NOx_AUG_NA, linestyle='-.', color='tab:red')
legend = ax1.legend(loc='upper left', shadow=True, fontsize='large')
fig.suptitle('NOx_AUG_NA')
#plt.show()
plt.savefig("plots/backgrounds/NOx_AUG_NA.png")
plt.clf()

print(len(counts_JUN_NA))
print(len(NOx_JUN_NA))
NOx_JUN_NA_list = [float(n) for n in NOx_JUN_NA]

#set plot parameters
#params = {'legend.fontsize': 'x-large',
#          'figure.figsize': (20, 5),
#         'axes.labelsize': 'x-large',
#         'axes.titlesize':'x-large',
#         'xtick.labelsize':'x-large',
#         'ytick.labelsize':'x-large'}
#plt.rcParams.update(params)
fig, ax1 = plt.subplots()
#color = 'tab:red'
ax1.set_ylabel('NOx (ppb)')       
ax1.set_xlabel('No of measurements')       
ax1.plot(counts_JUN_NA, NOx_JUN_NA_list, color='tab:red', label='NOx')  
ax1.tick_params(axis='y', labelcolor=color)
plt.axhline(y=median_NOx_JUN_NA, linestyle='-.', color='tab:red')
legend = ax1.legend(loc='upper left', shadow=True, fontsize='large')
fig.suptitle('NOx_JUN_NA')
#plt.show()
plt.savefig("plots/backgrounds/NOx_JUN_NA.png")
plt.clf()

#Box and whisker plot of values of NOx background each month for each region
data_MAY = NOx_MAY_NA
data_JUN = NOx_JUN_NA
data_JUL = NOx_JUL_NA
data_AUG = NOx_AUG_NA 
data_SEP = NOx_SEP_NA 
data_OCT = NOx_OCT_NA 
data_NOV = NOx_NOV_NA 
data_DEC = NOx_DEC_NA 
data = [data_MAY, data_JUN, data_JUL, data_AUG, data_SEP, data_OCT, data_NOV, data_DEC] 
  
fig1, ax1 = plt.subplots()
ax1.set_title('NOx Background North America 2015')
ax1.boxplot(data, labels=['MAY','JUN','JUL','AUG','SEP', 'OCT', 'NOV', 'DEC'], showfliers=False)
plt.savefig("plots/backgrounds/NOx_NA.png")
plt.clf()

#Box and whisker plot of values of NOx background each month for each region
data_MAY = NOx_MAY_AT
data_JUN = NOx_JUN_AT
data_JUL = NOx_JUL_AT
data_AUG = NOx_AUG_AT 
data_SEP = NOx_SEP_AT 
data_OCT = NOx_OCT_AT 
data_NOV = NOx_NOV_AT 
data_DEC = NOx_DEC_AT 
data = [data_MAY, data_JUN, data_JUL, data_AUG, data_SEP, data_OCT, data_NOV, data_DEC] 
  
fig1, ax1 = plt.subplots()
ax1.set_title('NOx Background Atlantic 2015')
ax1.boxplot(data, labels=['MAY','JUN','JUL','AUG','SEP', 'OCT', 'NOV', 'DEC'], showfliers=False)
plt.savefig("plots/backgrounds/NOx_AT.png")
plt.clf()

#Box and whisker plot of values of NOx background each month for each region
data_MAY = NOx_MAY_EU
data_JUN = NOx_JUN_EU
data_JUL = NOx_JUL_EU
data_AUG = NOx_AUG_EU 
data_SEP = NOx_SEP_EU 
data_OCT = NOx_OCT_EU 
data_NOV = NOx_NOV_EU 
data_DEC = NOx_DEC_EU 
data = [data_MAY, data_JUN, data_JUL, data_AUG, data_SEP, data_OCT, data_NOV, data_DEC] 
  
fig1, ax1 = plt.subplots()
ax1.set_title('NOx Background Europe 2015')
ax1.boxplot(data, labels=['MAY', 'JUN','JUL','AUG','SEP', 'OCT', 'NOV', 'DEC'], showfliers=False)
plt.savefig("plots/backgrounds/NOx_EU.png")
plt.clf()



