'''
Code to load and compare aircraft profiles of carbon monoxide
collated and harmonized for validation against MOPITT v10
retrievals of CO.

  Filter definitons:
  - aircraft profile must start below 750 hPa (850 hPa for NOAA sites sgp, lef, esp, or 700 hPa for NOAA rta), and the profile must end higher than 450 hPa (500 hPa for NOAA rta, 550 hPa for NOAA sgp, lef, esp). Additionally, the aircraft profiles must contain 5 or more flask measurements.
  - MOPITT retrievals must be within a 50 km radius for NOAA locations, (200 km radius for HIPPO and ATom), and MOPITT retrieval time must be within +/- 12 hrs of the observation. Finally, there must be 5 or more MOPITT profiles per aircraft profile.

  To use on mopfl2012:
  > python3.12 pair_mopitt_noaa_v10.py

  Steps in process:
  #--- load aircraft files
  #--- aircraft filters
  #--- load coincident MOPITT file
  #--- MOPITT spatiotemporal filters
  #--- adjust to 10 layers
  #--- use MERRA2 water vapor

--- rrb 2026-05-29
'''


#library
import glob # for listing files
import pandas as pd
import sys  # for sys.exit()


# ========================================================================
# user definitions
# ========================================================================

# NOAA file location
#--- all data (https://doi.org/10.5281/zenodo.20147785)
noaa_folder = '/home/buchholz/MOPITTv10/MOPITT_Validation/mopittv10_python/sample_data/NOAA/'
#noaa_folder = '/home/buchholz/MOPITTv10/MOPITT_Validation/aircraft_profile_CO_data/NOAA/'
aircraft_files = sorted(glob.glob(noaa_folder+"/*/*.asc"))

# MOPITTv10 file location
#mopitt_folder = '/MOPITT/V10T/Archive/L2/'

# MERRA2 file location
#mopitt_folder = '/MOPITT/project/datasets/merra2-nc4/Rebecca/3D/'

# Outfile name template
location_csv_name = '/home/buchholz/MOPITTv10/MOPITT_Validation/mopittv10_python/validation/validation_pairing/val_L2_v10.L2V19.9.2.'

# Filter thresholds
# Number of aircraft measurements averaged
nflaskmin = 5.
# Aircraft profile extent
p_top_thr = 450.
p_bot_thr = 750.
# Coarse MOPITT spatial range acceptance
dlatmax = 2.5
dlonmax = 2.5
# Fine MOPITT spatiotemporal range acceptance
distmax = 50.
dthrsmax = 12.

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
    aircraft_array = pd.read_csv(datafile, header=4, sep='\\s+', index_col=0)
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
    location_meta = pd.read_csv(datafile, header=None, skiprows=1, nrows=1, sep='\\s+')
    aircraft_meta_array = pd.DataFrame(columns=[location_ID])
    location_meta_temp = location_ID.iloc[0].str.split('-')
    #aircraft_meta_array.loc['DD'] = location_meta.iloc[0,0]
    #aircraft_meta_array.loc['MM'] = location_meta.iloc[0,0]
    #aircraft_meta_array.loc['YYYY'] = location_meta.iloc[0,0]
    aircraft_meta_array.loc['HHSS'] = location_meta.iloc[0,0]
    aircraft_meta_array.loc['lat'] = location_meta.iloc[0,0]
    aircraft_meta_array.loc['lon'] = location_meta.iloc[0,1]
    #correct for longitude values > 180.
    if (aircraft_meta_array.loc['lon'].values > 180.):
        aircraft_meta_array.loc['lon'] = aircraft_meta_array.loc['lon'] - 360.
    aircraft_meta_array.loc['presmax'] = location_meta.iloc[0,2]
    aircraft_meta_array.loc['presmin'] = location_meta.iloc[0,3]
    aircraft_meta_array.loc['N'] = location_meta.iloc[0,4]
    aircraft_meta_array.loc['fname'] = datafile

    return aircraft_meta_array


# ========================================================================
# process the comparison
# ========================================================================
#--- load aircraft files

count = 0

for file in aircraft_files[0:5]:
#for file in aircraft_files:
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


#--- aircraft filters




#--- load coincident MOPITT file




#--- MOPITT spatiotemporal filters




#--- adjust to 10 layers




#--- use MERRA2 water vapor



# ========================================================================
# write out file
# ========================================================================



