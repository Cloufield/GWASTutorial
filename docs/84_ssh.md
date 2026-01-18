# SSH

**SSH** stands for **Secure Shell Protocol**, which enables you to connect to remote servers safely.

Think of SSH as a secure way to remotely access and control another computer over the internet. Just like you can use a remote control to operate your TV from across the room, SSH allows you to operate a remote computer from your local machine. You can run commands, transfer files, and work on the remote computer as if you were sitting right in front of it, all while keeping your connection encrypted and secure.

![image](https://user-images.githubusercontent.com/40289485/210223930-1138fb9f-5230-415d-a595-3239113372c8.png)

## Login to Remote Server

```Bash
ssh <username>@<host>
```

Before you log in, you need to generate keys for SSH connection.

## SSH Keys

### Generate SSH Keys

```Bash
ssh-keygen -t rsa -b 4096
```

You will get two keys, a public one and a private one:

- **Public key**: `~/.ssh/id_rsa.pub`
- **Private key**: `~/.ssh/id_rsa`

!!! warning 
    Don't share your private key with others.    

### Copy Public Key to Remote Server

What you need to do is add your local public key to `~/.ssh/authorized_keys` on the host server.

You can do this manually or use the `ssh-copy-id` command:

```Bash
ssh-copy-id <username>@<host>
```

This command will automatically copy your public key to the remote server's `~/.ssh/authorized_keys` file.

## File Transfer

Suppose you are using a local machine:

### Download Files from Remote Host to Local Machine

```Bash
scp <username>@<host>:remote_path local_path
```

### Upload Files from Local Machine to Remote Host

```Bash
scp local_path <username>@<host>:remote_path
```

!!! info Copy Directories

    `-r` : Copy recursively. This option is needed when you want to transfer an entire directory. 

!!! example
    Copy the local work directory to remote home directory:
    ```Bash
    scp -r /home/gwaslab/work gwaslab@remote.com:/home/gwaslab 
    ```
    
## SSH Tunneling

### Local Port Forwarding

!!! quote 
    In this forwarding type, the SSH client listens on a given port and tunnels any connection to that port to the specified port on the remote SSH server, which then connects to a port on the destination machine. The destination machine can be the remote SSH server or any other machine. [https://linuxize.com/post/how-to-setup-ssh-tunneling/](https://linuxize.com/post/how-to-setup-ssh-tunneling/)

`-L`: Local port forwarding

```Bash
ssh -L [local_IP:]local_PORT:destination:destination_PORT <username>@<host>
```

!!! example
    Forward local port 8080 to remote server's port 80:
    ```Bash
    ssh -L 8080:localhost:80 <username>@<host>
    ```
    Then you can access the remote server's port 80 by visiting `localhost:8080` on your local machine.

### Remote Port Forwarding

`-R`: Remote port forwarding (reverse tunneling)

```Bash
ssh -R [remote_IP:]remote_PORT:destination:destination_PORT <username>@<host>
```

This allows the remote server to access services on your local machine.

## Other SSH Options

- `-f`: Send to background
- `-p`: Port for connection (default: 22)
- `-N`: Do not execute any commands on the remote host (useful for port forwarding only)
- `-v`: Verbose mode (use `-vv` or `-vvv` for more verbosity)
- `-X`: Enable X11 forwarding (for GUI applications)
- `-C`: Enable compression
- `-i`: Specify identity file (private key) to use

!!! example
    Connect to a server on a non-standard port with verbose output:
    ```Bash
    ssh -p 2222 -v <username>@<host>
    ```
