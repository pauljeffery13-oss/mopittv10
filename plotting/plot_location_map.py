'''
Code to load and plot aircraft locations

--- rrb 2026-05-22
'''

#library
import glob # for listing files
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs                 # For plotting maps
import cartopy.feature as cfeature         # For plotting maps
import sys  # for sys.exit()

# ========================================================================
# user definitions
# ========================================================================

# file path setup
noaa_location_file = 'NOAA_locations.csv'

# plot definitions
map_plot_name = '../images/aircraft_locations.png'

# ========================================================================
# load data
# ========================================================================

site_def = pd.read_csv(noaa_location_file, header=0, sep=',')
num_obs = site_def.shape[0]


# ========================================================================
# plot data
# ========================================================================

plt.figure(figsize=(20,8))

#Define projection
ax = plt.axes(projection=ccrs.PlateCarree())

# Zoom to a region
#longitude limits in degrees
ax.set_xlim(-179,180)
#latitude limits in degrees
ax.set_ylim(-90,90)

# add coastlines
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)

#add lat lon grids
gl = ax.gridlines(draw_labels=True, color='grey', alpha=0.8, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False

# Titles
# Main
plt.title("Aircraft profile locations",fontsize=18)

# y-axis
ax.text(-0.04, 0.5, 'Latitude', va='bottom', ha='center',
        rotation='vertical', rotation_mode='anchor',
        transform=ax.transAxes, fontsize=14)
# x-axis
ax.text(0.5, -0.08, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize=14)


#add locations in a loop
for i in range(num_obs):
     site_name = str(site_def.loc[i,'sitename']) 
     site_lon = site_def.loc[i,'lon']
     site_lat = site_def.loc[i,'lat']

     #print( 'station = ' + site_name + 
     #       ', lon = ' + str(site_lon) + 
     #       ', lat = ' + str(site_lat))

     plt.plot(site_lon, site_lat, linestyle='none', marker="o", markersize=8, alpha=0.8, c="black", markeredgecolor="red", markeredgewidth=1, transform=ccrs.PlateCarree())
#    plt.text(site_lon + 0.8, site_lat + 0.8, site_name, fontsize=20, horizontalalignment='left', transform=ccrs.PlateCarree())


#add legend


plt.savefig(map_plot_name)
plt.show()

