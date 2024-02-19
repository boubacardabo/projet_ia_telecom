import os
import sys
backend_folder = f"{os.getcwd()}\\backend"
if backend_folder not in sys.path:
    sys.path.append(backend_folder)

path_to_remove = f"{os.getcwd()}\\backend\\dataset"
if path_to_remove in sys.path:
    sys.path.remove(path_to_remove)


from dataset import dataset
from utils.main import write_function_to_file2


id = 8
function_string_whole = dataset[id][ 'whole_func_string']
func_code_url = dataset[id]["func_code_url"]
print(func_code_url)

write_function_to_file2(function_string_whole, backend_folder + "\\code_writer_usecase_dataset\\functions.py")

file_path = backend_folder + "\\code_writer_usecase_dataset\\functions.py"


