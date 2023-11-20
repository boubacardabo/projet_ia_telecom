In this file we'll see how to install Autogen and use it on Télécom GPUs

1. Connect to Télécom Paris network using OpenVPN GUI. Follow the steps [here](https://eole.telecom-paris.fr/vos-services/services-numeriques/connexions-aux-reseaux/openvpn-avec-windows).

2. Connect by SSH to Télécom GPUs. See how to do it [here](https://eole.telecom-paris.fr/vos-services/services-numeriques/connexions-aux-reseaux/openvpn-avec-windows).

3. `pip install openllm`
4. Verify installation with `openllm -h`
5. openllm is installed in `~/.local/bin`. Go into that directory
6. `./openllm start` allows you to see the LLMservers that you can launch. Make sure to book a GPU first using `CUDA_VISIBLE_DEVICES=0` for example.

