import os
import sys
backend_folder = f"{os.getcwd()}\\backend"
if backend_folder not in sys.path:
    sys.path.append(backend_folder)

path_to_remove = f"{os.getcwd()}\\backend\\dataset"
if path_to_remove in sys.path:
    sys.path.remove(path_to_remove)







