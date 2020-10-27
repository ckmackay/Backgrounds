#!/usr/bin/env python
# coding: utf-8

# CO backgrounds for different regions around the world
# C. Mackay 27 October 2020

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

co_vars = [c for c in df if c.startswith("data_vars_") and ("CO") in c and not "_err" in c and not "_stat" in c and not "_val" in c and not "CO2" in c] #selects only IAGOS-CORE flights (17247 in total)

flights_with_CO = df.loc[(df[co_vars] > 0).any(axis="columns")]

flights_with_CO_02 = flights_with_CO.loc["2002-01-01":]

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
        locals()['CO_{}_{}'.format(months[i],zones[j])] = []

        #create corresponding lists for each month in each zone for counts of NOx values for plotting

for i in range(len(months)):
    for j in range(len(zones)):
        locals()['counts_{}_{}'.format(months[i],zones[j])] = []

flight_no=0

nof=100 # limit to nof flights
for i in range(len(flights_with_CO_02)):
#for i in range(nof):
  
    flights_with_CO_02.drivers_load_args.iloc[i]
    ds = xr.load_dataset(*json.loads(flights_with_CO_02.drivers_load_args.iloc[i])["args"])
  
    start_datetime=(ds.departure_UTC_time)
    #print(ds.departure_UTC_time)
    date_time = start_datetime.split("T")
    date = date_time[0]
    time = datetime.datetime.strptime(date, "%Y-%m-%d")
    #print(date)       
    ds['data_vars_cruise'] = xr.where(ds["air_press_AC"]<30000, True, False)
    
    if ds.source=='IAGOS-MOZAIC':
        #print('Selected MOZAIC')
        data_CO = ds.CO_PM.where(ds.data_vars_cruise==True)
    elif ds.source=='IAGOS-CORE':
        #print("Selected CORE")
        data_CO = ds.CO_P1.where(ds.data_vars_cruise==True)
    elif ds.source=="IAGOS-CARIBIC":
        #print("Selected CARIBIC")
        #if ds.CO_PC1.any() > 0:
        if date < '2005-05-19':
            #print('Using CO_PC1')
            data_CO = ds.CO_PC1.where(ds.data_vars_cruise==True)
        elif date >= '2005-05-19':    
        #elif ds.CO_PC2.any() > 0:
            #print('Using CO_PC2')
            data_CO = ds.CO_PC2.where(ds.data_vars_cruise==True)
        else:
            print('Did not find CARIBIC data:', ds.source)
    else: 
        print('Did not find source:', ds.source)    
        
    t=ds.UTC_time.where(ds.data_vars_cruise==True)
    lon=ds.lon.where(ds.data_vars_cruise==True)
    lat=ds.lat.where(ds.data_vars_cruise==True)

    flight_no+=1

    k = 0
    for k in range(len(months)):
    #print(k+1)
        if time.month==k+1:
            locals()['flights_{}'.format(months[k])] += 1
            for j in range(len(lon)):
                for l in range(len(zones)):
                    if lon[j]<= locals()['{}_long_max'.format(zones[l])] and lon[j] >= globals()['{}_long_min'.format(zones[l])] and lat[j]<= globals()['{}_lat_max'.format(zones[l])] and lat[j] >= globals()['{}_lat_min'.format(zones[l])]:
                        if data_CO[j] > 0.00:
                            temp=data_CO[j]
                            locals()['CO_{}_{}'.format(months[k],zones[l])].append(temp)
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

#JAN_EU
##############################################################################
print("Entries for JAN_EU", flights_JAN_EU)
if len(CO_JAN_EU) > 1:
    CO_JAN_EU_list = [float(n) for n in CO_JAN_EU]
    mean_CO_JAN_EU = statistics.mean(CO_JAN_EU_list) 
    std_CO_JAN_EU = statistics.stdev(CO_JAN_EU_list) 
    CO_JAN_EU_list=sorted(CO_JAN_EU_list)
    median_CO_JAN_EU = statistics.median(CO_JAN_EU_list)
    upper_CO_JAN_EU_list = []
    lower_CO_JAN_EU_list = []

    for i in range(len(CO_JAN_EU_list)):
        if CO_JAN_EU_list[i]>median_CO_JAN_EU:
            upper_CO_JAN_EU_list.append(CO_JAN_EU_list[i])
        if CO_JAN_EU_list[i]<median_CO_JAN_EU:
            lower_CO_JAN_EU_list.append(CO_JAN_EU_list[i])
        
    upper_quartile_CO_JAN_EU = statistics.median(upper_CO_JAN_EU_list)
    lower_quartile_CO_JAN_EU = statistics.median(lower_CO_JAN_EU_list)
if flights_JAN_EU > 0:
    print("Number of entries JAN_EU :",len(CO_JAN_EU))
    print("             Mean JAN_EU :",mean_CO_JAN_EU)
    print("            Stdev JAN_EU :",std_CO_JAN_EU)
    print("           Median JAN_EU :",median_CO_JAN_EU)
    print("               Q3 JAN_EU :",upper_quartile_CO_JAN_EU)
    print("               Q1 JAN_EU :",lower_quartile_CO_JAN_EU)
#JAN_AT
print("Entries for JAN_AT", flights_JAN_AT)
if len(CO_JAN_AT) > 1:
    CO_JAN_AT_list = [float(n) for n in CO_JAN_AT]
    mean_CO_JAN_AT = statistics.mean(CO_JAN_AT_list)
    std_CO_JAN_AT = statistics.stdev(CO_JAN_AT_list)
    CO_JAN_AT_list=sorted(CO_JAN_AT_list)
    median_CO_JAN_AT = statistics.median(CO_JAN_AT_list)
    upper_CO_JAN_AT_list = []
    lower_CO_JAN_AT_list = []
    
    for i in range(len(CO_JAN_AT_list)):
        if CO_JAN_AT_list[i]>median_CO_JAN_AT:
            upper_CO_JAN_AT_list.append(CO_JAN_AT_list[i])
        if CO_JAN_AT_list[i]<median_CO_JAN_AT:
            lower_CO_JAN_AT_list.append(CO_JAN_AT_list[i])
                
    upper_quartile_CO_JAN_AT = statistics.median(upper_CO_JAN_AT_list)
    lower_quartile_CO_JAN_AT = statistics.median(lower_CO_JAN_AT_list)
if flights_JAN_AT > 0:
    print("Number of entries JAN_AT :",len(CO_JAN_AT))
    print("             Mean JAN_AT :",mean_CO_JAN_AT)
    print("            Stdev JAN_AT :",std_CO_JAN_AT)
    print("           Median JAN_AT :",median_CO_JAN_AT)
    print("               Q3 JAN_AT :",upper_quartile_CO_JAN_AT)
    print("               Q1 JAN_AT :",lower_quartile_CO_JAN_AT)
#JAN_NA
print("Entries for JAN_NA", flights_JAN_NA)
if len(CO_JAN_NA) > 1:
    CO_JAN_NA_list = [float(n) for n in CO_JAN_NA]
    #print(CO_JUN_NA_list)
    mean_CO_JAN_NA = statistics.mean(CO_JAN_NA_list) 
    std_CO_JAN_NA = statistics.stdev(CO_JAN_NA_list) 
    CO_JAN_NA_list=sorted(CO_JAN_NA_list)
    median_CO_JAN_NA = statistics.median(CO_JAN_NA_list)
    upper_CO_JAN_NA_list = []
    lower_CO_JAN_NA_list = []
    
    for i in range(len(CO_JAN_NA_list)):
        if CO_JAN_NA_list[i]>median_CO_JAN_NA:
            upper_CO_JAN_NA_list.append(CO_JAN_NA_list[i])
        if CO_JAN_NA_list[i]<median_CO_JAN_NA:
            lower_CO_JAN_NA_list.append(CO_JAN_NA_list[i])
                
    upper_quartile_CO_JAN_NA = statistics.median(upper_CO_JAN_NA_list)
    lower_quartile_CO_JAN_NA = statistics.median(lower_CO_JAN_NA_list)
if flights_JAN_NA > 0:                
    print("Number of entries JAN_NA :", len(CO_JAN_NA))
    print("             Mean JAN_NA :",mean_CO_JAN_NA)
    print("            Stdev JAN_NA :",std_CO_JAN_NA)
    print("           Median JAN_NA :",median_CO_JAN_NA)
    print("               Q3 JAN_NA :",upper_quartile_CO_JAN_NA)
    print("               Q1 JAN_NA :",lower_quartile_CO_JAN_NA)
