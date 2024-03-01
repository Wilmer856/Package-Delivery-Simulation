
# truck.py: Truck class to store truck information
#
# The trucks are also used to store packages within the packages field
#
class Truck:

    def __init__(self, truck_id, packages, location, time_depart):
        self.truck_id = truck_id
        self.packages = packages
        self.location = location
        self.time_depart = time_depart
        self.time_started = time_depart
        self.traveled = 0

    def __str__(self):
        return f'{self.truck_id} {self.packages} {self.location} {self.time_depart} {self.traveled}'
