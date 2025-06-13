import os.path

def get_files_info(working_directory, directory=None):
    not_dir_error = f'Error: "{directory}" is not a directory'
    outside_scope_error = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if directory is None:
        return not_dir_error

    path = os.path.join(working_directory, directory)
    if path.endswith('.'):
        path = path[:-1]

    if not os.path.isdir(path):
        return not_dir_error
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return outside_scope_error

    path_content = os.listdir(path)
    content = ""
    for item in path_content:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            content += f'{item}: file_size={os.path.getsize(item_path)}, is_dir=True\n'
        elif os.path.isfile(item_path):
            content += f'{item}: file_size={os.path.getsize(item_path)}, is_dir=False\n'
    return content
