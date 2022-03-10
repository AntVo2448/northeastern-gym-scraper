"""
Scrape data from Northeastern's gym data visualizer.
"""

# Generate requirements.txt with:  pipreqs . --force
from bs4 import BeautifulSoup
from psycopg2 import Error

import urllib.parse as urlparse
from datetime import datetime
# import pprint as pp
import requests
import psycopg2
import os



"""
   _____ ______ _______    _____       _______       
  / ____|  ____|__   __|  |  __ \   /\|__   __|/\    
 | |  __| |__     | |     | |  | | /  \  | |  /  \   
 | | |_ |  __|    | |     | |  | |/ /\ \ | | / /\ \  
 | |__| | |____   | |     | |__| / ____ \| |/ ____ \ 
  \_____|______|  |_|     |_____/_/    \_\_/_/    \_\
"""

# Using this header so the website doesn't think we're a bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}
# URL of the target site with data
url = "https://connect2concepts.com/connect2/?type=circle&key=2A2BE0D8-DF10-4A48-BEDD-B3BC0CD628E7"

# Send GET request to site to get HTML data
soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")



"""
  _____        _____   _____ ______    _____       _______       
 |  __ \ /\   |  __ \ / ____|  ____|  |  __ \   /\|__   __|/\    
 | |__) /  \  | |__) | (___ | |__     | |  | | /  \  | |  /  \   
 |  ___/ /\ \ |  _  / \___ \|  __|    | |  | |/ /\ \ | | / /\ \  
 | |  / ____ \| | \ \ ____) | |____   | |__| / ____ \| |/ ____ \ 
 |_| /_/    \_\_|  \_\_____/|______|  |_____/_/    \_\_/_/    \_\
"""

# Get a list of the names of the buildings
location_name_list = soup.find_all("div", {"style": "text-align:center;"})

# Get a list of all classes used to create a "circleChart" (contains percentages)
percent_list = soup.find_all("div", {"class": "circleChart"})

# Get a list of wherever "Last Count" appears in text (contains raw number)
count_list = soup.find_all(text=lambda x: x and "Last Count:" in x)

# Get a list of wherever "Updated" appears in text (contains raw number)
last_updated_list = soup.find_all(text=lambda x: x and "Updated:" in x)



"""
   _____ _______ ____  _____  ______    _____       _______       
  / ____|__   __/ __ \|  __ \|  ____|  |  __ \   /\|__   __|/\    
 | (___    | | | |  | | |__) | |__     | |  | | /  \  | |  /  \   
  \___ \   | | | |  | |  _  /|  __|    | |  | |/ /\ \ | | / /\ \  
  ____) |  | | | |__| | | \ \| |____   | |__| / ____ \| |/ ____ \ 
 |_____/   |_|  \____/|_|  \_\______|  |_____/_/    \_\_/_/    \_\
"""

# Convert data into list
# [Location Name, Last Updated, Last Count, Percentage]
# (Marino 2nd floor, Marino Gymnasium, Marino 3rd floor weights, Marino 3rd floor cardio, Marino track, Squashbusters 4th floor)

results = []

# Each list should be the same length
for index in range(len(location_name_list)):
  # Get the location name
  location_name = location_name_list[index].text[:location_name_list[index].text.find('(')]

  # Get the time the entry was last updated (converted to a datetime object)
  date_string = last_updated_list[index].split('Updated:')[1].strip()
  last_updated = datetime.strptime(date_string, '%m/%d/%Y %I:%M %p')

  # Get the last count reported
  last_count = count_list[index].split(':')[-1].strip()

  # Get the last percentage reported
  percentage = percent_list[index].get('data-percent')

  # Add data to results
  results.append([location_name, last_updated, last_count, percentage])

# print(results)



"""
  _    _ _____  _      ____          _____     _____       _______       
 | |  | |  __ \| |    / __ \   /\   |  __ \   |  __ \   /\|__   __|/\    
 | |  | | |__) | |   | |  | | /  \  | |  | |  | |  | | /  \  | |  /  \   
 | |  | |  ___/| |   | |  | |/ /\ \ | |  | |  | |  | |/ /\ \ | | / /\ \  
 | |__| | |    | |___| |__| / ____ \| |__| |  | |__| / ____ \| |/ ____ \ 
  \____/|_|    |______\____/_/    \_\_____/   |_____/_/    \_\_/_/    \_\
"""

# sql_marino_2nd_floor = f"INSERT INTO \"Marino Center - 2nd Floor\" (test) VALUES ({results[0][3]}, {results[0][2]}, {results[0][1]})"
# sql_marino_2nd_floor = "INSERT INTO \"Marino Center - 2nd Floor\" VALUES (%s, %s, '%s')" % (results[0][3], results[0][2], results[0][1])
# sql_marino_2nd_floor = """
# INSERT INTO "Marino Center - 2nd Floor" VALUES (50, 50, current_date)
# """

# SQL Queries to commit
sql_marino_2nd_floor   = f"INSERT INTO \"Marino Center - 2nd Floor\" VALUES ({results[0][3]}, {results[0][2]}, '{results[0][1]}')"
sql_marino_gymnasium   = f"INSERT INTO \"Marino Center - Gymnasium\" VALUES ({results[1][3]}, {results[1][2]}, '{results[1][1]}')"
sql_marino_3rd_weights = f"INSERT INTO \"Marino Center - 3rd Floor Weight Room\" VALUES ({results[2][3]}, {results[2][2]}, '{results[2][1]}')"
sql_marino_3rd_cardio  = f"INSERT INTO \"Marino Center - 3rd Floor Select & Cardio\" VALUES ({results[3][3]}, {results[3][2]}, '{results[3][1]}')"
sql_marino_track       = f"INSERT INTO \"Marino Center - Track\" VALUES ({results[4][3]}, {results[4][2]}, '{results[4][1]}')"
sql_squashbusters_4th  = f"INSERT INTO \"SquashBusters - 4th Floor\" VALUES ({results[5][3]}, {results[5][2]}, '{results[5][1]}')"

sql_queries = [
  sql_marino_2nd_floor, 
  sql_marino_gymnasium, 
  sql_marino_3rd_weights, 
  sql_marino_3rd_cardio, 
  sql_marino_track, 
  sql_squashbusters_4th
]

# Attempt to insert these queries
try:
    # Get secrets from Heroku environment variables
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    # Connect to an existing database (Heroku)
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=dbname)
    # Automatically commit the changes
    connection.autocommit = True

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    # print("PostgreSQL server information")
    # print(connection.get_dsn_parameters(), "\n")

    # Execute Queries
    for query in sql_queries:
      try:
        cursor.execute(query)
        print(cursor.query)
      except (Exception, Error) as error:
          print('\n')
          print("Query Error:\n", error)

except (Exception, Error) as error:
    print('\n')
    print("Connection Error:\n", error)
    pass
finally:
    if (connection):
        cursor.close()
        connection.close()
        print('\n')
        print("PostgreSQL connection is closed.")


# NOTES:
# Potential Caps
# Marino Center - Gynmasium (60 people b/c 48 is 80%)
# Marino Center - 3rd Floor (90 people b/c 33.3% is 30)
# Marino Center - Track (20 people b/c 5 is 25%)