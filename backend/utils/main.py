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

#Get the whole functions in a file as a string
def get_functions(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_def = ast.unparse(node).strip()
            function_with_tags = f"```python\n{function_def}\n```"
            functions.append(function_with_tags)

    return functions

# # Example usage:
# file_path = "backend\\code_writer_usecase\\functions.py"
# functions = get_functions(file_path)
# for func in functions:
#     print(func)

#Get the function names in a file
def get_function_names(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    function_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_names.append(node.name)

    return function_names


#extract Python code from LLM output
def extract_function_from_markdown(markdown_string):
    # Define a regular expression pattern to match the code block containing a function
    pattern = r"```python\s*([\s\S]+?)\s*```"
    # Search for the code block in the markdown string
    match = re.search(pattern, markdown_string)
    # If a match is found, extract the content of the code block
    if match:
        function_code = match.group(1)
        # Remove import statements from the function code
        function_code_cleaned = re.sub(r'^import\s.*?$', '', function_code, flags=re.MULTILINE)
        function_code_cleaned = re.sub(r'^from\s.*?$', '', function_code_cleaned, flags=re.MULTILINE)
        return function_code_cleaned.strip()
    else:
        return None
    


#write in the a file
def write_function_to_file(function_code, file_path, function_name, backend_folder):

    test_path = backend_folder + "/code_writer_usecase/function_AI_generated.py"
    with open(file_path, 'w') as file:
        file.write("import pytest\n")
        file.write("import os\n")
        file.write("import sys\n")
        file.write('backend_folder = f"{os.getcwd()}/backend"\n')
        file.write('sys.path.append(backend_folder)\n')
        file.write(f"from code_writer_usecase.functions import {function_name}\n\n")
        file.write(function_code)
        file.write("\n\n")
        file.write(f'retcode = pytest.main(["-x","{test_path}"])')


#write in the a file
def write_function_to_file2(function_string_whole, file_path):

    
    with open(file_path, 'w') as file:
        file.write(function_string_whole)
        
        




#To execute a python file from a call of this function
def execute_generated_file(file_path):
    result = subprocess.run(["python3", file_path], capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode



def extract_imports(file_path):
    imports = set()
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
    return imports


def add_imports_to_file(file_path, imports):
    with open(file_path, 'r+') as file:
        content = file.read()
        file.seek(0, 0)
        for package in imports:
            import_statement = f"import {package}\n"
            if import_statement not in content:
                file.write(import_statement)
        file.write(content)
    





def add_missing_imports(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract all the used but not imported modules
    used_modules = set()
    for line in content.split('\n'):
        # Check for modules used in the code
        if line.strip().startswith(('import ', 'from ')):
            continue  # Skip import lines
        for word in line.split():
            if word.isidentifier():
                # Add the word as a potential module
                used_modules.add(word)

    # Check if any used modules are not imported
    modules_to_import = set()
    for module in used_modules:
        if f"import {module}" not in content and f"from {module}" not in content:
            modules_to_import.add(f"import {module}")

    # Append the missing import statements to the beginning of the file's content
    if modules_to_import:
        import_statements = "\n".join(modules_to_import) + "\n"
        content = import_statements + content

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(content)