from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import argparse


parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
parser.add_argument('--destinationLat')
parser.add_argument('--destinationLong')
args = parser.parse_args()

#connection_string = args.connect
connection_string = "/dev/ttyAMA0"


#lat = float(args.destinationLat)
#long = float(args.destinationLong)
lat = 30.6235
long = -96.4


#-- Connect to the vehicle
print("Connection to the vehicle on %s"%connection_string)
vehicle = connect(connection_string, baud=57600, wait_ready=True)

#-- Define the function for takeoff
def arm_and_takeoff(tgt_altitude):
    print("Arming motors")
    
    while not vehicle.is_armable:
        time.sleep(1)
        
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    print("Bot in Guided Mode")
    
    while not vehicle.armed: time.sleep(1)
    
    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)
""" 
    #-- wait to reach the target altitude
    while True:
        altitude = vehicle.location.global_relative_frame.alt
        
        if altitude >= tgt_altitude -1:
            print("Altitude reached")
            break
            
        time.sleep(1)
"""
def get_lat():
    print("Getting new lat for obstacle")
    x = vehicle.location.global_frame.lat
    newLat = x + 0.0004
    print("New Latitude: ", newLat)
    return newLat

def get_long():
    print("Getting new long for obstacle")
    x = vehicle.location.global_frame.lon
    newLong = x + 0.00004
    print("New Longitude: ", newLong)
    return newLong
        
#------ MAIN PROGRAM ----
arm_and_takeoff(10)

#-- set default speed
vehicle.groundspeed = 5

#vehicle.home_location = LocationGlobal(30.623203, -96.344868, 0)
print("Setting Launch Location to Current Coordinates")
vehicle.home_location = vehicle.location.global_frame

print('Going to Coordinates: ', lat, long)
#lat = 30.6238081
#long = -96.3452455
at_destination = 0
i = 0
while i < 20:
    i = i + 1
    obstacle = 0
    if i % 19 == 0:
        at_destination = 1
    if i % 4 == 0:
        print("***Obstacle Detected***")
        obstacle = 1
        
    if at_destination:
        print("Arrived at Destination")
        continue

    #-- Go to wp
    wp1 = LocationGlobalRelative(lat, long, 10)
    #wp2 = LocationGlobalRelative(30.6235084, -96.3452459, 10)

    if obstacle:
        print("---Making Avoidance measures---")
        newLat = get_lat()
        newLong = get_long()
        wp1 = LocationGlobalRelative(newLat, newLong, 10)

    print("Go to")
    vehicle.simple_goto(wp1)
    time.sleep(4)
    if obstacle:
        time.sleep(10)

print("Global Location: %s" % vehicle.location.global_frame)
print("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print("Local Location: %s" % vehicle.location.local_frame)
print("Heading: ", vehicle.heading)
print("GPS INFO: ", vehicle.gps_0)

#--- Coming back
print("Coming back")
vehicle.mode = VehicleMode("RTL")

time.sleep(10)

#-- Close connection
vehicle.close()



