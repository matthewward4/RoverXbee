from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import argparse


parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
parser.add_argument('--destinationLat')
parser.add_argument('--destinationLong')
args = parser.parse_args()

connection_string = args.connect

lat = float(args.destinationLat)
long = float(args.destinationLong)

#-- Connect to the vehicle
print("Connection to the vehicle on %s"%connection_string)
vehicle = connect(connection_string, wait_ready=True)

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
    
    #-- wait to reach the target altitude
    while True:
        altitude = vehicle.location.global_relative_frame.alt
        
        if altitude >= tgt_altitude -1:
            print("Altitude reached")
            break
            
        time.sleep(1)

def get_lat():
    newLat = 30.6248993
    print("New Latitude: ", newLat)
    return newLat

def get_long():
    newLong = -96.3468213
    print("New Longitude: ", newLong)
    return newLong
        
#------ MAIN PROGRAM ----
arm_and_takeoff(10)

#-- set default speed
vehicle.groundspeed = 5

#vehicle.home_location = LocationGlobal(30.623203, -96.344868, 0)
print("Setting Launch Location to Current Coordinates")
vehicle.home_location = vehicle.location.global_frame

time.sleep(10)
at_destination = 0
i = 0
while i < 5:
    i = i + 1
    obstacle = 0
    if i % 4 == 0:
        at_destination = 1
        
    if at_destination:
        print("Arrived at Destination")
        continue

    #-- Go to wp
    wp1 = LocationGlobalRelative(get_lat(), get_long(), 10)
    print(wp1)
    print(vehicle.location.global_relative_frame)
    print("Go to")
    vehicle.simple_goto(wp1)
    if wp1 == vehicle.location.global_relative_frame:
        continue
    else:
        time.sleep(30)

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