###########################################################################
##############################################################################
#FEB_EU
print("Entries for FEB_EU", flights_FEB_EU)
if len(CO_FEB_EU) > 1:
    CO_FEB_EU_list = [float(n) for n in CO_FEB_EU]
    mean_CO_FEB_EU = statistics.mean(CO_FEB_EU_list) 
    std_CO_FEB_EU = statistics.stdev(CO_FEB_EU_list) 
    CO_FEB_EU_list=sorted(CO_FEB_EU_list)
    median_CO_FEB_EU = statistics.median(CO_FEB_EU_list)
    upper_CO_FEB_EU_list = []
    lower_CO_FEB_EU_list = []

    for i in range(len(CO_FEB_EU_list)):
        if CO_FEB_EU_list[i]>median_CO_FEB_EU:
            upper_CO_FEB_EU_list.append(CO_FEB_EU_list[i])
        if CO_FEB_EU_list[i]<median_CO_FEB_EU:
            lower_CO_FEB_EU_list.append(CO_FEB_EU_list[i])
        
    upper_quartile_CO_FEB_EU = statistics.median(upper_CO_FEB_EU_list)
    lower_quartile_CO_FEB_EU = statistics.median(lower_CO_FEB_EU_list)
if flights_FEB_EU > 0:
    print("Number of entries FEB_EU :",len(CO_FEB_EU))
    print("             Mean FEB_EU :",mean_CO_FEB_EU)
    print("            Stdev FEB_EU :",std_CO_FEB_EU)
    print("           Median FEB_EU :",median_CO_FEB_EU)
    print("               Q3 FEB_EU :",upper_quartile_CO_FEB_EU)
    print("               Q1 FEB_EU :",lower_quartile_CO_FEB_EU)
#FEB_AT
print("Entries for FEB_AT", flights_FEB_AT)
if len(CO_FEB_AT) > 1:
    CO_FEB_AT_list = [float(n) for n in CO_FEB_AT]
    mean_CO_FEB_AT = statistics.mean(CO_FEB_AT_list)
    std_CO_FEB_AT = statistics.stdev(CO_FEB_AT_list)
    CO_FEB_AT_list=sorted(CO_FEB_AT_list)
    median_CO_FEB_AT = statistics.median(CO_FEB_AT_list)
    upper_CO_FEB_AT_list = []
    lower_CO_FEB_AT_list = []
    
    for i in range(len(CO_FEB_AT_list)):
        if CO_FEB_AT_list[i]>median_CO_FEB_AT:
            upper_CO_FEB_AT_list.append(CO_FEB_AT_list[i])
        if CO_FEB_AT_list[i]<median_CO_FEB_AT:
            lower_CO_FEB_AT_list.append(CO_FEB_AT_list[i])
                
    upper_quartile_CO_FEB_AT = statistics.median(upper_CO_FEB_AT_list)
    lower_quartile_CO_FEB_AT = statistics.median(lower_CO_FEB_AT_list)
if flights_FEB_AT > 0:
    print("Number of entries FEB_AT :",len(CO_FEB_AT))
    print("             Mean FEB_AT :",mean_CO_FEB_AT)
    print("            Stdev FEB_AT :",std_CO_FEB_AT)
    print("           Median FEB_AT :",median_CO_FEB_AT)
    print("               Q3 FEB_AT :",upper_quartile_CO_FEB_AT)
    print("               Q1 FEB_AT :",lower_quartile_CO_FEB_AT)
#FEB_NA
print("Entries for FEB_NA", flights_FEB_NA)
if len(CO_FEB_NA) > 1:
    CO_FEB_NA_list = [float(n) for n in CO_FEB_NA]
    #print(CO_JUN_NA_list)
    mean_CO_FEB_NA = statistics.mean(CO_FEB_NA_list) 
    std_CO_FEB_NA = statistics.stdev(CO_FEB_NA_list) 
    CO_FEB_NA_list=sorted(CO_FEB_NA_list)
    median_CO_FEB_NA = statistics.median(CO_FEB_NA_list)
    upper_CO_FEB_NA_list = []
    lower_CO_FEB_NA_list = []
    
    for i in range(len(CO_FEB_NA_list)):
        if CO_FEB_NA_list[i]>median_CO_FEB_NA:
            upper_CO_FEB_NA_list.append(CO_FEB_NA_list[i])
        if CO_FEB_NA_list[i]<median_CO_FEB_NA:
            lower_CO_FEB_NA_list.append(CO_FEB_NA_list[i])
                
    upper_quartile_CO_FEB_NA = statistics.median(upper_CO_FEB_NA_list)
    lower_quartile_CO_FEB_NA = statistics.median(lower_CO_FEB_NA_list)
if flights_FEB_NA > 0:                
    print("Number of entries FEB_NA :", len(CO_FEB_NA))
    print("             Mean FEB_NA :",mean_CO_FEB_NA)
    print("            Stdev FEB_NA :",std_CO_FEB_NA)
    print("           Median FEB_NA :",median_CO_FEB_NA)
    print("               Q3 FEB_NA :",upper_quartile_CO_FEB_NA)
    print("               Q1 FEB_NA :",lower_quartile_CO_FEB_NA)
###########################################################################
##############################################################################
#MAR_EU
print("Entries for MAR_EU", flights_MAR_EU)
if len(CO_MAR_EU) > 1:
    CO_MAR_EU_list = [float(n) for n in CO_MAR_EU]
    mean_CO_MAR_EU = statistics.mean(CO_MAR_EU_list) 
    std_CO_MAR_EU = statistics.stdev(CO_MAR_EU_list) 
    CO_MAR_EU_list=sorted(CO_MAR_EU_list)
    median_CO_MAR_EU = statistics.median(CO_MAR_EU_list)
    upper_CO_MAR_EU_list = []
    lower_CO_MAR_EU_list = []

    for i in range(len(CO_MAR_EU_list)):
        if CO_MAR_EU_list[i]>median_CO_MAR_EU:
            upper_CO_MAR_EU_list.append(CO_MAR_EU_list[i])
        if CO_MAR_EU_list[i]<median_CO_MAR_EU:
            lower_CO_MAR_EU_list.append(CO_MAR_EU_list[i])
        
    upper_quartile_CO_MAR_EU = statistics.median(upper_CO_MAR_EU_list)
    lower_quartile_CO_MAR_EU = statistics.median(lower_CO_MAR_EU_list)
if flights_MAR_EU > 0:
    print("Number of entries MAR_EU :",len(CO_MAR_EU))
    print("             Mean MAR_EU :",mean_CO_MAR_EU)
    print("            Stdev MAR_EU :",std_CO_MAR_EU)
    print("           Median MAR_EU :",median_CO_MAR_EU)
    print("               Q3 MAR_EU :",upper_quartile_CO_MAR_EU)
    print("               Q1 MAR_EU :",lower_quartile_CO_MAR_EU)
#MAR_AT
print("Entries for MAR_AT", flights_MAR_AT)
if len(CO_MAR_AT) > 1:
    CO_MAR_AT_list = [float(n) for n in CO_MAR_AT]
    mean_CO_MAR_AT = statistics.mean(CO_MAR_AT_list)
    std_CO_MAR_AT = statistics.stdev(CO_MAR_AT_list)
    CO_MAR_AT_list=sorted(CO_MAR_AT_list)
    median_CO_MAR_AT = statistics.median(CO_MAR_AT_list)
    upper_CO_MAR_AT_list = []
    lower_CO_MAR_AT_list = []
    
    for i in range(len(CO_MAR_AT_list)):
        if CO_MAR_AT_list[i]>median_CO_MAR_AT:
            upper_CO_MAR_AT_list.append(CO_MAR_AT_list[i])
        if CO_MAR_AT_list[i]<median_CO_MAR_AT:
            lower_CO_MAR_AT_list.append(CO_MAR_AT_list[i])
                
    upper_quartile_CO_MAR_AT = statistics.median(upper_CO_MAR_AT_list)
    lower_quartile_CO_MAR_AT = statistics.median(lower_CO_MAR_AT_list)
if flights_MAR_AT > 0:
    print("Number of entries MAR_AT :",len(CO_MAR_AT))
    print("             Mean MAR_AT :",mean_CO_MAR_AT)
    print("            Stdev MAR_AT :",std_CO_MAR_AT)
    print("           Median MAR_AT :",median_CO_MAR_AT)
    print("               Q3 MAR_AT :",upper_quartile_CO_MAR_AT)
    print("               Q1 MAR_AT :",lower_quartile_CO_MAR_AT)
