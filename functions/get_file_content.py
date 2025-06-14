import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    FILE_ERROR = f'Error: File not found or is not a regular file: "{file_path}"'
    SCOPE_ERROR = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if file_path is None:
        return FILE_ERROR

    path = os.path.join(working_directory, file_path)

    if not os.path.isfile(path):
        return FILE_ERROR
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return SCOPE_ERROR

    try:
        with open(path, 'r') as file:
            content = file.read(MAX_CHARS)
            if len(content) >= MAX_CHARS:
                content += f'[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        return f'Error: Failed to read file "{file_path}": {str(e)}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
