from local_agent_workspace.core.tools.tool_registry import ToolRegistry
from local_agent_workspace.core.tools.file_tools import (
    list_files,
    read_file,
    search_files
)

def register_file_tools(registry: ToolRegistry) -> None:
    registry.register(
        name="list_files",
        description=(
            "List available Markdown and TXT documents "
            "in the project knowledge repository."
        ),
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        function=list_files
    )

    registry.register(
        name="read_file",
        description=(
            "Reads the content of a Markdown or TXT document "
            "from the project knowledge repository. "
            "Use a relative file path."
        ),
        parameters={
            "type": "object",
            "properties": {
                "relative_path": {
                    "type": "string",
                    "description": "Relative path of the document."
                }
            },
            "required": ["relative_path"],
            "additionalProperties": False
        },
        function=read_file
    )

    registry.register(
        name="search_files",
        description=(
            "Searches for a text term inside all available "
            "Markdown and TXT documents."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Text to search for."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        function=search_files
    )    