class Planet:
    def __init__(self, name, resource):
        self.name = name
        self.resource = resource

    def give_resource(self):
        return self.resource
