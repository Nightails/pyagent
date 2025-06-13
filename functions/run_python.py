import os
import subprocess

def run_python_file(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    if not path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        process = subprocess.run(['python', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30, check=True)
        output = f'STDOUT: {process.stdout.decode("utf-8") if process.stdout else "No output produced"}\n'
        error = f'STDERR: {process.stderr.decode("utf-8") if process.stderr else "No error produced"}\n'
        if process.returncode != 0:
            code = f'Process exited with code {process.returncode}\n'
            return f'{file_path}\n' + output + error + code
        return f'{file_path}\n' + output + error
    except subprocess.CalledProcessError as e:
        return f'Error: executing Python file: {str(e)}'