#MAR_NA
print("Entries for MAR_NA", flights_MAR_NA)
if len(CO_MAR_NA) > 1:
    CO_MAR_NA_list = [float(n) for n in CO_MAR_NA]
    #print(CO_JUN_NA_list)
    mean_CO_MAR_NA = statistics.mean(CO_MAR_NA_list) 
    std_CO_MAR_NA = statistics.stdev(CO_MAR_NA_list) 
    CO_MAR_NA_list=sorted(CO_MAR_NA_list)
    median_CO_MAR_NA = statistics.median(CO_MAR_NA_list)
    upper_CO_MAR_NA_list = []
    lower_CO_MAR_NA_list = []
    
    for i in range(len(CO_MAR_NA_list)):
        if CO_MAR_NA_list[i]>median_CO_MAR_NA:
            upper_CO_MAR_NA_list.append(CO_MAR_NA_list[i])
        if CO_MAR_NA_list[i]<median_CO_MAR_NA:
            lower_CO_MAR_NA_list.append(CO_MAR_NA_list[i])
                
    upper_quartile_CO_MAR_NA = statistics.median(upper_CO_MAR_NA_list)
    lower_quartile_CO_MAR_NA = statistics.median(lower_CO_MAR_NA_list)
if flights_MAR_NA > 0:                
    print("Number of entries MAR_NA :", len(CO_MAR_NA))
    print("             Mean MAR_NA :",mean_CO_MAR_NA)
    print("            Stdev MAR_NA :",std_CO_MAR_NA)
    print("           Median MAR_NA :",median_CO_MAR_NA)
    print("               Q3 MAR_NA :",upper_quartile_CO_MAR_NA)
    print("               Q1 MAR_NA :",lower_quartile_CO_MAR_NA)
###########################################################################
##############################################################################
#APR_EU
print("Entries for APR_EU", flights_APR_EU)
if len(CO_APR_EU) > 1:
    CO_APR_EU_list = [float(n) for n in CO_APR_EU]
    mean_CO_APR_EU = statistics.mean(CO_APR_EU_list) 
    std_CO_APR_EU = statistics.stdev(CO_APR_EU_list) 
    CO_APR_EU_list=sorted(CO_APR_EU_list)
    median_CO_APR_EU = statistics.median(CO_APR_EU_list)
    upper_CO_APR_EU_list = []
    lower_CO_APR_EU_list = []

    for i in range(len(CO_APR_EU_list)):
        if CO_APR_EU_list[i]>median_CO_APR_EU:
            upper_CO_APR_EU_list.append(CO_APR_EU_list[i])
        if CO_APR_EU_list[i]<median_CO_APR_EU:
            lower_CO_APR_EU_list.append(CO_APR_EU_list[i])
        
    upper_quartile_CO_APR_EU = statistics.median(upper_CO_APR_EU_list)
    lower_quartile_CO_APR_EU = statistics.median(lower_CO_APR_EU_list)
if flights_APR_EU > 0:
    print("Number of entries APR_EU :",len(CO_APR_EU))
    print("             Mean APR_EU :",mean_CO_APR_EU)
    print("            Stdev APR_EU :",std_CO_APR_EU)
    print("           Median APR_EU :",median_CO_APR_EU)
    print("               Q3 APR_EU :",upper_quartile_CO_APR_EU)
    print("               Q1 APR_EU :",lower_quartile_CO_APR_EU)
#APR_AT
print("Entries for APR_AT", flights_APR_AT)
if len(CO_APR_AT) > 1:
    CO_APR_AT_list = [float(n) for n in CO_APR_AT]
    mean_CO_APR_AT = statistics.mean(CO_APR_AT_list)
    std_CO_APR_AT = statistics.stdev(CO_APR_AT_list)
    CO_APR_AT_list=sorted(CO_APR_AT_list)
    median_CO_APR_AT = statistics.median(CO_APR_AT_list)
    upper_CO_APR_AT_list = []
    lower_CO_APR_AT_list = []
    
    for i in range(len(CO_APR_AT_list)):
        if CO_APR_AT_list[i]>median_CO_APR_AT:
            upper_CO_APR_AT_list.append(CO_APR_AT_list[i])
        if CO_APR_AT_list[i]<median_CO_APR_AT:
            lower_CO_APR_AT_list.append(CO_APR_AT_list[i])
                
    upper_quartile_CO_APR_AT = statistics.median(upper_CO_APR_AT_list)
    lower_quartile_CO_APR_AT = statistics.median(lower_CO_APR_AT_list)
if flights_APR_AT > 0:
    print("Number of entries APR_AT :",len(CO_APR_AT))
    print("             Mean APR_AT :",mean_CO_APR_AT)
    print("            Stdev APR_AT :",std_CO_APR_AT)
    print("           Median APR_AT :",median_CO_APR_AT)
    print("               Q3 APR_AT :",upper_quartile_CO_APR_AT)
    print("               Q1 APR_AT :",lower_quartile_CO_APR_AT)
#APR_NA
print("Entries for APR_NA", flights_APR_NA)
if len(CO_APR_NA) > 1:
    CO_APR_NA_list = [float(n) for n in CO_APR_NA]
    #print(CO_JUN_NA_list)
    mean_CO_APR_NA = statistics.mean(CO_APR_NA_list) 
    std_CO_APR_NA = statistics.stdev(CO_APR_NA_list) 
    CO_APR_NA_list=sorted(CO_APR_NA_list)
    median_CO_APR_NA = statistics.median(CO_APR_NA_list)
    upper_CO_APR_NA_list = []
    lower_CO_APR_NA_list = []
    
    for i in range(len(CO_APR_NA_list)):
        if CO_APR_NA_list[i]>median_CO_APR_NA:
            upper_CO_APR_NA_list.append(CO_APR_NA_list[i])
        if CO_APR_NA_list[i]<median_CO_APR_NA:
            lower_CO_APR_NA_list.append(CO_APR_NA_list[i])
                
    upper_quartile_CO_APR_NA = statistics.median(upper_CO_APR_NA_list)
    lower_quartile_CO_APR_NA = statistics.median(lower_CO_APR_NA_list)
if flights_APR_NA > 0:                
    print("Number of entries APR_NA :", len(CO_APR_NA))
    print("             Mean APR_NA :",mean_CO_APR_NA)
    print("            Stdev APR_NA :",std_CO_APR_NA)
    print("           Median APR_NA :",median_CO_APR_NA)
    print("               Q3 APR_NA :",upper_quartile_CO_APR_NA)
    print("               Q1 APR_NA :",lower_quartile_CO_APR_NA)    
##############################################################################
##############################################################################
#MAY_EU
print("Entries for MAY_EU", flights_MAY_EU)
if len(CO_MAY_EU) > 1:
    CO_MAY_EU_list = [float(n) for n in CO_MAY_EU]
    mean_CO_MAY_EU = statistics.mean(CO_MAY_EU_list) 
    std_CO_MAY_EU = statistics.stdev(CO_MAY_EU_list) 
    CO_MAY_EU_list=sorted(CO_MAY_EU_list)
    median_CO_MAY_EU = statistics.median(CO_MAY_EU_list)
    upper_CO_MAY_EU_list = []
    lower_CO_MAY_EU_list = []

    for i in range(len(CO_MAY_EU_list)):
        if CO_MAY_EU_list[i]>median_CO_MAY_EU:
            upper_CO_MAY_EU_list.append(CO_MAY_EU_list[i])
        if CO_MAY_EU_list[i]<median_CO_MAY_EU:
            lower_CO_MAY_EU_list.append(CO_MAY_EU_list[i])
        
    upper_quartile_CO_MAY_EU = statistics.median(upper_CO_MAY_EU_list)
    lower_quartile_CO_MAY_EU = statistics.median(lower_CO_MAY_EU_list)
if flights_MAY_EU > 0:
    print("Number of entries MAY_EU :",len(CO_MAY_EU))
    print("             Mean MAY_EU :",mean_CO_MAY_EU)
    print("            Stdev MAY_EU :",std_CO_MAY_EU)
    print("           Median MAY_EU :",median_CO_MAY_EU)
    print("               Q3 MAY_EU :",upper_quartile_CO_MAY_EU)
    print("               Q1 MAY_EU :",lower_quartile_CO_MAY_EU)
#MAY_AT
print("Entries for MAY_AT", flights_MAY_AT)
if len(CO_MAY_AT) > 1:
    CO_MAY_AT_list = [float(n) for n in CO_MAY_AT]
    mean_CO_MAY_AT = statistics.mean(CO_MAY_AT_list)
    std_CO_MAY_AT = statistics.stdev(CO_MAY_AT_list)
    CO_MAY_AT_list=sorted(CO_MAY_AT_list)
    median_CO_MAY_AT = statistics.median(CO_MAY_AT_list)
    upper_CO_MAY_AT_list = []
    lower_CO_MAY_AT_list = []
    
    for i in range(len(CO_MAY_AT_list)):
        if CO_MAY_AT_list[i]>median_CO_MAY_AT:
            upper_CO_MAY_AT_list.append(CO_MAY_AT_list[i])
        if CO_MAY_AT_list[i]<median_CO_MAY_AT:
            lower_CO_MAY_AT_list.append(CO_MAY_AT_list[i])
                
    upper_quartile_CO_MAY_AT = statistics.median(upper_CO_MAY_AT_list)
    lower_quartile_CO_MAY_AT = statistics.median(lower_CO_MAY_AT_list)
