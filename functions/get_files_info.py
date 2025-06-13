import os.path

def get_files_info(working_directory, directory=None):
    not_dir_error = f'Error: "{directory}" is not a directory'
    outside_scope_error = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if directory is None:
        return not_dir_error
    if directory.startswith('../') or directory.startswith('/'):
            return outside_scope_error

    path = os.path.join(working_directory, directory)
    if path.endswith('.'):
        path = path[:-1]
    is_dir = os.path.isdir(path)
    is_file = os.path.isfile(path)
    if is_dir:
        path_content = os.listdir(path) if is_dir else []
        content = ""
        for item in path_content:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                content += f'{item}: file_size={os.path.getsize(item_path)}, is_dir=True\n'
            elif os.path.isfile(item_path):
                content += f'{item}: file_size={os.path.getsize(item_path)}, is_dir=False\n'
        return content
    elif is_file:
        size = os.path.getsize(path)
        return f'{path}: file_size={size}, is_dir={is_dir}'
    return not_dir_error
