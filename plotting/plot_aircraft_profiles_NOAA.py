'''
Code to load and plot aircraft profiles of carbon monoxide
collated and harmonized for MOPITT v10 validation

--- rrb 2026-05-13
'''


#library
import glob # for listing files
import pandas as pd
import matplotlib.pyplot as plt
import sys  # for sys.exit()


# ========================================================================
# user definitions
# ========================================================================

# path setup
#--- all data (https://doi.org/10.5281/zenodo.20147785)
noaa_folder = '/home/buchholz/MOPITTv10/MOPITT_Validation/aircraft_profile_CO_data/NOAA/'
noaa_files = sorted(glob.glob(noaa_folder+"/*/*.asc"))

# plot definitions
profile_plot_name = '../images/noaa_all_profile.png'
plot_color = 'royalblue'
plot_title = 'Average aircraft profiles of CO from NOAA'

# ========================================================================
# functions
# ========================================================================

def get_location_name(datafile):
    '''
    Function to define a unique location name with station or campaign name,
    combined with UTC date and time ID-YYYY-MM-DD-HHMM
    
    datafile (str): string path to file containing data
  
    returns: location_ID (str) is a string unique to the profile file being used
    
    '''

    filename = pd.read_csv(datafile, header=None, nrows=1)

    location_meta_temp = filename.iloc[0].str.split('_')
    location_meta_temp_2 = location_meta_temp.str[-1].str.split('.')
    location_date_UTC = location_meta_temp_2.str[0]
    location_time_UTC = location_meta_temp_2.str[1]

    location_meta_temp_3 = filename.iloc[0].str.split('/')
    location_name = location_meta_temp_3.str[14]

    concat_info = location_name+'-'+location_date_UTC+'-'+location_time_UTC
    location_ID = str(concat_info.values[0])

    return location_ID


def load_profiles(datafile):
    
    '''
    Function that collects aircraft profiles from harmonized interpolated
    files and joins into a pandas dataframe
    
    datafile (str): string path to file containing data
    
    returns: aircraft_array (float) is a data array of CO values
    in a format to join to a pandas DataFrame
    
    '''
    location_ID = get_location_name(datafile)
    aircraft_array = pd.read_csv(datafile, header=4, sep='\s+', index_col=0)
    aircraft_array.columns = [location_ID]

    return aircraft_array


def load_meta(datafile):
    
    '''
    Function that collects meta data associated with aircraft profiles
    from harmonized interpolated files and joins into a pandas dataframe
    
    datafile (str): string path to file containing data
    
    returns: aircraft_meta_array (str) is an array of location information
    values in a format to join to a pandas DataFrame
    
    '''

    location_ID = get_location_name(datafile)
    location_meta = pd.read_csv(datafile, header=None, skiprows=1, nrows=1, sep='\s+')
    aircraft_meta_array = pd.DataFrame(columns=[location_ID])
    # truncate lat/lon to 1 decimal place for compressing location info
    aircraft_meta_array.loc['lat'] = location_meta.iloc[0,0]
    aircraft_meta_array.loc['lon'] = location_meta.iloc[0,1]
    aircraft_meta_array.loc['presmax'] = location_meta.iloc[0,2]
    aircraft_meta_array.loc['presmin'] = location_meta.iloc[0,3]
    aircraft_meta_array.loc['N'] = location_meta.iloc[0,4]

    return aircraft_meta_array


def profile_plot(x,y,color_choice,label_string,linewidth,marker):
    plt.plot(x, y, marker, label=label_string,
         color=color_choice,
         markersize=8, linewidth=linewidth,
         markerfacecolor=color_choice,
         markeredgecolor='grey',
         markeredgewidth=1)

# ========================================================================
# load files
# ========================================================================

count = 0

#for file in noaa_files[0:5]:
for file in noaa_files:
    profile_ID = get_location_name(file)

    if count == 0:
        print('collecting first aircraft profile record: '+profile_ID)
        aircraft_full_array = load_profiles(file)
        aircraft_full_meta = load_meta(file)
        count += 1
    else:
        print('collecting aircraft profile: '+profile_ID)
        temp = aircraft_full_array
        newdata = load_profiles(file)

        temp2 = aircraft_full_meta
        newdata2 = load_meta(file)

        aircraft_full_array = pd.concat([temp, newdata], axis=1)
        aircraft_full_meta = pd.concat([temp2, newdata2], axis=1)

#DEBUG
print('**************')
print(aircraft_full_array)
print(aircraft_full_meta)

# ========================================================================
# save out location file
# ========================================================================
location_temp =  aircraft_full_meta.transpose()
sitename_temp = aircraft_full_meta.columns.str.split('-')
location_temp['sitename'] = sitename_temp.str[0]
location_info = location_temp.groupby(['sitename'], as_index=False).mean()
print(location_info)

# write the csv
location_info.to_csv('NOAA_locations.csv', index=False, float_format='%.2f')

# ========================================================================
# calculate average profile and standard deviation
# ========================================================================
aircraft_mean = aircraft_full_array.mean(axis=1)
aircraft_sd = aircraft_full_array.std(axis=1)
num_prof = aircraft_full_array.shape[1]

# ========================================================================
# plot profile
# ========================================================================

plt.figure(figsize=(7,10))
ax = plt.axes()
ax.invert_yaxis()

#------------| variable |------| pressure |---------
profile_plot(aircraft_mean, aircraft_mean.index, plot_color,'Mean CO', 4,'-ok')
ax.fill_betweenx(aircraft_mean.index, aircraft_mean - aircraft_sd, aircraft_mean + aircraft_sd, color=plot_color, alpha=0.2, label='1 SD')


#titles
plt.title(plot_title,fontsize=16)        
plt.xlabel('CO VMR (ppb)',fontsize=14)
plt.ylabel('Pressure (hPa)',fontsize=14)
ax.tick_params(axis='both', labelsize=14) 

# legend
plt.legend(bbox_to_anchor=(0.98, 0.88),loc='lower right',fontsize=14)

# extra information
plt.text(0.72, 0.85, "N: "+str(num_prof),fontsize=14, transform=plt.gca().transAxes)

# background grid
ax.yaxis.grid(color='lightgray', linestyle='dashed', linewidth=1)
ax.xaxis.grid(color='lightgray', linestyle='dashed', linewidth=1)

plt.savefig(profile_plot_name)
plt.show()



