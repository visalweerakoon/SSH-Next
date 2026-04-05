# SSH Next

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)
![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Release](https://img.shields.io/badge/Release-v1.0-orange.svg)

**SSH Next** is a lightweight desktop SSH client built with **Python + PyQt5**.  
It provides a simple GUI to connect to remote Linux/Windows servers via SSH and execute commands in a terminal like environment.

---

## Features

- Secure SSH connection using **Paramiko**
- Clean and simple **PyQt5 GUI**
- Built in terminal-like command interface
- Real time output streaming from server
- Supports username, password, host, and port
- Lightweight and fast
- Interactive shell session support

---

## How It Works

SSH Next establishes an SSH connection using **Paramiko** and opens an interactive shell channel.

1. User enters server credentials  
2. Application creates SSH session  
3. Interactive shell is opened  
4. Commands are sent to remote server  
5. Output is streamed back in real time  

---

## Requirements

- Python 3.10+
- PyQt5
- Paramiko

### Install dependencies using requirements.txt

```bash
pip install -r requirements.txt
