# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on 2023-03-30

Updated on 2023-07-17

@author: Laurens P. Stoop
"""


# load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import matplotlib.dates as mdates
import matplotlib.transforms as mtransforms



#%%
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'xx-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
pylab.rcParams.update(params)

## colour definitions

# Solar
colour_solar = 'burlywood' # 0.03
colour_solar_clim = 'grey' # 1
colour_solar_hrw = 'tab:red' # 0.7
colour_solar_credi = 'orange'

# Wind
colour_wind = 'skyblue' # 0.03
colour_wind_clim = 'grey' # 1
colour_wind_hrw = 'dodgerblue' # 0.7
colour_wind_credi = 'steelblue'


# Region selection
REGION = 'NL01'
# REGION = 'SK00'
# REGION = 'SE02' 
# REGION = 'FR10'

#%%
# =============================================================================
# Define file locations
# =============================================================================

# Define some folders
FOLDER_project='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/ccmetrics/'

#%%
# =============================================================================
# Get the data to open
# =============================================================================


# Open climatology from disk
if REGION =='NL01':
    ds_SPVanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')
    ds_WONanom = xr.open_dataset(FOLDER_project+'data/processed/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40_additionalYear.nc')
else:
    ds_SPVanom = xr.open_dataset(FOLDER_project+'data/temp/ERA5_SPV_clim-anom_PECD_PEON_hrwCLIM40_additionalYear_'+REGION+'.nc')
    ds_WONanom = xr.open_dataset(FOLDER_project+'data/temp/ERA5_WON_clim-anom_PECD_PEON_hrwCLIM40_additionalYear_'+REGION+'.nc')



#%% WIND
# =============================================================================
# Winter WIND
# =============================================================================

# Initialize the dataframe
df_WEBi = pd.DataFrame()


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    if year == 1991:
        df_WEBi[str(year)] = ds_WONanom.anom.sel(time=slice(str(year)+'-09-01', str(year+1)+'-03-31')).cumsum().to_numpy()
    else:
        df_WEBi[str(year)] = ds_WONanom.anom.sel(time=slice(str(year)+'-09-01', str(year+1)+'-03-31')).cumsum().values

# show years
year_dates = pd.date_range('1999-09-01',periods=5088, freq='1h')

# we start a new figure
fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))
# fig, axes = plt.subplot_mosaic([['a)', 'b)', 'c)']], figsize=(18,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes['a)'].plot(year_dates, df_WEBi[str(year)], color='dodgerblue', alpha=0.3, linewidth=1)
    
axes['a)'].plot(year_dates,df_WEBi['1996'], color='red', label='1996', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['1998'], color='green', label='1998', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['2003'], color='purple', label='2003', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0,  axis=1),
    df_WEBi.quantile(1,  axis=1),
    color='dodgerblue', alpha=0.05, label='min-max'
    )

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0.1,  axis=1),
    df_WEBi.quantile(0.9,  axis=1),
    color='dodgerblue', alpha=0.1, label='10-90%'
    )

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0.25,  axis=1),
    df_WEBi.quantile(0.75,  axis=1),
    color='dodgerblue', alpha=0.2, label='25-75%'
    )

axes['b)'].plot(year_dates,df_WEBi.quantile(0.5,  axis=1), color='dodgerblue', label='50%')

axes['b)'].plot(year_dates,df_WEBi['1996'], color='red', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_WEBi['1998'], color='green', alpha=0.9, linewidth=1)
axes['b)'].plot(year_dates,df_WEBi['2003'], color='purple', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_WEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)


   
# # Add a line through zero
axes['a)'].axhline(y=0.0, color='gray', linestyle='--')
axes['b)'].axhline(y=0.0, color='gray', linestyle='--')

# # add window markers
# axes['a)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes['b)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')





# ## Now fix the nice stuff



# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a in ['a)', 'b)']:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a].xaxis.set_major_formatter(xfmt_years)




# # set the legend and labels
# axes['a)'].legend(loc='lower right', fontsize='medium')
axes['a)'].legend(loc='lower left', fontsize='medium')
axes['b)'].legend(loc='lower left', fontsize='medium')


if REGION == 'NL01':
    axes['a)'].set_ylim(-410,410)
    axes['b)'].set_ylim(-410,410)

# # Fix labels
axes['a)'].set_ylabel('Wind CREDI [FLH]')
# axes['b)'].set_ylabel('Solar Energy Balance index')



# # make it look better
plt.tight_layout()


# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')

if REGION == 'NL01':
    plt.savefig(FOLDER_project+'results/publication/WindCREDI_seasonal-winter.png')
    plt.savefig(FOLDER_project+'results/publication/WindCREDI_seasonal-winter.pdf')
else:
    plt.savefig(FOLDER_project+'results/additional_regions/WindCREDI_seasonal-winter_'+REGION+'.png')
    plt.savefig(FOLDER_project+'results/additional_regions/WindCREDI_seasonal-winter_'+REGION+'.pdf')

plt.show()


#%% WIND
# =============================================================================
# Summer WIND
# =============================================================================

# Initialize the dataframe
df_WEBi = pd.DataFrame()


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    if year == 1991:
        df_WEBi[str(year)] = ds_WONanom.anom.sel(time=slice(str(year)+'-04-01', str(year)+'-08-31')).cumsum().to_numpy()
    else:
        df_WEBi[str(year)] = ds_WONanom.anom.sel(time=slice(str(year)+'-04-01', str(year)+'-08-31')).cumsum().values

# show years
year_dates = pd.date_range('1999-04-01',periods=3672, freq='1h')


# we start a new figure
fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))
# fig, axes = plt.subplot_mosaic([['a)', 'b)', 'c)']], figsize=(18,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes['a)'].plot(year_dates, df_WEBi[str(year)], color='dodgerblue', alpha=0.3, linewidth=1)
    
axes['a)'].plot(year_dates,df_WEBi['1996'], color='red', label='1996', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['1998'], color='green', label='1998', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['2003'], color='purple', label='2003', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_WEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0,  axis=1),
    df_WEBi.quantile(1,  axis=1),
    color='dodgerblue', alpha=0.05, label='min-max'
    )

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0.1,  axis=1),
    df_WEBi.quantile(0.9,  axis=1),
    color='dodgerblue', alpha=0.1, label='10-90%'
    )

axes['b)'].fill_between(
    year_dates, 
    df_WEBi.quantile(0.25,  axis=1),
    df_WEBi.quantile(0.75,  axis=1),
    color='dodgerblue', alpha=0.2, label='25-75%'
    )

axes['b)'].plot(year_dates,df_WEBi.quantile(0.5,  axis=1), color='dodgerblue', label='50%')

axes['b)'].plot(year_dates,df_WEBi['1996'], color='red', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_WEBi['1998'], color='green', alpha=0.9, linewidth=1)
axes['b)'].plot(year_dates,df_WEBi['2003'], color='purple', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_WEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)


   
# # Add a line through zero
axes['a)'].axhline(y=0.0, color='gray', linestyle='--')
axes['b)'].axhline(y=0.0, color='gray', linestyle='--')

# # add window markers
# axes['a)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes['b)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')





# ## Now fix the nice stuff



# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a in ['a)', 'b)']:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a].xaxis.set_major_formatter(xfmt_years)




# # set the legend and labels
# axes['a)'].legend(loc='lower right', fontsize='medium')
axes['a)'].legend(loc='lower left', fontsize='medium')
axes['b)'].legend(loc='lower left', fontsize='medium')


if REGION == 'NL01':
    axes['a)'].set_ylim(-160,160)
    axes['b)'].set_ylim(-160,160)

# # Fix labels
axes['a)'].set_ylabel('Wind CREDI [FLH]')
# axes['b)'].set_ylabel('Solar Energy Balance index')



# # make it look better
plt.tight_layout()


# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')


if REGION == 'NL01':
    plt.savefig(FOLDER_project+'results/publication/WindCREDI_seasonal-summer.png')
    plt.savefig(FOLDER_project+'results/publication/WindCREDI_seasonal-summer.pdf')
else:
    plt.savefig(FOLDER_project+'results/additional_regions/WindCREDI_seasonal-summer_'+REGION+'.png')
    plt.savefig(FOLDER_project+'results/additional_regions/WindCREDI_seasonal-summer_'+REGION+'.pdf')

plt.show()


#%% SOLAR

# =============================================================================
# Summer SOLAR
# =============================================================================

# Initialize the dataframe
df_SEBi = pd.DataFrame()


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    if year == 1991:
        df_SEBi[str(year)] = ds_SPVanom.anom.sel(time=slice(str(year)+'-03-15', str(year)+'-10-15')).cumsum().to_numpy()
    else:
        df_SEBi[str(year)] = ds_SPVanom.anom.sel(time=slice(str(year)+'-03-15', str(year)+'-10-15')).cumsum().values

# show years
year_dates = pd.date_range('1999-03-15',periods=5160, freq='1h')


# we start a new figure
fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))
# fig, axes = plt.subplot_mosaic([['a)', 'b)', 'c)']], figsize=(18,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes['a)'].plot(year_dates, df_SEBi[str(year)], color=colour_solar_credi, alpha=0.5, linewidth=1)
    
axes['a)'].plot(year_dates,df_SEBi['1996'], color='red', label='1996', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['1998'], color='green', label='1998', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['2003'], color='purple', label='2003', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0,  axis=1),
    df_SEBi.quantile(1,  axis=1),
    color=colour_solar_credi, alpha=0.1, label='min-max'
    )

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0.1,  axis=1),
    df_SEBi.quantile(0.9,  axis=1),
    color=colour_solar_credi, alpha=0.2, label='10-90%'
    )

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0.25,  axis=1),
    df_SEBi.quantile(0.75,  axis=1),
    color=colour_solar_credi, alpha=0.4, label='25-75%'
    )

axes['b)'].plot(year_dates,df_SEBi.quantile(0.5,  axis=1), color=colour_solar_credi, label='50%')

# axes['b)'].plot(year_dates,df_SEBi['1996'], color='red', alpha=0.9, linewidth=1)
axes['b)'].plot(year_dates,df_SEBi['1998'], color='green', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_SEBi['2003'], color='purple', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_SEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)


   
# # Add a line through zero
axes['a)'].axhline(y=0.0, color='gray', linestyle='--')
axes['b)'].axhline(y=0.0, color='gray', linestyle='--')

# # add window markers
# axes['a)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes['b)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')





# ## Now fix the nice stuff



# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a in ['a)', 'b)']:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a].xaxis.set_major_formatter(xfmt_years)




# # set the legend and labels
# axes['a)'].legend(loc='lower right', fontsize='medium')
axes['a)'].legend(loc='lower left', fontsize='medium')
axes['b)'].legend(loc='lower left', fontsize='medium')

if REGION == 'NL01':
    LIMITER = 90
    axes['a)'].set_ylim(- LIMITER,LIMITER)
    axes['b)'].set_ylim(- LIMITER,LIMITER)

# # Fix labels
axes['a)'].set_ylabel('Solar CREDI [FLH]')
# axes['b)'].set_ylabel('Solar Energy Balance index')



# # make it look better
plt.tight_layout()


# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')


if REGION == 'NL01':
    plt.savefig(FOLDER_project+'results/publication/SolarCREDI_seasonal-summer.png')
    plt.savefig(FOLDER_project+'results/publication/SolarCREDI_seasonal-summer.pdf')
else:
    plt.savefig(FOLDER_project+'results/additional_regions/SolarCREDI_seasonal-summer_'+REGION+'.png')
    plt.savefig(FOLDER_project+'results/additional_regions/SolarCREDI_seasonal-summer_'+REGION+'.pdf')


plt.show()

#%%
# =============================================================================
# Winter SOLAR
# =============================================================================

# Initialize the dataframe
df_SEBi = pd.DataFrame()


# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    if year == 1991:
        df_SEBi[str(year)] = ds_SPVanom.anom.sel(time=slice(str(year)+'-10-15', str(year+1)+'-03-15')).cumsum().to_numpy()
    else:
        df_SEBi[str(year)] = ds_SPVanom.anom.sel(time=slice(str(year)+'-10-15', str(year+1)+'-03-15')).cumsum().values

# show years
year_dates = pd.date_range('1999-10-15',periods=3648, freq='1h')


# we start a new figure
fig, axes = plt.subplot_mosaic([['a)', 'b)']], figsize=(13,5))
# fig, axes = plt.subplot_mosaic([['a)', 'b)', 'c)']], figsize=(18,5))


# fix date-format
fig.autofmt_xdate()

### First plot the initial yearly energy balance index and additional lines 

# we want to see all years
for year in np.arange(start=1991,stop=2021):
    
    # Show the data for all the years
    axes['a)'].plot(year_dates, df_SEBi[str(year)], color=colour_solar_credi, alpha=0.5, linewidth=1)
    
axes['a)'].plot(year_dates,df_SEBi['1996'], color='red', label='1996', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['1998'], color='green', label='1998', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['2003'], color='purple', label='2003', alpha=0.9, linewidth=1)
axes['a)'].plot(year_dates,df_SEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0,  axis=1),
    df_SEBi.quantile(1,  axis=1),
    color=colour_solar_credi, alpha=0.1, label='min-max'
    )

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0.1,  axis=1),
    df_SEBi.quantile(0.9,  axis=1),
    color=colour_solar_credi, alpha=0.2, label='10-90%'
    )

axes['b)'].fill_between(
    year_dates, 
    df_SEBi.quantile(0.25,  axis=1),
    df_SEBi.quantile(0.75,  axis=1),
    color=colour_solar_credi, alpha=0.4, label='25-75%'
    )

axes['b)'].plot(year_dates,df_SEBi.quantile(0.5,  axis=1), color=colour_solar_credi, label='50%')

# axes['b)'].plot(year_dates,df_SEBi['1996'], color='red', alpha=0.9, linewidth=1)
axes['b)'].plot(year_dates,df_SEBi['1998'], color='green', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_SEBi['2003'], color='purple', alpha=0.9, linewidth=1)
# axes['b)'].plot(year_dates,df_SEBi['2016'], color='black', label='2016', alpha=0.9, linewidth=1)


   
# # Add a line through zero
axes['a)'].axhline(y=0.0, color='gray', linestyle='--')
axes['b)'].axhline(y=0.0, color='gray', linestyle='--')

# # add window markers
# axes['a)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=0, ymax=900, color='gray', alpha=0.6, linestyle='-.',  label='Climatology period')
# axes['b)'].vlines(x=['1991-01-01', '2020-12-31'], ymin=-250, ymax=0, color='gray', alpha=0.6, linestyle='-.', label='Climatology period')





# ## Now fix the nice stuff



# formate the date-axis 
xfmt_years = mdates.DateFormatter('%b')
for a in ['a)', 'b)']:
    axes[a].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axes[a].xaxis.set_minor_locator(mdates.MonthLocator())
    axes[a].xaxis.set_major_formatter(xfmt_years)




# # set the legend and labels
# axes['a)'].legend(loc='lower right', fontsize='medium')
axes['a)'].legend(loc='lower left', fontsize='medium')
axes['b)'].legend(loc='lower left', fontsize='medium')

if REGION == 'NL01':
    LIMITER = 30
    axes['a)'].set_ylim(- LIMITER,LIMITER)
    axes['b)'].set_ylim(- LIMITER,LIMITER)

# # Fix labels
axes['a)'].set_ylabel('Solar CREDI [FLH]')
# axes['b)'].set_ylabel('Solar Energy Balance index')



# # make it look better
plt.tight_layout()


# print subplot names
for label, ax in axes.items():
    # label physical distance in and down:
    trans = mtransforms.ScaledTranslation(10/72, -8/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='xx-large', verticalalignment='top')


if REGION == 'NL01':
    plt.savefig(FOLDER_project+'results/publication/SolarCREDI_seasonal-winter.png')
    plt.savefig(FOLDER_project+'results/publication/SolarCREDI_seasonal-winter.pdf')
else:
    plt.savefig(FOLDER_project+'results/additional_regions/SolarCREDI_seasonal-winter_'+REGION+'.png')
    plt.savefig(FOLDER_project+'results/additional_regions/SolarCREDI_seasonal-winter_'+REGION+'.pdf')



plt.show()

