# Windows Linux Subsystem

In this section, we will briefly demonstrate how to install a Linux subsystem on Windows using WSL (Windows Subsystem for Linux).

## Official Documents

- English version: [https://docs.microsoft.com/en-us/windows/wsl/install](https://docs.microsoft.com/en-us/windows/wsl/install)
- Japanese version: [https://docs.microsoft.com/ja-jp/windows/wsl/install](https://docs.microsoft.com/ja-jp/windows/wsl/install)
- Chinese version: [https://docs.microsoft.com/zh-cn/windows/wsl/install](https://docs.microsoft.com/zh-cn/windows/wsl/install)

## Prerequisites

You must be running Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11.

## Installation Steps

### Step 1: Open Terminal as Administrator

Open your terminal as administrator (right-click the icon and you will see the option).

### Step 2: Install WSL

Run the following command:

```bash
wsl.exe --install
```

<img width="738" alt="install_wsl" src="https://user-images.githubusercontent.com/40289485/187106933-9578a013-0d22-40a6-95af-20d97838400e.PNG">

### Step 3: Reboot Your Computer

Restart your computer to complete the installation.

### Step 4: Run the Subsystem

After rebooting, run the subsystem from the Start menu or by typing `wsl` in the command prompt.

<img width="738" alt="username" src="https://user-images.githubusercontent.com/40289485/187106625-714e1b8d-fc29-4995-b414-48040dffdfb7.PNG">

### Step 5: Setup Username and Password

When prompted, create a username and password for your Linux distribution.

<img width="738" alt="username_password" src="https://user-images.githubusercontent.com/40289485/187106674-2129caf0-ec72-4632-93a1-7f2e63519174.PNG">

### Step 6: Ready to Go!

Your WSL installation is complete! You can now use Linux commands in your Windows environment.

<img width="738" alt="successful_installation" src="https://user-images.githubusercontent.com/40289485/187106730-1f1de14d-9d47-496d-8a57-73303413d83f.PNG">

## Additional Notes

- By default, `wsl.exe --install` installs WSL2, which is the latest version and recommended for most users.
- You can access your Windows files from WSL at `/mnt/c/` (for C: drive).
- To update WSL, run: `wsl --update`
- To check your WSL version, run: `wsl --version`
