
# main.py : Main python class for the execution of the program.
# Custom Imports: HashTable.py, package.py, truck.py, colors.py
import datetime
import csv
from HashTable import HashTable
from package import Package
from truck import Truck
from colors import colors

########## Extracting CSV Data and Returning its contents #############

# csvToList(): Takes a CSV file as input and returns its contents as a list


def csvToList(file):
    with open(file) as csvFile:
        data = csv.reader(csvFile)
        data = list(data)
    return data

# extractPackages(): Takes a HashTable and the CSV file with the package contents as input.
# Creates package objects with the CSV file data and places it into the HashTable that's passed as input.


def extractPackages(packageTable, file):
    with open(file) as csvFile:
        csvFile = csv.reader(csvFile)
        csvFile = list(csvFile)
        for package in csvFile:
            id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deadline = package[5]
            weight = package[6]
            status = "AT THE HUB"

            pkg = Package(id, address, city, state,
                          zip, deadline, weight, status)
            packageTable.insert(id, pkg)


# Calls the 'csvToList' function with the specified files and place the returned List into 'distanceData' and 'addressData'
# distanceData: Stores the distances in miles from one address to another
# addressData: Stores the id/index of the addresses, the location name, and address of the possible delivery locations
distanceData = csvToList('wgupsDistances.csv')
addressData = csvToList('addresses.csv')

# addressLocation(): Takes in an address of a package as input.
# Looks for the input address that matches with an address in the 'addressData' list
# Returns: The id/index that matches with the address from the 'addressData' list (if found)


def addressLocation(address):
    for a in addressData:
        if address in a[2]:
            return int(a[0])

# locationFromAddress(): Similar to the 'addressLocation' function
# Finds the address and returns the Location Name
# Mainly used for UI/Display purposes


def locationFromAddress(address):
    for a in addressData:
        if address in a[2]:
            return a[1]

# extractDistance(): Uses the 'addressLocation' function to obtain start/end coordinate indices and returns the distance between two locations in miles
# The if condition is to perform the inverse if required


def extractDistance(start, end):
    startidx = addressLocation(start)
    endidx = addressLocation(end)

    if distanceData[startidx][endidx] == '':
        return float(distanceData[endidx][startidx])

    return float(distanceData[startidx][endidx])

 ########## Load Packages #############

# packageLookup(): package id and a specifc time are inputs
# Updates the status of the package according to the specifc time
# Primarily used for UI/Display purposes


def packageLookup(id, time):
    package = packageData.get(id)
    package.update_status(time)
    # ensures that the wrong address is shown until the correct address is known at 10:20 AM
    if id == 9:
        if package.address == '410 S State St' and time < datetime.timedelta(hours=10, minutes=20):
            package.changeAddress(
                '300 State St', 'Salt Lake City', 'UT', '84103')
    print(package)


# Create instance of HashTable to 'packageData'
packageData = HashTable()

# Place all of the packages from the csv file to 'packageData'
extractPackages(packageData, 'wgupsPackages.csv')


########## Package Delivery #############

# displayTruckStats(): Display truck metrics after the simulation of deliveries
def displayTruckStats(truck):
    print(f'Truck {truck.truck_id}:')
    print('------------')

    print(f'Time Departed: {truck.time_started}')
    print(f'Time Returned: {truck.time_depart}')
    print(f'Time driven: {round(truck.traveled/18, 2)} hours')
    print(f'Time Distance: {round(truck.traveled, 2)} miles\n')

# packageDelivery(): Simulates the delivery process by finding out shortest distance and perform calulations to store data.
# The packages are sorted according to the Greedy Nearest Neighbor Algorithm, which allows the calculation of the delivery time for each package.


def packageDelivery(truck):

    # Switches the address for package #9 after 10:20 AM
    if 9 in truck.packages:
        # Verifies that the truck with package #9 leaves after being updated by checking that the truck departs after 10:20 AM
        # since information is unknown until 10:20 AM.
        if truck.time_started > datetime.timedelta(hours=10, minutes=20):
            pkg = packageData.get(9)
            if pkg.address != '410 S State St':
                print(f'{colors.YELLOW}New address information for Package #9 received! Updating new address to: 410 S. State St., Salt Lake City, UT 84111......')
                # New address information passed as arguments
                pkg.changeAddress('410 S State St',
                                  'Salt Lake City', 'UT', '84111')
                print(f'{colors.GREEN}Package #9 Successfully Changed{colors.ENDC}')

    # Holds the packages as a temporary storage to sort them in the truck
    tempStorage = []
    for id in truck.packages:
        package = packageData.get(id)
        tempStorage.append(package)

    truck.packages.clear()

    # Loops through the temporary storage and sorts the packages accorrding to shortest distance into the truck
    while len(tempStorage) > 0:

        nearestAddress = 500
        upcomingPackage = None

        for package in tempStorage:
            distance = extractDistance(truck.location, package.address)

            if distance <= nearestAddress:
                nearestAddress = distance
                upcomingPackage = package

        # Place shortest distance into truck and remove package from temporary storage
        truck.packages.append(upcomingPackage.id)
        tempStorage.remove(upcomingPackage)

        # The current location of the truck is the address of the package last delivered
        truck.location = upcomingPackage.address
        upcomingPackage.depart = truck.time_depart

        # Amount of miles truck traveled is updated
        truck.traveled += nearestAddress
        # Time truck took to deliver the package is calculated according to the constant 18 mph speed
        truck.time_depart += datetime.timedelta(hours=nearestAddress/18)
        # Package arrival time is updated according to the time the truck took to arrive
        upcomingPackage.arrival = truck.time_depart
        # Display the Truck status in the simulation
        print(f'{truck.time_depart} Truck {truck.truck_id} has delivered Package(s) to: "{locationFromAddress(upcomingPackage.address)}"')

    # Time calculated for the truck to arrive back to the headquarters from last delivery location
    distance = extractDistance(truck.location, '4001 South 700 East')
    truck.traveled += distance
    truck.time_depart += datetime.timedelta(hours=distance/18)
    # Display that truck is now arriving back
    print(f'{truck.time_depart} Truck {truck.truck_id} now arriving back to: "{locationFromAddress("4001 South 700 East")}"')


