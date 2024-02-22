# Generative AI trained for software debugging and validation

## Project Overview

Create a generative AI able to support NXP developers during debugging phases and able to predict new bugs based on code/test updates. The model sohuld also be able to generate tests (unit, system) in Python for  NFC/UWB products. The AI must be able to understand the domain, the specification and the existing tests. RAG methods (Langchain,...) with open source models (Code Llama, Llama 2...) will be used.

## Architecture
See [architecture](architecture/README.md) for more information 

## End goals
Generative AI trained for software validation :

    - Code Writer:
        Use case: On demand generate of test from specification (unit, system)

    - Code Coverage:
        Use case: Generate missing tests improving the code coverage (positive and negative tests) 
        Use case: Injects invalid, malformed, or unexpected inputs into a system to reveal software defects and vulnerabilities.

    - Code Tester:
        Use case: Dynamic selection of test cases to run for the verification of code updates.

    - Log Reader:
        Use case: Chat with an AI on a large source of logs.

    - Advanced query with natural language
        Use case: Detect code error based on the log tracking - data lake.




Generative AI trained for software debugging:

    - Code Debugger:
        Use case: Detect new bugs by tracking the source evolution (testbench, tests, code, specs).
        Use case: Assist developers during the debugging phase.

    - Code Reader:
        Use case: Check if the source code is aligned to specification (UML,…).

    - Code Assistant:
        Use case: Understand existing source code, translate to human readable form.



# Launching the LLM-powered application



- Create a venv (make sure to have a python version more recent than *3.10.12*)

```bash
python3 -m venv venv
```


- Activate the venv

```bash
source venv/Scripts/activate
```
- Install required packages

```bash
pip install -r ./frontend/requirements.txt
```

- Run the application
```bash
streamlit run ./frontend/home.py
```

- Make sure to have a LLM server running. **If there already is a LLM inference server running on the cluster**, skip this step. Otherwise, you can launch a LLM inference server by doing the following :   


  1. Connect to Télécom Paris network using OpenVPN GUI. Follow the steps [here](https://eole.telecom-paris.fr/vos-services/services-numeriques/connexions-aux-reseaux/openvpn-avec-windows).

  2. Connect by SSH to one of Télécom GPU clusters. See how to do it [here](resources/GPU_access.md).
   

  3. Launch an LLM inference server. See how to do it [here](OpenLLM/OpenLLM.md).
   


- Now, you need to make an SSH tunnel between your local machine and the remote machine. See how to do it [here](resources/tunnel_SSH.md).


Normally, you should now ready to use the application.
<br>
<br>
<br>
<br>

## Developer mode and development recommendation

To test the backend, you can upload the `backend` folder to the remote machine using the *Secure Copy Protocol* on your local machine:

```bash
scp -r <absolute_path_of_backend_folder> <your_id>3@gpu<number_cluster_gpu>.enst.fr:/home/infres/<your_id>
```

don't forget to also sent your `.env`.


You can use a *virtual environment* :

```bash
python3 -m venv venv
source venv/Scripts/activate
pip install -r ./backend/requirements.txt
```



and then launch an entrypoint (`main.py`) file on the remote machine:

```bash
CUDA_VISIBLE_DEIVCES=<ID_OF_YOUR_GPU>, python3 ./backend/test/main.py
``` 
for example. 

 Note that it's important to launch files from the parent directory of backend (because the `os.getcwd` method returns the current working directory of the process and that return value is internally used by Python to manage the paths of imports of modules).

 After you're done, make sure to kill your process (`Ctrl + D` should be enough) to free the memory of the GPU.


 ## adding usecase

make one folder `backend` per usecase.

--- 
<br>

**additional information**
If you install models on télécom GPUs using HuggingFace, they will be in: 
`~/.cache/huggingface/hub`
