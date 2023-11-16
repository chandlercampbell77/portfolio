# Create Hash Table class
class HashTable:
    # Initializer / Constructor
    def __init__(self):
        # Use size 40 because there are 40 packages
        self.size = 40
        self.table = [None] * 40

    # Insert method
    def insert(self, package):
        # Hash Table is zero-indexed, so subtract 1
        index = package.id - 1
        # Insert into hash
        self.table[index] = package

    # Lookup method
    def lookup(self, id):
        # Hash Table is zero-indexed, so subtract 1
        index = id - 1
        # Return the package
        return self.table[index]