if flights_MAY_AT > 0:
    print("Number of entries MAY_AT :",len(CO_MAY_AT))
    print("             Mean MAY_AT :",mean_CO_MAY_AT)
    print("            Stdev MAY_AT :",std_CO_MAY_AT)
    print("           Median MAY_AT :",median_CO_MAY_AT)
    print("               Q3 MAY_AT :",upper_quartile_CO_MAY_AT)
    print("               Q1 MAY_AT :",lower_quartile_CO_MAY_AT)
#MAY_NA
print("Entries for MAY_NA", flights_MAY_NA)
if len(CO_MAY_NA) > 1:
    CO_MAY_NA_list = [float(n) for n in CO_MAY_NA]
    #print(CO_JUN_NA_list)
    mean_CO_MAY_NA = statistics.mean(CO_MAY_NA_list) 
    std_CO_MAY_NA = statistics.stdev(CO_MAY_NA_list) 
    CO_MAY_NA_list=sorted(CO_MAY_NA_list)
    median_CO_MAY_NA = statistics.median(CO_MAY_NA_list)
    upper_CO_MAY_NA_list = []
    lower_CO_MAY_NA_list = []
    
    for i in range(len(CO_MAY_NA_list)):
        if CO_MAY_NA_list[i]>median_CO_MAY_NA:
            upper_CO_MAY_NA_list.append(CO_MAY_NA_list[i])
        if CO_MAY_NA_list[i]<median_CO_MAY_NA:
            lower_CO_MAY_NA_list.append(CO_MAY_NA_list[i])
                
    upper_quartile_CO_MAY_NA = statistics.median(upper_CO_MAY_NA_list)
    lower_quartile_CO_MAY_NA = statistics.median(lower_CO_MAY_NA_list)
if flights_MAY_NA > 0:                
    print("Number of entries MAY_NA :", len(CO_MAY_NA))
    print("             Mean MAY_NA :",mean_CO_MAY_NA)
    print("            Stdev MAY_NA :",std_CO_MAY_NA)
    print("           Median MAY_NA :",median_CO_MAY_NA)
    print("               Q3 MAY_NA :",upper_quartile_CO_MAY_NA)
    print("               Q1 MAY_NA :",lower_quartile_CO_MAY_NA)
###########################################################################
############################################################################print("Entries for JUN_EU", flights_JUN_EU)
if len(CO_JUN_EU) > 1:
    CO_JUN_EU_list = [float(n) for n in CO_JUN_EU]
    mean_CO_JUN_EU = statistics.mean(CO_JUN_EU_list) 
    std_CO_JUN_EU = statistics.stdev(CO_JUN_EU_list) 
    CO_JUN_EU_list=sorted(CO_JUN_EU_list)
    median_CO_JUN_EU = statistics.median(CO_JUN_EU_list)
    upper_CO_JUN_EU_list = []
    lower_CO_JUN_EU_list = []

    for i in range(len(CO_JUN_EU_list)):
        if CO_JUN_EU_list[i]>median_CO_JUN_EU:
            upper_CO_JUN_EU_list.append(CO_JUN_EU_list[i])
        if CO_JUN_EU_list[i]<median_CO_JUN_EU:
            lower_CO_JUN_EU_list.append(CO_JUN_EU_list[i])
        
    upper_quartile_CO_JUN_EU = statistics.median(upper_CO_JUN_EU_list)
    lower_quartile_CO_JUN_EU = statistics.median(lower_CO_JUN_EU_list)
if flights_JUN_EU > 0:
    print("Number of entries JUN_EU :",len(CO_JUN_EU))
    print("             Mean JUN_EU :",mean_CO_JUN_EU)
    print("            Stdev JUN_EU :",std_CO_JUN_EU)
    print("           Median JUN_EU :",median_CO_JUN_EU)
    print("               Q3 JUN_EU :",upper_quartile_CO_JUN_EU)
    print("               Q1 JUN_EU :",lower_quartile_CO_JUN_EU)
#JUN_AT
print("Entries for JUN_AT", flights_JUN_AT)
if len(CO_JUN_AT) > 1:
    CO_JUN_AT_list = [float(n) for n in CO_JUN_AT]
    mean_CO_JUN_AT = statistics.mean(CO_JUN_AT_list)
    std_CO_JUN_AT = statistics.stdev(CO_JUN_AT_list)
    CO_JUN_AT_list=sorted(CO_JUN_AT_list)
    median_CO_JUN_AT = statistics.median(CO_JUN_AT_list)
    upper_CO_JUN_AT_list = []
    lower_CO_JUN_AT_list = []
    
    for i in range(len(CO_JUN_AT_list)):
        if CO_JUN_AT_list[i]>median_CO_JUN_AT:
            upper_CO_JUN_AT_list.append(CO_JUN_AT_list[i])
        if CO_JUN_AT_list[i]<median_CO_JUN_AT:
            lower_CO_JUN_AT_list.append(CO_JUN_AT_list[i])
                
    upper_quartile_CO_JUN_AT = statistics.median(upper_CO_JUN_AT_list)
    lower_quartile_CO_JUN_AT = statistics.median(lower_CO_JUN_AT_list)
if flights_JUN_AT > 0:
    print("Number of entries JUN_AT :",len(CO_JUN_AT))
    print("             Mean JUN_AT :",mean_CO_JUN_AT)
    print("            Stdev JUN_AT :",std_CO_JUN_AT)
    print("           Median JUN_AT :",median_CO_JUN_AT)
    print("               Q3 JUN_AT :",upper_quartile_CO_JUN_AT)
    print("               Q1 JUN_AT :",lower_quartile_CO_JUN_AT)
#JUN_NA
print("Entries for JUN_NA", flights_JUN_NA)
if len(CO_JUN_NA) > 1:
    CO_JUN_NA_list = [float(n) for n in CO_JUN_NA]
    #print(CO_JUN_NA_list)
    mean_CO_JUN_NA = statistics.mean(CO_JUN_NA_list) 
    std_CO_JUN_NA = statistics.stdev(CO_JUN_NA_list) 
    CO_JUN_NA_list=sorted(CO_JUN_NA_list)
    median_CO_JUN_NA = statistics.median(CO_JUN_NA_list)
    upper_CO_JUN_NA_list = []
    lower_CO_JUN_NA_list = []
    
    for i in range(len(CO_JUN_NA_list)):
        if CO_JUN_NA_list[i]>median_CO_JUN_NA:
            upper_CO_JUN_NA_list.append(CO_JUN_NA_list[i])
        if CO_JUN_NA_list[i]<median_CO_JUN_NA:
            lower_CO_JUN_NA_list.append(CO_JUN_NA_list[i])
                
    upper_quartile_CO_JUN_NA = statistics.median(upper_CO_JUN_NA_list)
    lower_quartile_CO_JUN_NA = statistics.median(lower_CO_JUN_NA_list)
if flights_JUN_NA > 0:                
    print("Number of entries JUN_NA :", len(CO_JUN_NA))
    print("             Mean JUN_NA :",mean_CO_JUN_NA)
    print("            Stdev JUN_NA :",std_CO_JUN_NA)
    print("           Median JUN_NA :",median_CO_JUN_NA)
    print("               Q3 JUN_NA :",upper_quartile_CO_JUN_NA)
    print("               Q1 JUN_NA :",lower_quartile_CO_JUN_NA)
###########################################################################
############################################################################
#JUL_EU
print("Entries for JUL_EU", flights_JUL_EU)
if len(CO_JUL_EU) > 1:
    CO_JUL_EU_list = [float(n) for n in CO_JUL_EU]
    mean_CO_JUL_EU = statistics.mean(CO_JUL_EU_list) 
    std_CO_JUL_EU = statistics.stdev(CO_JUL_EU_list) 
    CO_JUL_EU_list=sorted(CO_JUL_EU_list)
    median_CO_JUL_EU = statistics.median(CO_JUL_EU_list)
    upper_CO_JUL_EU_list = []
    lower_CO_JUL_EU_list = []
    
    for i in range(len(CO_JUL_EU_list)):
        if CO_JUL_EU_list[i]>median_CO_JUL_EU:
            upper_CO_JUL_EU_list.append(CO_JUL_EU_list[i])
        if CO_JUL_EU_list[i]<median_CO_JUL_EU:
            lower_CO_JUL_EU_list.append(CO_JUL_EU_list[i])
                
    upper_quartile_CO_JUL_EU = statistics.median(upper_CO_JUL_EU_list)
    lower_quartile_CO_JUL_EU = statistics.median(lower_CO_JUL_EU_list)
