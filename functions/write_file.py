import os

def write_file(working_directory, file_path, content):
    SCOPE_ERROR = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    path = os.path.join(working_directory, file_path)
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return SCOPE_ERROR

    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        with open(path, 'w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Failed to write to "{file_path}": {str(e)}'
