# Student ID: 011247597

import Package
import Truck
import HashTable
from datetime import timedelta
import csv

# Initialize Hash Table
package_table = HashTable.HashTable()

# Initialize Trucks
truck1 = Truck.Truck(1, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
                     0.0, timedelta(hours=8), timedelta(hours=8))

truck2 = Truck.Truck(2, [3, 6, 18, 25, 28, 32, 33, 35, 36, 38, 39],
                     0.0, timedelta(hours=9, minutes=30), timedelta(hours=9, minutes=30))

truck3 = Truck.Truck(3, [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27],
                     0.0, timedelta(hours=11), timedelta(hours=11))

# Create distance matrix to hold distances
distance_matrix = []

# Read distances into distance matrix
with open("distance_data.csv", 'r', encoding='utf-8-sig') as file:
    csvreader = csv.reader(file)
    for line in csvreader:
        distance_matrix.append(line)

# Read package data
with open('package_data.csv', 'r', encoding='utf-8-sig') as file:
    for line in file:
        # Split the line based on commas
        data = line.strip().split(',')
        # Create a Package object using the data
        package = Package.Package(
            id=int(data[0]),
            address=data[1],
            deadline=data[5],
            city=data[2],
            state=data[3],
            zip=data[4],
            weight=data[6],
            status="At Hub",
            delivery_time=None
        )
        # Insert the package into the hash table based on package ID
        package_table.insert(package)

# Function to convert csv file into list
def read_address_data():
    with open("address_data.csv", "r", encoding="utf-8-sig") as file:
        address_reader = csv.reader(file)
        return list(address_reader)

# Function to find the address ID of a given address
def get_address_id(address_data, address):
    for line in address_data:
        if address == line[2]:
            return int(line[0])
    return None

# Function to find the difference in miles between the truck's location and package's delivery address
def calculate_distance(truck_address_id, package_address_id, distance_matrix):
    distance = distance_matrix[truck_address_id][package_address_id]
    if distance:
        return float(distance)
    else:
        return float(distance_matrix[package_address_id][truck_address_id])

# Function to get the package with the closest address to the truck's current location
def find_closest_package(undelivered, truck, address_data, distance_matrix):
    # Initially, closest distance is infinity and there is no package chosen
    current_package = None
    closest_distance = float("inf")
    truck.address_id = get_address_id(address_data, truck.address)
    # To find the closest address, have to compare all distances to current location
    for package in undelivered:
        package.address_id = get_address_id(address_data, package.address)
        distance = calculate_distance(truck.address_id, package.address_id, distance_matrix)
        # If the distance found is closer than the current closest, update closest distance
        if distance <= closest_distance:
            current_package = package
            closest_distance = distance
    return current_package, closest_distance

def deliver_packages(truck, distance_matrix, package_table):

    # Add the truck packages to a list to keep track of which still need to be delivered
    undelivered = []
    for id in truck.packages:
        package = package_table.lookup(id)
        # Package 9 has the wrong address which is not updated until 10:20 AM
        if package.id == 9 and truck.time_now >= timedelta(hours=10, minutes=20):
            package.address = "410 S State St"
            package.zip = "84111"
            package.address_id = 19
        undelivered.append(package)

    # Find the truck's current address ID
    address_data = read_address_data()
    truck.address_id = get_address_id(address_data, truck.address)

    # Update the status of all packages on the truck
    for package in undelivered:
        package.status = "En Route"
        package.enroute_time = truck.time_now

    # Package 15 is on truck 1
    if truck.id == 2 or truck.id == 3:
        fifteen_delivered = True
    else:
        fifteen_delivered = False
    # Deliver packages until all are delivered
    while undelivered:
        # This is the code that will execute for the 39 other packages
        if fifteen_delivered:
            current_package, closest_distance = find_closest_package(undelivered, truck, address_data, distance_matrix)
        # Check to see if package 15 is on truck and/or is undelivered
        # Deliver package 15 first because it has 9 AM deadline
        else:
            for package in undelivered:
                if package.id == 15:
                    current_package = package_table.lookup(15)
                    closest_distance = calculate_distance(truck.address_id, get_address_id(address_data, current_package.address), distance_matrix)

        # After figuring out the package to deliver and distance to travel, actually deliver the package

        # Update the truck's milage, current location, and current time
        truck.address = current_package.address
        truck.address_id = get_address_id(address_data, truck.address)
        truck.mileage += closest_distance
        # Truck travels at 18 MPH
        truck.time_now += timedelta(hours=closest_distance / 18.0)

        # Update the package with delivery information
        current_package.delivery_time = truck.time_now
        current_package.status = "Delivered"
        undelivered.remove(current_package)

        # If the current package delivered was 15, update the Boolean
        if current_package.id == 15:
            fifteen_delivered = True

# Create list of trucks
trucks = [truck1, truck2, truck3]

print("Trucks:")
# Loop through trucks to deliver packages and associate each package with a truck ID
for truck in trucks:
    deliver_packages(truck, distance_matrix, package_table)
    print(truck)
    for id in truck.packages:
        package = package_table.lookup(id)
        package.truck = truck.id

print(f"Total mileage driven by all 3 trucks: {truck1.mileage + truck2.mileage + truck3.mileage}")
print()

print("This is WGU's package delivery service")
# Forever loop
while True:
    print("To begin the User Interface, type 'begin': ")
    print("To end the forever loop, type 'end': ")
    word = input().lower().strip()
    if word == "begin":
        # Ask user if they want to view every package or just one
        word = input("Type 'all' to view all packages or 'individual' to view a single package: ").lower().strip()
        if word == "all":
            # Get the time the user wants to check on
            time = input("Type the time you want to check. Use the 'HH:MM' format: ").lower().strip()
            if ":" in time:
                time = time.split(":")
                hours = int(time[0])
                minutes = int(time[1])
                time = timedelta(hours=hours, minutes=minutes)
                # Loop through and print all packages, accessing hash table
                for id in range (1,41):
                    package = package_table.lookup(id)
                    # Handle package 9 not having correct address until 10:20 AM
                    if package.id == 9 and time < timedelta(hours=10, minutes=20):
                        package.address = "300 State St"
                        package.zip = "84103"
                    # Else the time is greater than or equal to 10:20, so use correct address
                    elif package.id == 9:
                        package.address = "410 S State St"
                        package.zip = "84111"
                    package.current_status(time)
                    print(package)
                continue
            elif time == "end":
                break
            else:
                print("Invalid input, restarting loop...")
                continue
        elif word == "individual":
            # Get the time the user wants to check on
            time = input("Type the time you want to check. Use the 'HH:MM' format: ").lower().strip()
            if ":" in time:
                time = time.split(":")
                hours = int(time[0])
                minutes = int(time[1])
                time = timedelta(hours=hours, minutes=minutes)
                # Get the ID of the package the user wants to see
                id = input("Type the package ID: ")
                if id == "end":
                    break
                # Access hash table to get and print package
                package = package_table.lookup(int(id))
                # Handle package 9 not having correct address until 10:20 AM
                if package.id == 9 and time < timedelta(hours=10, minutes=20):
                    package.address = "300 State St"
                    package.zip = "84103"
                # Else the time is greater than or equal to 10:20, so use correct address
                elif package.id == 9:
                    package.address = "410 S State St"
                    package.zip = "84111"
                package.current_status(time)
                print(package)
                continue
            elif time == "end":
                break
            else:
                print("Invalid input, restarting loop...")
                continue
        elif word == "end":
            break
        else:
            print("Invalid input, restarting loop...")
            continue
    elif word == "end":
        break
    else:
        print("Invalid input, restarting loop...")
        continue
