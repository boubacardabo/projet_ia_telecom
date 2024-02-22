#!/bin/bash

#This script is to launch an OpenLLM server with Mixtral.

#Connect to Télécom Paris network using OpenVPN GUI. Follow the steps here :
#https://eole.telecom-paris.fr/vos-services/services-numeriques/connexions-aux-reseaux/openvpn-avec-windows

#Connect by SSH to Télécom GPUs

#Make the script executable by running the following command in your terminal:
#chmod +x script_openllm.sh

#script usage : 
#./script_openllm.sh <CUDA_VISIBLE_DEVICES>



###################################################################################################


# Check if openllm is already installed
if ! command -v openllm &> /dev/null; then
    # openllm is not installed
    echo "please install openllm (more generally depedencies in requirements.txt)"
fi

# Check if the CUDA_VISIBLE_DEVICES argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <CUDA_VISIBLE_DEVICES> <MODEL_NAME> (default:mistralai/Mixtral-8x7B-Instruct-v0.1)"
    exit 1
fi

# Add ~/.local/bin to the PATH if it's not already included.
# openllm is installed in ~/.local/bin. to use this script, you have to have ~/.local/bin to the PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    export PATH="$HOME/.local/bin:$PATH"
fi

# Kill the process listening on port 3000. Kill only if there is a proces to kill. Somehow it doesn't work if you don't kill them. 
if lsof -t -i:3000 &> /dev/null; then
    lsof -t -i:3000 | xargs kill -9
fi


# Set CUDA_VISIBLE_DEVICES environment variable
export CUDA_VISIBLE_DEVICES="$1"


# Check if the user provided an argument for the model
if [ $# -eq 2 ]; then
    model="$2"
else
    # Default model if no argument is provided
    model="TheBloke/Mistral-7B-Instruct-v0.2-AWQ"
fi

openllm start "$model" --backend vllm --quantize awq --max_new_tokens 2048


pkill -f 'bentoml|openllm'

###################################################################################################

# For some reason, it only works when CUDA_VISIBLE_DEVICES=0 (and not 1 or 2) on Télécom GPUs. 
#I haven't find a way to solve this problem yet.

#`--backend` pt is suboptimal, and `--backend vllm` is better, but somehow vllm doesn't run on the Télécom GPUs
# --quantize int4 : quantization of the model (that way, 25 Gb are required instead of 100Gb)
# --max_new_tokens 2048 : maximum number of new tokens that can be generated.

#In OpenLLM source file, you way want to change the timeout value for a bigger time. You can modify it in the source code
#at "~/.local/lib/python3.10/site-packages/openllm_client/_http.py", for the `timeout` argument 
#in the __init__ method of the HTTPClient Python class.


#if you get this error :
#-bash: ./backend/script_openllm.sh: /bin/bash^M: bad interpreter: No such file or directory
# thenk you can solve it be using the command :
#sed -i 's/\r$//' ./backend/script_openllm.sh



### If it doesn't work, try to
#modify the file  ~/.local/lib/python3.10/site-packages/langchain_community/llms/openllm.py by replacing it by the code at https://github.com/langchain-ai/langchain/blob/3d94cfdaf0c82ab67849f9e0b6a120654193025c/libs/community/langchain_community/llms/openllm.py
#Back at the time, I had to do that, but maybe they patched the issue within the last updates.