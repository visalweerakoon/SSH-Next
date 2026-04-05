import paramiko
import re


class SSHClient:
    def __init__(self):
        self.client = None
        self.channel = None
        self.last_cmd = None

    def connect(self, host, username, password, port=22):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(
                hostname=host,
                username=username,
                password=password,
                port=int(port)
            )

            self.channel = self.client.invoke_shell()
            self.channel.settimeout(0.0)

            return "Connected"

        except Exception as e:
            return f"Connection failed: {e}"

    def send(self, cmd):
        if self.channel:
            self.last_cmd = cmd
            self.channel.send(cmd + "\n")

    def receive(self):
        if self.channel and self.channel.recv_ready():
            data = self.channel.recv(4096).decode(errors="ignore")

            # remove ANSI escape junk
            data = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', data)

            if getattr(self, 'last_cmd', None):
                echo1 = self.last_cmd + "\r\n"
                echo2 = self.last_cmd + "\n"
                if data.startswith(echo1):
                    data = data[len(echo1):]
                elif data.startswith(echo2):
                    data = data[len(echo2):]
                elif data.startswith(self.last_cmd):
                    data = data[len(self.last_cmd):]
                self.last_cmd = None

            return data
        return ""