if flights_JUL_EU > 0:                
    print("Number of entries JUL_EU :",len(CO_JUL_EU))
    print("             Mean JUL_EU :",mean_CO_JUL_EU)
    print("            Stdev JUL_EU :",std_CO_JUL_EU)
    print("           Median JUL_EU :",median_CO_JUL_EU)
    print("               Q3 JUL_EU :",upper_quartile_CO_JUL_EU)
    print("               Q1 JUL_EU :",lower_quartile_CO_JUL_EU)
#JUL_AT
print("Entries for JUL_AT", flights_JUL_AT)
if len(CO_JUL_AT) > 1:
    CO_JUL_AT_list = [float(n) for n in CO_JUL_AT]
    mean_CO_JUL_AT = statistics.mean(CO_JUL_AT_list) 
    std_CO_JUL_AT = statistics.stdev(CO_JUL_AT_list) 
    CO_JUL_AT_list=sorted(CO_JUL_AT_list)
    median_CO_JUL_AT = statistics.median(CO_JUL_AT_list)
    upper_CO_JUL_AT_list = []
    lower_CO_JUL_AT_list = []
    
    for i in range(len(CO_JUL_AT_list)):
        if CO_JUL_AT_list[i]>median_CO_JUL_AT:
            upper_CO_JUL_AT_list.append(CO_JUL_AT_list[i])
        if CO_JUL_AT_list[i]<median_CO_JUL_AT:
            lower_CO_JUL_AT_list.append(CO_JUL_AT_list[i])
                
    upper_quartile_CO_JUL_AT = statistics.median(upper_CO_JUL_AT_list)
    lower_quartile_CO_JUL_AT = statistics.median(lower_CO_JUL_AT_list)
if flights_JUL_AT > 0:                            
    print("Number of entries JUL_AT :",len(CO_JUL_AT))
    print("             Mean JUL_AT :",mean_CO_JUL_AT)
    print("            Stdev JUL_AT :",std_CO_JUL_AT)
    print("           Median JUL_AT :",median_CO_JUL_AT)
    print("               Q3 JUL_AT :",upper_quartile_CO_JUL_AT)
    print("               Q1 JUL_AT :",lower_quartile_CO_JUL_AT)
#JUL_NA
print("Entries for JUL_NA", flights_JUL_NA)
if len(CO_JUL_NA) > 1:
    CO_JUL_NA_list = [float(n) for n in CO_JUL_NA]
    mean_CO_JUL_NA = statistics.mean(CO_JUL_NA_list) 
    std_CO_JUL_NA = statistics.stdev(CO_JUL_NA_list) 
    CO_JUL_NA_list=sorted(CO_JUL_NA_list)
    median_CO_JUL_NA = statistics.median(CO_JUL_NA_list)
    upper_CO_JUL_NA_list = []
    lower_CO_JUL_NA_list = []
    
    for i in range(len(CO_JUL_NA_list)):
        if CO_JUL_NA_list[i]>median_CO_JUL_NA:
            upper_CO_JUL_NA_list.append(CO_JUL_NA_list[i])
        if CO_JUL_NA_list[i]<median_CO_JUL_NA:
            lower_CO_JUL_NA_list.append(CO_JUL_NA_list[i])
                
    upper_quartile_CO_JUL_NA = statistics.median(upper_CO_JUL_NA_list)
    lower_quartile_CO_JUL_NA = statistics.median(lower_CO_JUL_NA_list)
if flights_JUL_NA > 0:
    print("Number of entries JUL_NA :", len(CO_JUL_NA))
    print("             Mean JUL_NA :",mean_CO_JUL_NA)
    print("            Stdev JUL_NA :",std_CO_JUL_NA)
    print("           Median JUL_NA :",median_CO_JUL_NA)
    print("               Q3 JUL_NA :",upper_quartile_CO_JUL_NA)
    print("               Q1 JUL_NA :",lower_quartile_CO_JUL_NA)
###########################################################################
############################################################################
#AUG_EU
print("Entries for AUG_EU", flights_AUG_EU)
if len(CO_AUG_EU) > 1:
    CO_AUG_EU_list = [float(n) for n in CO_AUG_EU]
    mean_CO_AUG_EU = statistics.mean(CO_AUG_EU_list) 
    std_CO_AUG_EU = statistics.stdev(CO_AUG_EU_list) 
    CO_AUG_EU_list=sorted(CO_AUG_EU_list)
    median_CO_AUG_EU = statistics.median(CO_AUG_EU_list)
    upper_CO_AUG_EU_list = []
    lower_CO_AUG_EU_list = []
    
    for i in range(len(CO_AUG_EU_list)):
        if CO_AUG_EU_list[i]>median_CO_AUG_EU:
            upper_CO_AUG_EU_list.append(CO_AUG_EU_list[i])
        if CO_AUG_EU_list[i]<median_CO_AUG_EU:
            lower_CO_AUG_EU_list.append(CO_AUG_EU_list[i])
                
    upper_quartile_CO_AUG_EU = statistics.median(upper_CO_AUG_EU_list)
    lower_quartile_CO_AUG_EU = statistics.median(lower_CO_AUG_EU_list)
if flights_AUG_EU > 0:                
    print("Number of entries AUG_EU :",len(CO_AUG_EU))
    print("             Mean AUG_EU :",mean_CO_AUG_EU)
    print("            Stdev AUG_EU :",std_CO_AUG_EU)
    print("           Median AUG_EU :",median_CO_AUG_EU)
    print("               Q3 AUG_EU :",upper_quartile_CO_AUG_EU)
    print("               Q1 AUG_EU :",lower_quartile_CO_AUG_EU)
#AUG_AT
print("Entries for AUG_AT", flights_AUG_AT)
if len(CO_AUG_AT) > 1:
    CO_AUG_AT_list = [float(n) for n in CO_AUG_AT]
    mean_CO_AUG_AT = statistics.mean(CO_AUG_AT_list) 
    std_CO_AUG_AT = statistics.stdev(CO_AUG_AT_list) 
    CO_AUG_AT_list=sorted(CO_AUG_AT_list)
    median_CO_AUG_AT = statistics.median(CO_AUG_AT_list)
    upper_CO_AUG_AT_list = []
    lower_CO_AUG_AT_list = []
    
    for i in range(len(CO_AUG_AT_list)):
        if CO_AUG_AT_list[i]>median_CO_AUG_AT:
            upper_CO_AUG_AT_list.append(CO_AUG_AT_list[i])
        if CO_AUG_AT_list[i]<median_CO_AUG_AT:
            lower_CO_AUG_AT_list.append(CO_AUG_AT_list[i])
                
    upper_quartile_CO_AUG_AT = statistics.median(upper_CO_AUG_AT_list)
    lower_quartile_CO_AUG_AT = statistics.median(lower_CO_AUG_AT_list)
if flights_AUG_AT > 0:                
    print("Number of entries AUG_AT :",len(CO_AUG_AT))
    print("             Mean AUG_AT :",mean_CO_AUG_AT)
    print("            Stdev AUG_AT :",std_CO_AUG_AT)
    print("           Median AUG_AT :",median_CO_AUG_AT)
    print("               Q3 AUG_AT :",upper_quartile_CO_AUG_AT)
    print("               Q1 AUG_AT :",lower_quartile_CO_AUG_AT)
#AUG_NA
print("Entries for AUG_NA", flights_AUG_NA)
if len(CO_AUG_NA) > 1:
    CO_AUG_NA_list = [float(n) for n in CO_AUG_NA]
    mean_CO_AUG_NA = statistics.mean(CO_AUG_NA_list) 
    std_CO_AUG_NA = statistics.stdev(CO_AUG_NA_list) 
    CO_AUG_NA_list=sorted(CO_AUG_NA_list)
    median_CO_AUG_NA = statistics.median(CO_AUG_NA_list)
    upper_CO_AUG_NA_list = []
    lower_CO_AUG_NA_list = []
    
    for i in range(len(CO_AUG_NA_list)):
        if CO_AUG_NA_list[i]>median_CO_AUG_NA:
            upper_CO_AUG_NA_list.append(CO_AUG_NA_list[i])
        if CO_AUG_NA_list[i]<median_CO_AUG_NA:
            lower_CO_AUG_NA_list.append(CO_AUG_NA_list[i])
                
    upper_quartile_CO_AUG_NA = statistics.median(upper_CO_AUG_NA_list)
    lower_quartile_CO_AUG_NA = statistics.median(lower_CO_AUG_NA_list)
