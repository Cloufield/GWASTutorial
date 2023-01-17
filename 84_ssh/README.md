# SSH

**SSH** stands for **Secure Shell Protocol**, which enables you to connect to remote server safely.

![image](https://user-images.githubusercontent.com/40289485/210223930-1138fb9f-5230-415d-a595-3239113372c8.png)

## Login to remote server

```Bash
ssh <username>@<host>
```

Before you login in, you need to generate keys for ssh connection:


## Keys

```Bash
ssh-keygen -t rsa -b 4096
```
You will get two keys, a public one and a private one.

- public key  :  `~/.ssh/id_rsa.pub`
- private key :  `~/.ssh/id_rsa`

!!! warning 
    Don't share your private key with others.    

What you need to do is just add you local public key to `~/.ssh/authorized_keys` on host server.

## File transfer

Suppose you are using a local machine: 

Donwload files from remote host to local machine 

```
scp <username>@<host>:remote_path local_path
```

Upload files from local machine to remote host

```
scp local_path <username>@<host>:remote_path
```

!!! info Copy directories

    `-r` : copy recursively. This option is needed when you want to transfer an entire directory. 

!!! example
    Copy the local work directory to remote home directory
    ```
    $ scp -r /home/gwaslab/work gwaslab@remote.com:/home/gwaslab 
    ```
    
## SSH Tunneling

!!! quote 
    In this forwarding type, the SSH client listens on a given port and tunnels any connection to that port to the specified port on the remote SSH server, which then connects to a port on the destination machine. The destination machine can be the remote SSH server or any other machine. [https://linuxize.com/post/how-to-setup-ssh-tunneling/](https://linuxize.com/post/how-to-setup-ssh-tunneling/)

`-L` : Local port forwarding

```
ssh -L [local_IP:]local_PORT:destination:destination_PORT <username>@<host>
```

## other SSH options

- `-f` : send to background.
- `-p`:  port for connenction (default:22).
- `-N` : not to execute any commands on the remote host. (so you will not open a remote shell but just forward ports.)
