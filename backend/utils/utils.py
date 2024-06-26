import torch
import ast
import re
import subprocess


def select_gpu_if_available():
    dtype = torch.float32
    if torch.cuda.is_available():
        torch.set_default_device("cuda")
        dtype = torch.float16
    else:
        torch.set_default_device("cpu")
    return dtype



def get_functions(file_path):
    """Get the whole functions in a file as a string"""
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_def = ast.unparse(node).strip()
            function_with_tags = f"```python\n{function_def}\n```"
            functions.append(function_with_tags)

    return functions




def get_function_names(file_path):
    """Get the function names in a file."""
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    function_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_names.append(node.name)

    return function_names



def extract_function_from_markdown(markdown_string, remove_imports=True):
    """Extract Python code from LLM output."""
    # Define a regular expression pattern to match the code block containing a function
    pattern = r"```python\s*([\s\S]+?)\s*```"
    # Search for the code block in the markdown string
    match = re.search(pattern, markdown_string)
    # If a match is found, extract the content of the code block
    if match:
        function_code = match.group(1)
        # Remove import statements from the function code
        if remove_imports :
            function_code_cleaned = re.sub(r'^import\s.*?$', '', function_code, flags=re.MULTILINE)
            function_code_cleaned = re.sub(r'^from\s.*?$', '', function_code_cleaned, flags=re.MULTILINE)
            function_code = function_code_cleaned
        return function_code.strip()
    else:
        return None
    


def write_function_to_file(function_code, file_path, function_name):
    """write in a file (used by code_writer_unit_test_usecase)"""
    with open(file_path, 'w') as file:
        file.write("import pytest\n")
        file.write("import os\n")
        file.write("import sys\n")
        file.write('backend_folder = f"{os.getcwd()}/backend"\n')
        file.write('sys.path.append(backend_folder)\n')
        file.write(f"from code_writer_unit_test_usecase.functions import {function_name}\n\n")
        file.write(function_code)
        file.write("\n\n")
        file.write(f'retcode = pytest.main(["-x","{file_path}"])')



def write_function_to_file2(function_string_whole, file_path):
    """write in a file (used by code_writer_system_test_usecase)"""
    with open(file_path, 'w') as file:
        file.write(function_string_whole)
        file.write("\n\n")
        file.write(f'retcode = pytest.main(["-x","{file_path}"])')
        
        

def execute_generated_file(file_path):

    """To execute a python file from a call of this function"""

    result = subprocess.run(["python3", file_path], capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode



