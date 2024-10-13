'''
Planet Class (planet.py)
○ Attributes: name, resource (e.g., "Water").
○ Methods:
■ give_resource() - returns the resource.
'''
class Planet:
    def __init__(self, name, resource):
        self.name = name
        self.resource = resource
    def give_resource(self):
        return self.resource