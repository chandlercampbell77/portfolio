# Create a Truck class
class Truck:
    # Initializer / Constructor
    def __init__(self, id, packages, mileage, start_time, time_now):
        self.id = id
        self.packages = packages
        self. mileage = mileage
        self.start_time = start_time
        self.time_now = time_now
        # Start at the hub
        self.address = "4001 South 700 East"
        self.address_id = 0

    def __str__(self):
        return (f"ID: {self.id}, Packages: {self.packages}, Mileage: {self.mileage}, StartTime: {self.start_time}"
                f", FinishTime: {self.time_now}")
