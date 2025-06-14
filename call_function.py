from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_files_info import get_files_info
from functions.get_file_content import schema_get_file_content
from functions.get_file_content import get_file_content
from functions.run_python import schema_run_python_file
from functions.run_python import run_python_file
from functions.write_file import schema_write_file
from functions.write_file import write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

function_names = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}