if flights_AUG_NA > 0:                
    print("Number of entries AUG_NA :", len(CO_AUG_NA))
    print("             Mean AUG_NA :",mean_CO_AUG_NA)
    print("            Stdev AUG_NA :",std_CO_AUG_NA)
    print("           Median AUG_NA :",median_CO_AUG_NA)
    print("               Q3 AUG_NA :",upper_quartile_CO_AUG_NA)
    print("               Q1 AUG_NA :",lower_quartile_CO_AUG_NA)
###########################################################################
############################################################################
#SEP_EU
print("Entries for SEP_EU", flights_SEP_EU)
print("len of sep EU", len(CO_SEP_EU))
if len(CO_SEP_EU) > 1:
    CO_SEP_EU_list = [float(n) for n in CO_SEP_EU]
    mean_CO_SEP_EU = statistics.mean(CO_SEP_EU_list) 
    std_CO_SEP_EU = statistics.stdev(CO_SEP_EU_list) 
    CO_SEP_EU_list=sorted(CO_SEP_EU_list)
    median_CO_SEP_EU = statistics.median(CO_SEP_EU_list)
    upper_CO_SEP_EU_list = []
    lower_CO_SEP_EU_list = []
    
    for i in range(len(CO_SEP_EU_list)):
        if CO_SEP_EU_list[i]>median_CO_SEP_EU:
            upper_CO_SEP_EU_list.append(CO_SEP_EU_list[i])
        if CO_SEP_EU_list[i]<median_CO_SEP_EU:
            lower_CO_SEP_EU_list.append(CO_SEP_EU_list[i])
                
    upper_quartile_CO_SEP_EU = statistics.median(upper_CO_SEP_EU_list)
    lower_quartile_CO_SEP_EU = statistics.median(lower_CO_SEP_EU_list)
if flights_SEP_EU > 0:                
    print("Number of entries SEP_EU :",len(CO_SEP_EU))
    print("             Mean SEP_EU :",mean_CO_SEP_EU)
    print("            Stdev SEP_EU :",std_CO_SEP_EU)
    print("           Median SEP_EU :",median_CO_SEP_EU)
    print("               Q3 SEP_EU :",upper_quartile_CO_SEP_EU)
    print("               Q1 SEP_EU :",lower_quartile_CO_SEP_EU)
#SEP_AT
print("Entries for SEP_AT", flights_SEP_AT)
if len(CO_SEP_AT) > 1:
    CO_SEP_AT_list = [float(n) for n in CO_SEP_AT]
    mean_CO_SEP_AT = statistics.mean(CO_SEP_AT_list) 
    std_CO_SEP_AT = statistics.stdev(CO_SEP_AT_list) 
    CO_SEP_AT_list=sorted(CO_SEP_AT_list)
    median_CO_SEP_AT = statistics.median(CO_SEP_AT_list)
    upper_CO_SEP_AT_list = []
    lower_CO_SEP_AT_list = []
    
    for i in range(len(CO_SEP_AT_list)):
        if CO_SEP_AT_list[i]>median_CO_SEP_AT:
            upper_CO_SEP_AT_list.append(CO_SEP_AT_list[i])
        if CO_SEP_AT_list[i]<median_CO_SEP_AT:
            lower_CO_SEP_AT_list.append(CO_SEP_AT_list[i])
                
    upper_quartile_CO_SEP_AT = statistics.median(upper_CO_SEP_AT_list)
    lower_quartile_CO_SEP_AT = statistics.median(lower_CO_SEP_AT_list)
if flights_SEP_AT > 0:
    print("Number of entries SEP_AT :",len(CO_SEP_AT))
    print("             Mean SEP_AT :",mean_CO_SEP_AT)
    print("            Stdev SEP_AT :",std_CO_SEP_AT)
    print("           Median SEP_AT :",median_CO_SEP_AT)
    print("               Q3 SEP_AT :",upper_quartile_CO_SEP_AT)
    print("               Q1 SEP_AT :",lower_quartile_CO_SEP_AT)
#SEP_NA
print("Entries for SEP_NA", flights_SEP_NA)
if len(CO_SEP_NA) > 1:
    CO_SEP_NA_list = [float(n) for n in CO_SEP_NA]
    mean_CO_SEP_NA = statistics.mean(CO_SEP_NA_list) 
    std_CO_SEP_NA = statistics.stdev(CO_SEP_NA_list) 
    CO_SEP_NA_list=sorted(CO_SEP_NA_list)
    median_CO_SEP_NA = statistics.median(CO_SEP_NA_list)
    upper_CO_SEP_NA_list = []
    lower_CO_SEP_NA_list = []
    
    for i in range(len(CO_SEP_NA_list)):
        if CO_SEP_NA_list[i]>median_CO_SEP_NA:
            upper_CO_SEP_NA_list.append(CO_SEP_NA_list[i])
        if CO_SEP_NA_list[i]<median_CO_SEP_NA:
            lower_CO_SEP_NA_list.append(CO_SEP_NA_list[i])
                
    upper_quartile_CO_SEP_NA = statistics.median(upper_CO_SEP_NA_list)
    lower_quartile_CO_SEP_NA = statistics.median(lower_CO_SEP_NA_list)
if flights_SEP_NA > 0:            
    print("Number of entries SEP_NA :", len(CO_SEP_NA))
    print("             Mean SEP_NA :",mean_CO_SEP_NA)
    print("            Stdev SEP_NA :",std_CO_SEP_NA)
    print("           Median SEP_NA :",median_CO_SEP_NA)
    print("               Q3 SEP_NA :",upper_quartile_CO_SEP_NA)
    print("               Q1 SEP_NA :",lower_quartile_CO_SEP_NA)
###########################################################################
############################################################################
#OCT_EU
print("Entries for OCT_EU", flights_OCT_EU)
if len(CO_OCT_EU) > 1:
    CO_OCT_EU_list = [float(n) for n in CO_OCT_EU]
    mean_CO_OCT_EU = statistics.mean(CO_OCT_EU_list) 
    std_CO_OCT_EU = statistics.stdev(CO_OCT_EU_list) 
    CO_OCT_EU_list=sorted(CO_OCT_EU_list)
    median_CO_OCT_EU = statistics.median(CO_OCT_EU_list)
    upper_CO_OCT_EU_list = []
    lower_CO_OCT_EU_list = []
    
    for i in range(len(CO_OCT_EU_list)):
        if CO_OCT_EU_list[i]>median_CO_OCT_EU:
            upper_CO_OCT_EU_list.append(CO_OCT_EU_list[i])
        if CO_OCT_EU_list[i]<median_CO_OCT_EU:
            lower_CO_OCT_EU_list.append(CO_OCT_EU_list[i])
                
    upper_quartile_CO_OCT_EU = statistics.median(upper_CO_OCT_EU_list)
    lower_quartile_CO_OCT_EU = statistics.median(lower_CO_OCT_EU_list)
if flights_OCT_EU > 0:                
    print("Number of entries OCT_EU :",len(CO_OCT_EU))
    print("             Mean OCT_EU :",mean_CO_OCT_EU)
    print("            Stdev OCT_EU :",std_CO_OCT_EU)
    print("           Median OCT_EU :",median_CO_OCT_EU)
    print("               Q3 OCT_EU :",upper_quartile_CO_OCT_EU)
    print("               Q1 OCT_EU :",lower_quartile_CO_OCT_EU)
#OCT_AT
print("Entries for OCT_AT", flights_OCT_AT)
if len(CO_OCT_AT) > 1:
    CO_OCT_AT_list = [float(n) for n in CO_OCT_AT]
    mean_CO_OCT_AT = statistics.mean(CO_OCT_AT_list) 
    std_CO_OCT_AT = statistics.stdev(CO_OCT_AT_list) 
    CO_OCT_AT_list=sorted(CO_OCT_AT_list)
    median_CO_OCT_AT = statistics.median(CO_OCT_AT_list)
    upper_CO_OCT_AT_list = []
    lower_CO_OCT_AT_list = []
    
    for i in range(len(CO_OCT_AT_list)):
        if CO_OCT_AT_list[i]>median_CO_OCT_AT:
            upper_CO_OCT_AT_list.append(CO_OCT_AT_list[i])
        if CO_OCT_AT_list[i]<median_CO_OCT_AT:
            lower_CO_OCT_AT_list.append(CO_OCT_AT_list[i])
                
    upper_quartile_CO_OCT_AT = statistics.median(upper_CO_OCT_AT_list)
    lower_quartile_CO_OCT_AT = statistics.median(lower_CO_OCT_AT_list)
if flights_OCT_AT > 0:                
    print("Number of entries OCT_AT :",len(CO_OCT_AT))
    print("             Mean OCT_AT :",mean_CO_OCT_AT)
    print("            Stdev OCT_AT :",std_CO_OCT_AT)
    print("           Median OCT_AT :",median_CO_OCT_AT)
    print("               Q3 OCT_AT :",upper_quartile_CO_OCT_AT)
    print("               Q1 OCT_AT :",lower_quartile_CO_OCT_AT)
