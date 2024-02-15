import shutil
import os
import sqlite3

from global_config import (
    GLOBALLY_CONFIGURED_FILEPATH,
)
from utils import (
    construct_history_copied_full_file_path,
)

HISTORY_SNAPSHOT_DESTINATION = construct_history_copied_full_file_path(GLOBALLY_CONFIGURED_FILEPATH)
CHROME_HISTORY_DESTINATION = 'C:\\Users\\BudoB\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'

# Delete or overwrite the copied history file
if os.path.exists(HISTORY_SNAPSHOT_DESTINATION):
    os.remove(HISTORY_SNAPSHOT_DESTINATION)

# Make a copy of the current Google Chrome browsing history
# Making a copy of the browsing history because the original file is "locked" while chrome is running
shutil.copy(CHROME_HISTORY_DESTINATION, HISTORY_SNAPSHOT_DESTINATION)


# Connect to the Chrome History database
conn = sqlite3.connect(HISTORY_SNAPSHOT_DESTINATION)
#conn = sqlite3.connect(CHROME_HISTORY_DESTINATION)
cursor = conn.cursor()
# Query to retrieve the URL of the latest YouTube video within the last 100 visited URLs
query = """
    SELECT urls.url, urls.title, urls.last_visit_time
    FROM urls
    INNER JOIN visits ON urls.id = visits.url
    WHERE urls.url LIKE 'https://www.youtube.com/watch?v=%'
    ORDER BY visits.visit_time DESC
    LIMIT 1000
"""

# Execute the query
cursor.execute(query)

# Fetch the result
result = cursor.fetchone()

# Close the database connection
conn.close()


# Print the result
if result:
    url, title, last_visit_time = result
    print("URL:", url)
    print("Title:", title)
    print("Last Visit Time (Epoch Nano):", last_visit_time)
else:
    print("No browsing history found.")