########## Main class  #############
#
# Class main: UI/Display and the logic for it starts
class Main:

    while True:
        print("Welcome to the Western Governors University Parcel Service (WGUPS)")
        print("Would you like to simulate today's route?")
        print("y - Begin simulation and View Package Information")
        print("n - Exit")

        # Create instance of Truck object for 'truck1' (Truck 1)
        truck1 = Truck(1, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34,
                       37, 40], "4001 South 700 East", datetime.timedelta(hours=8))

        # Create instance of Truck object for 'truck2' (Truck 2)
        truck2 = Truck(2, [3, 6, 18, 23, 25, 26, 27, 35, 36, 38, 39],
                       "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

        # Create instance of Truck object for 'truck3' (Truck 3)
        truck3 = Truck(3, [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 24, 28, 32, 33],
                       "4001 South 700 East", datetime.timedelta(hours=10, minutes=30))

        # Assign a truck number to the packages
        for i in range(1, 41):
            pkg = packageData.get(i)
            if i in truck1.packages:
                pkg.truckNumber = 1
            elif i in truck2.packages:
                pkg.truckNumber = 2
            elif i in truck3.packages:
                pkg.truckNumber = 3

        # Set time packages are out for delivery
        # 'timeLeft' field used to calculate the package status
        for i in range(1, 41):
            package = packageData.get(i)
            if package.id in truck1.packages:
                packageData.get(i).timeLeft = truck1.time_started
            elif package.id in truck2.packages:
                packageData.get(i).timeLeft = truck2.time_started
            elif package.id in truck3.packages:
                packageData.get(i).timeLeft = truck3.time_started

        while True:

            choice = input().lower()
            print()

            # Runs the simulation of delivery for each truck
            if choice == 'y':
                print(f'{colors.GREEN}Simulation Now Running...{colors.ENDC}\n')
                # Truck 1 out for delivery at 08:00 A.M.
                packageDelivery(truck1)
                print()
                # Trucl 2 out for delivery at 09:05 A.M. holding the packages that were delayed to arrive at 09:05 A.M. and others
                packageDelivery(truck2)
                print()

                # Previous runs of the program have concluded that truck 1 returns at 9:57 A.M., so that driver is currently available to take truck 3
                packageDelivery(truck3)
                print(f'\n{colors.GREEN}All Deliveries Completed{colors.ENDC}\n')

                # Display Truck metrics
                print(f'{colors.CYAN}Truck Statistics:{colors.ENDC}')
                print("----------------------------")
                displayTruckStats(truck1)
                displayTruckStats(truck2)
                displayTruckStats(truck3)
                print(
                    f'{colors.GREEN}Combined miles driven for all trucks: {truck1.traveled + truck2.traveled + truck3.traveled} miles')
                print(f'{colors.GREEN}Time taken for all packages: {round((truck3.time_depart-truck1.time_started).total_seconds()/3600, 2)} hours{colors.ENDC}\n')

                print('Select what to do next: ')
                print('Select "p" to find out package information - p')
                print('Select "q" to exit the application - q')

                while choice != 'p':
                    choice = input().lower()
                    if choice == 'q':  # exit application
                        exit()
                    elif choice != 'p':
                        print('Invalid choice. Please enter "p" or "q"')

                # Asks for a time to display package status
                print("Enter a time to view package information (e.g. 14:30):")
                choice = input()
                time = choice.split(':')
                (h, m) = time[0], time[1]
                time = datetime.timedelta(hours=int(h), minutes=int(m))

                # Asks if you would like to see all package statuses (a) or just a singular package status by its id (i) at the time specified
                print("Select all packages - a")
                print("Select package by id - i")

                choice = input().lower()

                if choice == 'a':
                    print(
                        f'\n{colors.CYAN}All Package Statuses at {time}{colors.ENDC}')
                    print('----------------------------')
                    for i in range(1, 41):
                        packageLookup(i, time)
                elif choice == 'i':
                    choice = input('Select a package to view (1-40): ')
                    print(f'\nAll Package Status at {time}')
                    print('----------------------------')
                    packageLookup(int(choice), time)

                break  # Get out of loop to make another choice

            elif choice == 'n':  # exit application
                exit()
            else:
                print('Invalid choice. Please enter "y" or "n"')
