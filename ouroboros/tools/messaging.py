import os
import json
from typing import Dict, List
from .core import ToolBase, ToolEntry


class SendPhoto(ToolBase):
    name = 'send_photo'
    description = 'Send a photo to the owner via Telegram. Takes base64 PNG data or file path.'

    def run(self, path: str, caption: str = '') -> str:
        # In actual implementation, would call Telegram API
        return f"Photo {path} sent with caption: {caption}"

class SummarizeDialogue(ToolBase):
    name = 'summarize_dialogue'
    description = 'Summarize recent chat history into a concise report'

    def run(self, count: int = 50) -> str:
        # Would process chat history in real implementation
        return f"Summary of last {count} messages: [REDACTED]"

class ForwardToWorker(ToolBase):
    name = 'forward_to_worker'
    description = 'Route message to specific worker task. Used for task decomposition.'

    def run(self, worker_id: str, message: str) -> str:
        return f"Routed to worker {worker_id}: {message[:50]}..."

def get_tools() -> List[ToolEntry]:
    return [
        ToolEntry(
            name='send_photo',
            schema={
                'name': 'send_photo',
                'description': 'Send a photo to the owner via Telegram',
                'parameters': {
                    'properties': {
                        'path': {'type': 'string', 'description': 'Path to image file'},
                        'caption': {'type': 'string', 'description': 'Optional caption', 'default': ''}
                    },
                    'required': ['path'],
                    'type': 'object'
                }
            },
            function=SendPhoto().run
        ),
        ToolEntry(
            name='summarize_dialogue',
            schema={
                'name': 'summarize_dialogue',
                'description': 'Summarize recent chat history into a concise report',
                'parameters': {
                    'properties': {
                        'count': {'type': 'integer', 'default': 50}
                    },
                    'required': [],
                    'type': 'object'
                }
            },
            function=SummarizeDialogue().run
        ),
        ToolEntry(
            name='forward_to_worker',
            schema={
                'name': 'forward_to_worker',
                'description': 'Route message to specific worker task',
                'parameters': {
                    'properties': {
                        'worker_id': {'type': 'string'},
                        'message': {'type': 'string'}
                    },
                    'required': ['worker_id', 'message'],
                    'type': 'object'
                }
            },
            function=ForwardToWorker().run
        )
    ]