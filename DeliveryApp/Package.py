# Create a package class
class Package:
    # Initializer / Constructor
    def __init__(self, id, address, deadline, city, state, zip, weight, status, delivery_time):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zip = zip
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time
        self.address_id = 0
        self.enroute_time = None
        self.truck = None

    # Method needed for user interface: updates status based on user's given time
    def current_status(self, time):
        if time < self.enroute_time:
            self.status = "At Hub"
        elif time >= self.enroute_time and time < self.delivery_time:
            self.status = "En Route"
        elif time >= self.delivery_time:
            self.status = "Delivered"

    def __str__(self):
        return (f"ID: {self.id}, Truck: {self.truck}, Status: {self.status}, Deadline: {self.deadline}, Delivered: {self.delivery_time}"
                f", Address: {self.address}, {self.city}, {self.state}, {self.zip}, Weight: {self.weight}")

