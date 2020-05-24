"""
Python script that automatically pulls data from Yelp's Fusion API based on 
user inputs and produces specified csv files, data visualizations, and 
ArcGIS shapefiles.

Final Project
GISC 6317
@author: Rita Savill
"""

from IPython import get_ipython
import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import arcpy

# Yelp Fusion API documentation referenced:
# https://www.yelp.com/developers/documentation/v3/business_search

## CONSTANTS
YELP_AUTH = {"Authorization": "Bearer (INSERT API KEY HERE)"}
REQUEST_LIMIT = 50
REQUEST_OFFSET_STEP = 50

## FUNCTIONS

# Returns response for yelp request with specified parameters
def yelp_request(business, location, input_offset):

  request_params = {
    "term": business, 
    "location": location, 
    "limit": REQUEST_LIMIT, 
    "offset": input_offset
  }

  return requests.get('https://api.yelp.com/v3/businesses/search', params=request_params, headers=YELP_AUTH) 

# Clean data
def clean_data(df):
    # Only keep open establishments
    df = df[df['is_closed']==False]
    
    # Drop unnecessary columns from dataframe
    df = df.drop(['id', 'alias', 'image_url', 'is_closed', 'url', 'categories', 
                  'transactions', 'price', 'phone', 'display_phone', 
                  'distance', 'location.address1', 'location.address2', 
                  'location.address3', 'location.display_address'], axis = 1)
    
    # Rename columns
    df = df.rename(columns = {'coordinates.longitude': 'long'})
    df = df.rename(columns = {'coordinates.latitude': 'lat'})
    df = df.rename(columns = {'location.city': 'city'})
    df = df.rename(columns = {'location.zip_code': 'zip_code'})
    df = df.rename(columns = {'location.country': 'country'})
    df = df.rename(columns = {'location.state': 'state'})
    return df

# Visualize data
# seaborn/matplotlib cheat sheet used:
# https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Python_Seaborn_Cheat_Sheet.pdf
def vis_data(df, name, title):
    sns.set()
    sns.countplot("rating", data=df, palette="Blues_d")
    plt.suptitle(title, fontsize=16)
    plt.savefig(name)
    plt.show()
    plt.clf()

# Create csv and shapefile
def point_shp(df):
    # Get current working directory and set as workspace
    arcpy.env.workspace = os.getcwd()
    
    # Allow previous output to be overwritten
    arcpy.env.overwriteOutput = True
    
    # Convert dataframe to csv file
    out_name = input("Name for shapefile? e.g. Starbucks_Dallas ")
    csv_name = out_name + '.csv'
    df.to_csv(csv_name, index = False, header = True)
    
    ## Convert csv file to shapefile
    
    # Set the local variables
    out_shp = out_name + '.shp'
    x_coords = "long"
    y_coords = "lat"

    # Create shapefile
    arcpy.management.XYTableToPoint(csv_name, out_shp, x_coords, y_coords)


## MAIN SCRIPT

request_results = []

# Get user input
input_business = input("Enter a business: ")
input_location = input("Enter a location (e.g. Dallas, TX, US): ")

# Make initial request for businesses
intial_response = yelp_request(input_business, input_location, 0)
json_dict = intial_response.json()
df = pd.json_normalize(json_dict["businesses"])
request_results.append(df)

# Make request for up to 900 results
total = json_dict["total"]
offset = REQUEST_OFFSET_STEP 

while offset <= total and offset < (1000 - REQUEST_OFFSET_STEP): 
  next_response = yelp_request(input_business, input_location, offset)
  json_dict = next_response.json()
  current_df = pd.json_normalize(json_dict["businesses"])
  request_results.append(current_df)

  offset += REQUEST_OFFSET_STEP

# Combine request dataframes into one
df_all = pd.concat(request_results)

# Ask user if they want competitor data included
comp_ask = input("Do you want to keep competitor data? (Y/N) ").upper()

# Check for valid user input
while comp_ask != "Y" and comp_ask != "N":
    print("Invalid input.")
    comp_ask = input("Do you want to keep competitor data? (Y/N) ").upper()


# Filter dataframe to make competitor data frame   
if comp_ask == "Y":
    df_comp = df_all[~df_all["name"].str.lower().str.contains(input_business.lower())]
    df_comp = clean_data(df_comp)
    print(" ")
    print("Names for files containing ONLY competitor data:")
    vis_name_comp = input("File name for ratings plot? e.g. vis1.png ")
    plot_title_comp = input("Title for ratings plot? e.g. Yelp Ratings ")
    vis_data(df_comp, vis_name_comp, plot_title_comp)
    point_shp(df_comp)

# Filter dataframe to remove competitor data
no_comp = df_all[df_all["name"].str.lower().str.contains(input_business.lower())]
no_comp = clean_data(no_comp)
print(" ")
print("Names for files containing NO competitor data:")
vis_name = input("File name for ratings plot? e.g. vis1.png ")
plot_title = input("Title for ratings plot? e.g. Yelp Ratings ")
vis_data(no_comp, vis_name, plot_title)
point_shp(no_comp)


# Reset all variables
# found this code snippet from github user stsievert
# https://gist.github.com/stsievert/8655158355b7155b2dd8
get_ipython().magic('reset -sf')
