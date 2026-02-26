class ToolBase:
    pass

class ToolEntry:
    def __init__(self, name, schema, function):
        self.name = name
        self.schema = schema
        self.function = function

# Core file operations
from .file_tools import repo_read, repo_list, drive_read, drive_list, drive_write, codebase_digest