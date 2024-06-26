# Generative AI trained for software debugging and validation

## Project Overview

The goal of the project is to create a generative AI able to support NXP developers during debugging and software validation phases. The AI system should be able to predict new bugs as well as unexpected behavior based on the source code of a project, and should be able to generate testing code for NFC/UWB products. During this project, we were faced against two main constraints:

- One of them is to adapt our solution to the specific source code of NFC/UWB products from NXP semiconductors, that is to say a source code mainly in Python, C and C++ to deal with microcontrollers, sensors, and electronics;

- One of the goals of our project is to serve as a Proof of Concept (PoC) for NXP to demonstrate the feasibility of developing such use cases in an open-source way. Therefore we had to use open-source technologies (one of the main consequence is that we can’t rely on the OpenAI API to build our application).

## Architecture
See the draft [architecture](architecture/README.md) for more information. 

## End goals
Generative AI trained for software validation:

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


Make sure to use Python *3.10.12*. It might work for similar version, but it's not a guarantee. If you're using conda, you can do the following :

```bash
conda update conda
conda create -n conda-env python=3.10.12
conda activate conda-env
```

You can check the Python version :

```bash
python --version
```

- Now, create a venv

```bash
python -m venv venv
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

1. Connect to Télécom Paris network using OpenVPN GUI. Follow the steps [here](https://eole.telecom-paris.fr/vos-services/services-numeriques/connexions-aux-reseaux/openvpn-avec-windows).


- You can connect yourself by SSH to the GPU directly from the web interface. You need to make an SSH tunnel between your local machine and the remote machine this also can be done from the frontend. If you have an issue, you can do it manually [here](resources/tunnel_SSH.md).

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
source venv/bin/activate
pip install -r ./backend/requirements.txt
```

Make sure the that your virtual environment name is the same as specified in the frontend ``home.py`` file in the *serve_command* variables!


and then launch an entrypoint (`main.py`) file on the remote machine:

```bash
CUDA_VISIBLE_DEIVCES=<ID_OF_YOUR_GPU>, python3 ./backend/test/main.py
``` 
for example. 

 Note that it's important to launch files from the parent directory of backend (because the `os.getcwd` method returns the current working directory of the process and that return value is internally used by Python to manage the paths of imports of modules).

 After you're done, make sure to kill your process (`Ctrl + D` should be enough) to free the memory of the GPU.


## homemade tutorial

-  Connect by SSH to one of Télécom GPU clusters. See how to do it [here](resources/GPU_access.md). 

- Launch an LLM inference server using OpenLLM. See how to do it [here](OpenLLM/OpenLLM.md).

     
 ## adding usecase to the project

make one folder `backend` per usecase.

--- 
<br>

## additional information
If you install models on télécom GPUs using *HuggingFace*, they will be in: 
`~/.cache/huggingface/hub`
