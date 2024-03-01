
# Custom imports: colors.py
#
# colors.py is used to display package status in a color coded fashion
#
from colors import colors


class Package:

    def __init__(self, id, address, city, state, zip, deadline, weight, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.timeLeft = None
        self.depart = None
        self.arrival = None
        self.truckNumber = None

    # update_status(): Used to set the status of a package according to a specified time provided in the function input
    def update_status(self, time):
        if self.arrival <= time:
            self.status = "DELIVERED"
        elif self.timeLeft < time:
            self.status = "EN ROUTE"
        else:
            self.status = "AT THE HUB"

    # changeAddress(): Used to change address information for a package
    # Function was specifically created for package #9's address change
    # Makes more sense to keep functions that change package information in this class.
    def changeAddress(self, address, city, state, zip):
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

    # Change the print() appearance of the package based on the status of the package
    # Set up this way for UI/Display purposes
    def __str__(self):
        if self.status == 'DELIVERED':
            return f'{colors.GREEN}Truck {self.truckNumber}: {self.id}, {self.status} ({self.arrival}), {self.address}, {self.deadline}, {self.city}, {self.zip}, {self.weight}{colors.ENDC}'
        elif self.status == "EN ROUTE":
            return f'{colors.YELLOW}Truck {self.truckNumber}: {self.id}, {self.status}, {self.address}, {self.deadline}, {self.city}, {self.zip}, {self.weight}{colors.ENDC}'
        elif self.status == 'AT THE HUB':
            return f'{colors.RED}Truck {self.truckNumber}: {self.id}, {self.status}, {self.address}, {self.deadline}, {self.city}, {self.zip}, {self.weight}{colors.ENDC}'
