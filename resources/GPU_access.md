**Date: 25-10-2023**

**Meeting hosted by Nils Holzenberger**

In this session, we will cover essential commands and guidelines for effectively utilizing the GPU resources at Telecom. Please take note of the following commands and recommendations:

**Connecting to Telecom's GPUs:**
```shell
ssh <id-telecom>@gpu6.enst.fr
```
This command allows you to establish a secure connection to Telecom's GPU servers. gpu1, gpu2, gpu3, ... gpu6 are accessible.

**Monitoring GPU Information:**
```shell
nvidia-smi
```
Use this command to retrieve valuable information about the GPUs, such as usage, temperature, and more.

**Navigating to Home Directory:**
```shell
cd ~
```
The `~` symbol represents your home directory, where you can store your files and data within reasonable limits.

**Utilizing GPU in Python (PyTorch):**
```python
import torch
torch.FloatTensor(1).to('cuda')
```
This Python code snippet enables the use of the reserved GPU1 through CUDA.

**Understanding CUDA_VISIBLE_DEVICES:**
`CUDA_VISIBLE_DEVICES` is a crucial environment variable for GPU reservation. You can specify the GPU you want to use with this variable.

**Reserving GPUs:**
```shell
CUDA_VISIBLE_DEVICES=0 python script.py
```
When running Python scripts, it's essential to reserve GPUs. Using an unreserved GPU may disrupt ongoing processes and result in potential bans. You can also export the variable : `export CUDA_VISIBLE_DEVICES=0` 

**PyTorch Integration:**
In PyTorch-based Python code, there's no need to define `CUDA_VISIBLE_DEVICES`. PyTorch manages GPU usage internally.

**Working with GPU Clusters:**
You can utilize multiple machines simultaneously with commands like `CUDA_VISIBLE_DEVICES=0,1`. There are a total of 6 GPUs available for your use.

**Utilizing GPUs in Python:**
In your Python code, you can employ the `.to("cuda")` method to seamlessly utilize the GPU. PyTorch will handle GPU selection automatically.

**Checking GPU Availability:**
A GPU is considered available if its GPU utilization is at 0%. Avoid using a GPU with non-zero GPU utilization, as it may be in use by someone else.

**Jupyter Notebook Limitation:**
Please note that Jupyter Notebook usage on the GPUs is not supported. You should use Python scripts for your work.

**GPU Accessibility:**
To access the GPUs, you must be connected to Telecom's network (Eduroam). If you need to use the GPUs outside Telecom, consider using a VPN.

**Cluster Usage Policy:**
It's important to be aware that Telecom's GPU cluster is intended for academic and research purposes and should not be used for commercial activities.

**Continuous Service Considerations:**
For continuous, uninterrupted GPU usage, the Telecom GPUs may not be the ideal choice. Please plan accordingly.

**Logging Out:**
To log out of a session, simply press `Ctrl` + `D`.

Thank you for adhering to these guidelines and making the most of Telecom's GPU resources. If you have any questions or require further assistance, please do not hesitate to reach out.

**Check CUDA version:**
`nvcc --version`