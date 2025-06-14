import os.path
from google.genai import types

def get_files_info(working_directory, directory=None):
    DIR_ERROR = f'Error: "{directory}" is not a directory'
    SCOPE_ERROR = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if directory is None:
        return DIR_ERROR

    path = os.path.join(working_directory, directory)
    if path.endswith('.'):
        path = path[:-1]

    if not os.path.isdir(path):
        return DIR_ERROR
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return SCOPE_ERROR

    path_content = os.listdir(path)
    content = ""
    for item in path_content:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            content += f'{item}: file_size={os.path.getsize(item_path)}, is_dir=True\n'
        elif os.path.isfile(item_path):
            content += f'{item}: file_size={os.path.getsize(item_path)}, is_dir=False\n'
    return content

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
