"""
Program -- fully implemented.

A TinyCStr program is a list of functions
"""

class Program:
    def __init__(self):
        self.functions = []

    def addFunction(self, function):
        self.functions.append(function)

    def getFunctions(self):
        return self.functions
