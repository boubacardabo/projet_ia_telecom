import torch


def select_gpu_if_available():
    dtype = torch.float32
    if torch.cuda.is_available():
        torch.set_default_device("cuda")
        dtype = torch.float16
    else:
        torch.set_default_device("cpu")
    return dtype



import ast

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