#OCT_NA
print("Entries for OCT_NA", flights_OCT_NA)
if len(CO_OCT_NA) > 1:
    CO_OCT_NA_list = [float(n) for n in CO_OCT_NA]
    mean_CO_OCT_NA = statistics.mean(CO_OCT_NA_list) 
    std_CO_OCT_NA = statistics.stdev(CO_OCT_NA_list) 
    CO_OCT_NA_list=sorted(CO_OCT_NA_list)
    median_CO_OCT_NA = statistics.median(CO_OCT_NA_list)
    upper_CO_OCT_NA_list = []
    lower_CO_OCT_NA_list = []
    
    for i in range(len(CO_OCT_NA_list)):
        if CO_OCT_NA_list[i]>median_CO_OCT_NA:
            upper_CO_OCT_NA_list.append(CO_OCT_NA_list[i])
        if CO_OCT_NA_list[i]<median_CO_OCT_NA:
            lower_CO_OCT_NA_list.append(CO_OCT_NA_list[i])
                
    upper_quartile_CO_OCT_NA = statistics.median(upper_CO_OCT_NA_list)
    lower_quartile_CO_OCT_NA = statistics.median(lower_CO_OCT_NA_list)
if flights_OCT_NA > 0:
    print("Number of entries OCT_NA :", len(CO_OCT_NA))
    print("             Mean OCT_NA :",mean_CO_OCT_NA)
    print("            Stdev OCT_NA :",std_CO_OCT_NA)
    print("           Median OCT_NA :",median_CO_OCT_NA)
    print("               Q3 OCT_NA :",upper_quartile_CO_OCT_NA)
    print("               Q1 OCT_NA :",lower_quartile_CO_OCT_NA)
###########################################################################
############################################################################
#NOV_EU
print("Entries for NOV_EU", flights_NOV_EU)
if len(CO_NOV_EU) > 1:
    CO_NOV_EU_list = [float(n) for n in CO_NOV_EU]
    mean_CO_NOV_EU = statistics.mean(CO_NOV_EU_list) 
    std_CO_NOV_EU = statistics.stdev(CO_NOV_EU_list) 
    CO_NOV_EU_list=sorted(CO_NOV_EU_list)
    median_CO_NOV_EU = statistics.median(CO_NOV_EU_list)
    upper_CO_NOV_EU_list = []
    lower_CO_NOV_EU_list = []
    
    for i in range(len(CO_NOV_EU_list)):
        if CO_NOV_EU_list[i]>median_CO_NOV_EU:
            upper_CO_NOV_EU_list.append(CO_NOV_EU_list[i])
        if CO_NOV_EU_list[i]<median_CO_NOV_EU:
            lower_CO_NOV_EU_list.append(CO_NOV_EU_list[i])
                
    upper_quartile_CO_NOV_EU = statistics.median(upper_CO_NOV_EU_list)
    lower_quartile_CO_NOV_EU = statistics.median(lower_CO_NOV_EU_list)
if flights_NOV_EU > 0:                
    print("Number of entries NOV_EU :",len(CO_NOV_EU))
    print("             Mean NOV_EU :",mean_CO_NOV_EU)
    print("            Stdev NOV_EU :",std_CO_NOV_EU)
    print("           Median NOV_EU :",median_CO_NOV_EU)
    print("               Q3 NOV_EU :",upper_quartile_CO_NOV_EU)
    print("               Q1 NOV_EU :",lower_quartile_CO_NOV_EU)
#NOV_AT
print("Entries for NOV_AT", flights_NOV_AT)
if len(CO_NOV_AT) > 1:
    CO_NOV_AT_list = [float(n) for n in CO_NOV_AT]
    mean_CO_NOV_AT = statistics.mean(CO_NOV_AT_list) 
    std_CO_NOV_AT = statistics.stdev(CO_NOV_AT_list) 
    CO_NOV_AT_list=sorted(CO_NOV_AT_list)
    median_CO_NOV_AT = statistics.median(CO_NOV_AT_list)
    upper_CO_NOV_AT_list = []
    lower_CO_NOV_AT_list = []
    
    for i in range(len(CO_NOV_AT_list)):
        if CO_NOV_AT_list[i]>median_CO_NOV_AT:
            upper_CO_NOV_AT_list.append(CO_NOV_AT_list[i])
        if CO_NOV_AT_list[i]<median_CO_NOV_AT:
            lower_CO_NOV_AT_list.append(CO_NOV_AT_list[i])
                
    upper_quartile_CO_NOV_AT = statistics.median(upper_CO_NOV_AT_list)
    lower_quartile_CO_NOV_AT = statistics.median(lower_CO_NOV_AT_list)
if flights_NOV_AT > 0:
    print("Number of entries NOV_AT :",len(CO_NOV_AT))
    print("             Mean NOV_AT :",mean_CO_NOV_AT)
    print("            Stdev NOV_AT :",std_CO_NOV_AT)
    print("           Median NOV_AT :",median_CO_NOV_AT)
    print("               Q3 NOV_AT :",upper_quartile_CO_NOV_AT)
    print("               Q1 NOV_AT :",lower_quartile_CO_NOV_AT)
#NOV_NA
print("Entries for NOV_NA", flights_NOV_NA)
if len(CO_NOV_NA) > 1:
    CO_NOV_NA_list = [float(n) for n in CO_NOV_NA]
    mean_CO_NOV_NA = statistics.mean(CO_NOV_NA_list) 
    std_CO_NOV_NA = statistics.stdev(CO_NOV_NA_list) 
    CO_NOV_NA_list=sorted(CO_NOV_NA_list)
    median_CO_NOV_NA = statistics.median(CO_NOV_NA_list)
    upper_CO_NOV_NA_list = []
    lower_CO_NOV_NA_list = []
    
    for i in range(len(CO_NOV_NA_list)):
        if CO_NOV_NA_list[i]>median_CO_NOV_NA:
            upper_CO_NOV_NA_list.append(CO_NOV_NA_list[i])
        if CO_NOV_NA_list[i]<median_CO_NOV_NA:
            lower_CO_NOV_NA_list.append(CO_NOV_NA_list[i])
                
    upper_quartile_CO_NOV_NA = statistics.median(upper_CO_NOV_NA_list)
    lower_quartile_CO_NOV_NA = statistics.median(lower_CO_NOV_NA_list)
if flights_NOV_NA > 0:                
    print("Number of entries NOV_NA :", len(CO_NOV_NA))
    print("             Mean NOV_NA :",mean_CO_NOV_NA)
    print("            Stdev NOV_NA :",std_CO_NOV_NA)
    print("           Median NOV_NA :",median_CO_NOV_NA)
    print("               Q3 NOV_NA :",upper_quartile_CO_NOV_NA)
    print("               Q1 NOV_NA :",lower_quartile_CO_NOV_NA)
###########################################################################
############################################################################
#DEC_EU
print("Entries for DEC_EU", flights_DEC_EU)
if len(CO_DEC_EU) > 1:
    CO_DEC_EU_list = [float(n) for n in CO_DEC_EU]
    mean_CO_DEC_EU = statistics.mean(CO_DEC_EU_list) 
    std_CO_DEC_EU = statistics.stdev(CO_DEC_EU_list) 
    CO_DEC_EU_list=sorted(CO_DEC_EU_list)
    median_CO_DEC_EU = statistics.median(CO_DEC_EU_list)
    upper_CO_DEC_EU_list = []
    lower_CO_DEC_EU_list = []
    
    for i in range(len(CO_DEC_EU_list)):
        if CO_DEC_EU_list[i]>median_CO_DEC_EU:
            upper_CO_DEC_EU_list.append(CO_DEC_EU_list[i])
        if CO_DEC_EU_list[i]<median_CO_DEC_EU:
            lower_CO_DEC_EU_list.append(CO_DEC_EU_list[i])
                
    upper_quartile_CO_DEC_EU = statistics.median(upper_CO_DEC_EU_list)
    lower_quartile_CO_DEC_EU = statistics.median(lower_CO_DEC_EU_list)
if flights_DEC_EU > 0:                
    print("Number of entries DEC_EU :",len(CO_DEC_EU))
    print("             Mean DEC_EU :",mean_CO_DEC_EU)
    print("            Stdev DEC_EU :",std_CO_DEC_EU)
    print("           Median DEC_EU :",median_CO_DEC_EU)
    print("               Q3 DEC_EU :",upper_quartile_CO_DEC_EU)
    print("               Q1 DEC_EU :",lower_quartile_CO_DEC_EU)
