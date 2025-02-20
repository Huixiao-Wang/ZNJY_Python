import config

class target:
    def __init__(self, vector, label):
        self.vector = vector
        self.label = label
        self.distance = (vector[2] ** 2 + vector[0] ** 2) ** 0.5
    def __str__(self):
        return f"vector: {self.vector}, label: {config.DICTIONARY[self.label]}, distance: {self.distance}"