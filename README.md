# Automation of Pulling and Exploring Yelp Data
Overview:
The enclosed script allows you to pull data automatically from Yelp's Fusion API and create resulting csv files, data visualizations, and shapefiles. The script is interactive, giving you the ability to name the files, and make decisions about what data you want.

What's Included:
This folder contains an ArcGIS Pro project folder and a python script. All files created by the script will automatically be stored in this project folder. No need to set a file path, the script will do this for you.

System Requirements:
* Internet access
* ArcGIS Pro (2.3+)
* Spyder
* Python3

Required Packages: 
* IPython(should be installed w/ Spyder)
* os
* requests
* pandas
* seaborn
* matplotlib
* arcpy

How To Use:
1) Save project folder to desired location
2) Open your Spyder application (make sure it works with ArcGIS Pro/arcpy)
3) Open the ArcGIS Pro project, final6317.aprx
4) Open the yelp_to_shp.py file in Spyder and run it
5) Follow the prompts in the IPython console in your Spyder application
6) Locate the created files in the project folder
7) Refresh the project folder in ArcGIS Pro and add your created shapefile(s) to the map


Yelp API limitations:
* you cannot exceed 5000 requests per day, the script makes approximately 20 requests each run
* The API will not return more than 1000 businesses per search

Notes:
* If you are running an earlier version than 2.5 of ArcGIS Pro, you might get some errors in the console. These errors should be resolved in 2.5; they do not affect the functionality of the script.
