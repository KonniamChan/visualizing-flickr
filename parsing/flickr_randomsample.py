from __future__ import division
import sys
import numpy as np

# Cities to filter out
# {City: [min latitude, min longitude, max latitude, max longitude]}
cities = {"San Francisco": {"coordinates": [37.699342, -122.561829, 37.866062, -122.280451], "file": "sf.csv"},
         "New York": {"coordinates": [40.667300, -74.092467, 40.823483, -73.880939], "file": "ny.csv"},
         "Paris": {"coordinates": [48.788798, 2.189496, 48.936948, 2.473834], "file": "paris.csv"},
         "Hong Kong": {"coordinates": [22.175548, 114.050751, 22.379670, 114.280063], "file": "hk.csv"}}
camera_makers = ["CANON", "NIKON", "APPLE", "SONY", "PANASONIC"]
dir, input, factor = sys.argv[1], sys.argv[2], int(sys.argv[3])
np.random.seed(0)

# Filtering
def geo_filter(dir, input, factor):
    '''
    Takes path of directory, input file, and sampling factor as arguments. Output csv files of cities.
    '''
    in_file = open(dir + "/" + input, "r")
    out_files = {}
    
    # Write header
    for city in cities:
        out_files[city] = open(dir + "/" + cities[city]["file"], "a")
        out_files[city].write("identifier,nsid,user,year,camera,title,longitude,latitude,url,license\n")
    
    for line in in_file:
        # Sample (1/factor) of lines
        if np.random.uniform() > (1 / factor): continue

        array = line.strip().split("\t")
        
        # User
        user = array[2].replace("+", " ")
        
        # Year
        year = array[3][:4]
        
        # Device
        camera_array = array[5]
        camera_index = camera_array.find("+")
        camera = camera_array[:camera_index].upper() if camera_index != -1 else "NA"
        
        # Title
        title = array[6].replace("+", " ")
            
        # Longitude and latitude
        longitude = float(array[10]) if array[10] else 9999
        latitude = float(array[11]) if array[11] else 9999
        
        # License
        lic_url = array[16]
        lic_url = lic_url[lic_url.find("by"):].split("/")        
        license = lic_url[0]

        output_line = array[0] + "," + array[1] + "," + user + "," + year + "," + camera + "," + title + "," + array[10] + "," + array [11] + "," +  array[14] + "," + license + "\n"
        
        # Filter and write
        for city in cities:
	        if (latitude > cities[city]["coordinates"][0] and longitude > cities[city]["coordinates"][1] and 
	            latitude < cities[city]["coordinates"][2] and longitude < cities[city]["coordinates"][3] and array[22]=="0" and
	           camera in camera_makers):
	            out_files[city].write(output_line)

geo_filter(dir, input, factor)