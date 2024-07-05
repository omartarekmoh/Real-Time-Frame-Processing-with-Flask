from gps3 import gps3

# Create a GPS instance
gps_connection = gps3.GPSDSocket()

try:
    # Open GPS connection
    gps_connection.connect()

    # Enable GPS streaming
    gps_connection.watch()

    for new_data in gps_connection:
        if new_data:
            latitude = new_data['lat']
            longitude = new_data['lon']
            print("GPS Coordinates:", latitude, longitude)

            # Generate Google Maps URL or perform other actions with accurate location data

except Exception as e:
    print("Error occurred:", e)
finally:
    gps_connection.close()