#DEC_AT
print("Entries for DEC_AT", flights_DEC_AT)
if len(CO_DEC_AT) > 1:
    CO_DEC_AT_list = [float(n) for n in CO_DEC_AT]
    mean_CO_DEC_AT = statistics.mean(CO_DEC_AT_list) 
    std_CO_DEC_AT = statistics.stdev(CO_DEC_AT_list) 
    CO_DEC_AT_list=sorted(CO_DEC_AT_list)
    median_CO_DEC_AT = statistics.median(CO_DEC_AT_list)
    upper_CO_DEC_AT_list = []
    lower_CO_DEC_AT_list = []
    
    for i in range(len(CO_DEC_AT_list)):
        if CO_DEC_AT_list[i]>median_CO_DEC_AT:
            upper_CO_DEC_AT_list.append(CO_DEC_AT_list[i])
        if CO_DEC_AT_list[i]<median_CO_DEC_AT:
            lower_CO_DEC_AT_list.append(CO_DEC_AT_list[i])
                
    upper_quartile_CO_DEC_AT = statistics.median(upper_CO_DEC_AT_list)
    lower_quartile_CO_DEC_AT = statistics.median(lower_CO_DEC_AT_list)
if flights_DEC_AT > 0:                
    print("Number of entries DEC_AT :",len(CO_DEC_AT))
    print("             Mean DEC_AT :",mean_CO_DEC_AT)
    print("            Stdev DEC_AT :",std_CO_DEC_AT)
    print("           Median DEC_AT :",median_CO_DEC_AT)
    print("               Q3 DEC_AT :",upper_quartile_CO_DEC_AT)
    print("               Q1 DEC_AT :",lower_quartile_CO_DEC_AT)
#DEC_NA
print("Entries for DEC_NA", flights_DEC_NA)
if len(CO_DEC_NA) > 1:
    CO_DEC_NA_list = [float(n) for n in CO_DEC_NA]
    mean_CO_DEC_NA = statistics.mean(CO_DEC_NA_list) 
    std_CO_DEC_NA = statistics.stdev(CO_DEC_NA_list) 
    CO_DEC_NA_list=sorted(CO_DEC_NA_list)
    median_CO_DEC_NA = statistics.median(CO_DEC_NA_list)
    upper_CO_DEC_NA_list = []
    lower_CO_DEC_NA_list = []
    
    for i in range(len(CO_DEC_NA_list)):
        if CO_DEC_NA_list[i]>median_CO_DEC_NA:
            upper_CO_DEC_NA_list.append(CO_DEC_NA_list[i])
        if CO_DEC_NA_list[i]<median_CO_DEC_NA:
            lower_CO_DEC_NA_list.append(CO_DEC_NA_list[i])
                
    upper_quartile_CO_DEC_NA = statistics.median(upper_CO_DEC_NA_list)
    lower_quartile_CO_DEC_NA = statistics.median(lower_CO_DEC_NA_list)
if flights_DEC_NA > 0:
    print("Number of entries DEC_NA :", len(CO_DEC_NA))
    print("             Mean DEC_NA :",mean_CO_DEC_NA)
    print("            Stdev DEC_NA :",std_CO_DEC_NA)
    print("           Median DEC_NA :",median_CO_DEC_NA)
    print("               Q3 DEC_NA :",upper_quartile_CO_DEC_NA)
    print("               Q1 DEC_NA :",lower_quartile_CO_DEC_NA)
###########################################################################

#print(len(counts_JUL_NA))
#print(len(CO_JUL_NA))
CO_JUL_NA_list = [float(n) for n in CO_JUL_NA]

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
ax1.set_ylabel('CO (ppb)')       
ax1.set_xlabel('No of measurements')       
ax1.plot(counts_JUL_NA, CO_JUL_NA_list, color='tab:red', label='CO')  
ax1.tick_params(axis='y', labelcolor=color)
plt.axhline(y=median_CO_JUL_NA, linestyle='-.', color='tab:red')
legend = ax1.legend(loc='upper left', shadow=True, fontsize='large')
fig.suptitle('CO_JUL_NA')
#plt.show()
plt.savefig("plots/backgrounds/CO_JUL_NA.png")
plt.clf()

#print(len(counts_AUG_NA))
#print(len(CO_AUG_NA))
CO_AUG_NA_list = [float(n) for n in CO_AUG_NA]

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
ax1.set_ylabel('CO (ppb)')       
ax1.set_xlabel('No of measurements')       
ax1.plot(counts_AUG_NA, CO_AUG_NA_list, color='tab:red', label='CO')  
ax1.tick_params(axis='y', labelcolor=color)
plt.axhline(y=median_CO_AUG_NA, linestyle='-.', color='tab:red')
legend = ax1.legend(loc='upper left', shadow=True, fontsize='large')
fig.suptitle('CO_AUG_NA')
#plt.show()
plt.savefig("plots/backgrounds/CO_AUG_NA.png")
plt.clf()

print(len(counts_JUN_NA))
print(len(CO_JUN_NA))
CO_JUN_NA_list = [float(n) for n in CO_JUN_NA]

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
ax1.set_ylabel('CO (ppb)')       
ax1.set_xlabel('No of measurements')       
ax1.plot(counts_JUN_NA, CO_JUN_NA_list, color='tab:red', label='CO')  
ax1.tick_params(axis='y', labelcolor=color)
plt.axhline(y=median_CO_JUN_NA, linestyle='-.', color='tab:red')
legend = ax1.legend(loc='upper left', shadow=True, fontsize='large')
fig.suptitle('CO_JUN_NA')
#plt.show()
plt.savefig("plots/backgrounds/CO_JUN_NA.png")
plt.clf()

###########################################################################
#Box and whisker plot of values of CO background each month for each region
###########################################################################
# NA
data_JAN = CO_JAN_NA
data_FEB = CO_FEB_NA
data_MAR = CO_MAR_NA
data_APR = CO_APR_NA
data_MAY = CO_MAY_NA
data_JUN = CO_JUN_NA
data_JUL = CO_JUL_NA
data_AUG = CO_AUG_NA 
data_SEP = CO_SEP_NA 
data_OCT = CO_OCT_NA 
data_NOV = CO_NOV_NA 
data_DEC = CO_DEC_NA 
data = [data_JAN, data_FEB, data_MAR, data_APR, data_MAY, data_JUN, data_JUL, data_AUG, data_SEP, data_OCT, data_NOV, data_DEC] 
  
fig1, ax1 = plt.subplots()
ax1.set_title('CO Background North America 2015')
ax1.boxplot(data, labels=['JAN', 'FEB', 'MAR', 'APR', 'MAY','JUN','JUL','AUG','SEP', 'OCT', 'NOV', 'DEC'], showfliers=False)
plt.savefig("plots/backgrounds/CO_NA.png")
plt.clf()

#Box and whisker plot of values of CO background each month for each region
data_JAN = CO_JAN_AT
data_FEB = CO_FEB_AT
data_MAR = CO_MAR_AT
data_APR = CO_APR_AT
data_MAY = CO_MAY_AT
data_JUN = CO_JUN_AT
data_JUL = CO_JUL_AT
data_AUG = CO_AUG_AT 
data_SEP = CO_SEP_AT 
data_OCT = CO_OCT_AT 
data_NOV = CO_NOV_AT 
data_DEC = CO_DEC_AT 
data = [data_JAN, data_FEB, data_MAR, data_APR, data_MAY, data_JUN, data_JUL, data_AUG, data_SEP, data_OCT, data_NOV, data_DEC] 
  
fig1, ax1 = plt.subplots()
ax1.set_title('CO Background Atlantic 2015')
ax1.boxplot(data, labels=['JAN', 'FEB', 'MAR', 'APR', 'MAY','JUN','JUL','AUG','SEP', 'OCT', 'NOV', 'DEC'], showfliers=False)
plt.savefig("plots/backgrounds/CO_AT.png")
plt.clf()

#Box and whisker plot of values of CO background each month for each region
data_JAN = CO_JAN_EU
data_FEB = CO_FEB_EU
data_MAR = CO_MAR_EU
data_APR = CO_APR_EU
data_MAY = CO_MAY_EU
data_JUN = CO_JUN_EU
data_JUL = CO_JUL_EU
data_AUG = CO_AUG_EU 
data_SEP = CO_SEP_EU 
data_OCT = CO_OCT_EU 
data_NOV = CO_NOV_EU 
data_DEC = CO_DEC_EU 
data = [data_JAN, data_FEB, data_MAR, data_APR, data_MAY, data_JUN, data_JUL, data_AUG, data_SEP, data_OCT, data_NOV, data_DEC] 
  
fig1, ax1 = plt.subplots()
ax1.set_title('CO Background Europe 2015')
ax1.boxplot(data, labels=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN','JUL','AUG','SEP', 'OCT', 'NOV', 'DEC'], showfliers=False)
plt.savefig("plots/backgrounds/CO_EU.png")
plt.clf()



