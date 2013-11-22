#!/usr/bin/python
from max31855 import MAX31855, MAX31855Error
import sys, os, time, sqlite3

# Open the database. Will create one if it does not already exist
conn = sqlite3.connect(sys.argv[1])
stmt = 'create table if not exists temps (temp text)'
c = conn.cursor()
c.execute(stmt)
conn.commit()

# Pins designated for the MAX31855
cs_pin = 10
clock_pin = 7
data_pin = 8
units = "f"
thermocouple = MAX31855(cs_pin, clock_pin, data_pin, units)

# Go until I say stop
print("Reading from thermocouple...\nPress CTRL-C to stop.")
while(True):
  try:
    temp = thermocouple.get()
    str_temp = str(temp)
    c.execute('INSERT INTO temps VALUES (?)', [str_temp])
    conn.commit()
    print(temp) # Console output is nice
    time.sleep(3) # Get a temp every 3 seconds
  except KeyboardInterrupt:
    thermocouple.cleanup()
    print("\nstopping")
    conn.commit() # Commit any changes
    conn.close() # Get out of here
