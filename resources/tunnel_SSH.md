# Accessing `0.0.0.0:3000` of `gpu6.enst.fr` using SSH commands


## Regular SSH Tunnel (Local Port Forwarding):

```bash
ssh -L 3000:0.0.0.0:3000 username@gpu6.enst.fr
```

Replace username with your username on gpu6.enst.fr. This command forwards traffic from port ``3000`` on your local machine to port ``3000`` on ``gpu6.enst.fr``. You can then access the service running on ``gpu6.enst.fr:3000`` as if it were running locally on your machine.

## Reverse SSH Tunnel (Remote Port Forwarding):

```bash
ssh -R 3000:localhost:3000 username@gpu6.enst.fr
```

This command forwards traffic from port ``3000`` on ``gpu6.enst.fr`` to port ``3000`` on your local machine. You can use this command to allow bidirectional flow of information between your local machine and gpu6.enst.fr.

In both cases, replace username with your username on ``gpu6.enst.fr``. You'll be prompted to enter your password for the SSH connection. Once the connection is established, the tunnel will be active until you close the SSH connection.

These commands can be run from a terminal or command prompt on your local machine. Make sure you have SSH access to ``gpu6.enst.fr`` and that your username has the necessary permissions to establish SSH tunnels.

--- 
<br>
<br>
<br>
<br>



# Accessing `0.0.0.0:3000` of `gpu6.enst.fr` via PuTTy

## Description

### Regular SSH Tunnel (Local Port Forwarding):

0. Downlaod PuTTY (https://www.putty.org/)
1. 
To access `0.0.0.0:3000` of `gpu6.enst.fr` via Putty, you'll need to set up a tunnel using SSH port forwarding. Follow these steps:

1. Open Putty and enter `gpu6.enst.fr` as the hostname.
2. Under "Saved Sessions", give your session a name (e.g., "GPU6 SSH").
3. Click "Save" to save the session for future use.
4. In the left-hand category pane, navigate to Connection > SSH > Tunnels.
5. In the "Source port" field, enter `3000`.
6. In the "Destination" field, enter `0.0.0.0:3000`.
7. Make sure the "Local" radio button is selected.
8. Click "Add" to add the forwarded port.
9. Go back to the "Session" category in the left-hand pane.
10. Click "Save" again to save your changes to the session configuration.
11. Click "Open" to start the SSH connection.

Once you're connected via SSH, any traffic sent to `0.0.0.0:3000` on the remote server (`gpu6.enst.fr`) will be forwarded through the SSH tunnel to `localhost:3000` on your local machine. You can access the service running on port 3000 of the remote server as if it were running locally on your machine.

Make sure the service you're trying to access is actually running on port 3000 on the remote server (`gpu6.enst.fr`). If it's running on a different port, you'll need to adjust the port number accordingly in the SSH tunnel configuration.

By doing that, you will set up a direct SSH tunnel between the local machine and the remote machine. That is to this say information can only go from the local machine to the remote machine. In order to have bidirectionel flow of information we need to setup a reverse SSH tunnel :

### Reverse SSH Tunnel (Remote Port Forwarding):

1. Open Putty and enter `gpu6.enst.fr` as the hostname.
2. Under "Saved Sessions", give your session a name (e.g., "GPU6 SSH reverse").
3. Click "Save" to save the session for future use.
4. In the left-hand category pane, navigate to Connection > SSH > Tunnels.
5. In the "Source port" field, enter `3000`.
6. In the "Destination" field, enter `localhost:3000`.
7. Make sure the "Remote" radio button is selected.
8. Click "Add" to add the forwarded port.
9. Go back to the "Session" category in the left-hand pane.
10. Click "Save" again to save your changes to the session configuration.
11. Click "Open" to start the SSH connection.




