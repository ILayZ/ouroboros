class ToolBase:
    pass

class ToolEntry:
    def __init__(self, name, schema, function):
        self.name = name
        self.schema = schema
        self.function = function