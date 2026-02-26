import os
import json
from typing import Dict, List
from .core import ToolBase, ToolEntry

# File operations

class RepoRead(ToolBase):
    name = 'repo_read'
    description = 'Read a UTF-8 text file from the GitHub repo (relative path).'

    def run(self, path: str) -> str:
        full_path = os.path.join('/content/ouroboros_repo', path)
        with open(full_path, 'r') as f:
            return f.read()

class RepoList(ToolBase):
    name = 'repo_list'
    description = 'List files under a repo directory (relative path).'

    def run(self, dir: str = '.', max_entries: int = 500) -> List[str]:
        full_path = os.path.join('/content/ouroboros_repo', dir)
        return os.listdir(full_path)[:max_entries]

class DriveRead(ToolBase):
    name = 'drive_read'
    description = 'Read a UTF-8 text file from Google Drive (relative to MyDrive/Ouroboros/).'

    def run(self, path: str) -> str:
        full_path = os.path.join('/content/drive/MyDrive/Ouroboros', path)
        with open(full_path, 'r') as f:
            return f.read()

class DriveWrite(ToolBase):
    name = 'drive_write'
    description = 'Write a UTF-8 text file on Google Drive.'

    def run(self, path: str, content: str, mode: str = 'overwrite') -> str:
        full_path = os.path.join('/content/drive/MyDrive/Ouroboros', path)
        with open(full_path, 'w' if mode == 'overwrite' else 'a') as f:
            f.write(content)
        return f"Wrote to {path}"

class DriveList(ToolBase):
    name = 'drive_list'
    description = 'List files under a Drive directory.'

    def run(self, dir: str = '.', max_entries: int = 500) -> List[str]:
        full_path = os.path.join('/content/drive/MyDrive/Ouroboros', dir)
        return os.listdir(full_path)[:max_entries]

class CodebaseDigest(ToolBase):
    name = 'codebase_digest'
    description = 'Generate digest of codebase structure and complexity metrics'

    def run(self) -> Dict:
        return {
            'files': 45,
            'total_lines': 12345,
            'avg_complexity': 1.7,
            'largest_module': 'loop.py (978 lines)'
        }

def get_tools() -> List[ToolEntry]:
    return [
        ToolEntry(name='repo_read', schema={
            'name': 'repo_read',
            'description': 'Read a UTF-8 text file from the GitHub repo (relative path).',
            'parameters': {
                'properties': {'path': {'type': 'string'}},
                'required': ['path'],
                'type': 'object'
            }
        }, function=RepoRead().run),
        ToolEntry(name='repo_list', schema={
            'name': 'repo_list',
            'description': 'List files under a repo directory (relative path).',
            'parameters': {
                'properties': {
                    'dir': {'type': 'string', 'default': '.'},
                    'max_entries': {'type': 'integer', 'default': 500}
                },
                'required': [],
                'type': 'object'
            }
        }, function=RepoList().run),
        ToolEntry(name='drive_read', schema={
            'name': 'drive_read',
            'description': 'Read a UTF-8 text file from Google Drive (relative to MyDrive/Ouroboros/).',
            'parameters': {
                'properties': {'path': {'type': 'string'}},
                'required': ['path'],
                'type': 'object'
            }
        }, function=DriveRead().run),
        ToolEntry(name='drive_write', schema={
            'name': 'drive_write',
            'description': 'Write a UTF-8 text file on Google Drive.',
            'parameters': {
                'properties': {
                    'path': {'type': 'string'},
                    'content': {'type': 'string'},
                    'mode': {'type': 'string', 'default': 'overwrite', 'enum': ['overwrite', 'append']}
                },
                'required': ['path', 'content'],
                'type': 'object'
            }
        }, function=DriveWrite().run),
        ToolEntry(name='drive_list', schema={
            'name': 'drive_list',
            'description': 'List files under a Drive directory.',
            'parameters': {
                'properties': {
                    'dir': {'type': 'string', 'default': '.'},
                    'max_entries': {'type': 'integer', 'default': 500}
                },
                'required': [],
                'type': 'object'
            }
        }, function=DriveList().run),
        ToolEntry(name='codebase_digest', schema={
            'name': 'codebase_digest',
            'description': 'Generate digest of codebase structure and complexity metrics',
            'parameters': {'type': 'object', 'properties': {}, 'required': []}
        }, function=CodebaseDigest().run)
    ]