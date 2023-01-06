# SSH

**SSH** stands for **Secure Shell Protocol**, which enables you to connect to remote server safely.

![image](https://user-images.githubusercontent.com/40289485/210223930-1138fb9f-5230-415d-a595-3239113372c8.png)

login to romote server:

```Bash
ssh <username>@<host>
```

Before you login in, you need to generate keys for ssh connection:

```Bash
ssh-keygen -t rsa -b 4096
```
You will get two keys, a public one and a private one.

- public key  :  `~/.ssh/id_rsa.pub`
- private key :  `~/.ssh/id_rsa`   ,please don't share this with others.       

What you need to do is just add you local public key to `~/.ssh/authorized_keys` on host server.