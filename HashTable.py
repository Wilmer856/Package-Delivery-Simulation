#
#  HashTable.py: Stores HashTable class that is used for the packages
#
#
#   -delivery address
#   -delivery deadline
#   -delivery city
#   -delivery zip code
#   -package weight
#   -delivery status (i.e., at the hub, en route, or delivered), including the delivery time


class HashTable:

    def __init__(self):
        self.cap = 64
        self.size = 0
        self.table = [None] * self.cap

    # Create hash from key
    def _hash(self, key):
        sum = 0
        for val in str(key):
            sum += ord(val)
        return sum % self.cap

    # Insert into hash table
    def insert(self, key, value):
        hash = self._hash(key)
        item = [key, value]

        if self.table[hash] is None:
            self.table[hash] = list([item])
            return True
        else:
            for set in self.table[hash]:
                if set[0] == key:
                    set[1] = value
                    return True
                self.table[hash].append(item)

    # Return the value from the key
    # In this case, returns a package throughout the program
    def get(self, key):
        hash = self._hash(key)
        if self.table[hash] is not None:
            for set in self.table[hash]:
                if set[0] == key:
                    return set[1]
        return None

    # Remove a key/value pair from the hash table
    def remove(self, key):
        hash = self._hash(key)

        if self.table[hash] is None:
            return False

        for i in range(0, len(self.table[hash])):
            if self.table[hash][i][0] == key:
                self.table[hash].pop(i)
                if not (len(self.table[hash])):
                    self.table[hash] = None
                return True
            return None

    # Print the key/value pairs
    def print(self):
        for item in self.table:
            if item is not None:
                print(item)
