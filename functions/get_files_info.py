import os
from config import MAX_CHAR
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = (os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs)
        if not valid_target_dir:
            return (f'Error: Cannot list "{directory}" as it is ' "outside the permitted working directory")
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        entries = os.listdir(target_dir)
        result = []

        for entry in entries:
            entry_path = os.path.join(target_dir, entry)

            file_size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)

            result.append(
                f"- {entry}: file_size={file_size} bytes, "
                f"is_dir={is_dir}"
            )

        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"
    
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = (os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs)
        if not valid_target_dir:
            return (f'Error: Cannot list "{file_path}" as it is ' "outside the permitted working directory")
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHAR)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = (os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs)
        if not valid_target_dir:
            return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": (
            "Reads and returns the contents of a file relative to the "
            "working directory. The output is truncated if it exceeds "
            "the maximum character limit."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the file to read, relative to the "
                        "working directory."
                    ),
                },
            },
            "required": ["file_path"],
        },
    },
}


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Creates or overwrites a file with the provided content "
            "within the permitted working directory. Creates missing "
            "parent directories when necessary."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path of the file to create or overwrite, "
                        "relative to the working directory."
                    ),
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write into the file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}


available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
]