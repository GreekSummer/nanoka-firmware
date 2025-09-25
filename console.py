import board
import time
import microcontroller

class Console():
    def __init__(self, commands, uart):
        self.command = ""
        self.commands = commands
        self.active = False
        self.uart = uart
        
        self.codes = {
            "Enter": b'\r',
            "Backspace": b'\x7f',
            "Erase": b'\b \b',
            "Newline": b'\n\r\x1b[32mNanoka\x1b[34m >> \x1b[0m',
            "Escape": b'\x1b'
            }
        
        f = open("nanoka.ascii", "r")
        self.ascii_art = "".join(f.readlines()).replace("\n", "\r\n")
        f.close()
        
    def monitor_enable(self):
        data = self.uart.read(6)
        if not data== None:
            try:
                utf8 = data.decode("utf-8")
            except:
                self.uart.write("Bad baudrate!")
                return
                
            if utf8 == "er":
                self.active = True
                self.uart.write(self.ascii_art.encode())
                self.uart.write("\n\r\n\r\n\r")
                self.uart.write("Project Nanoka CLI (Python Core)\n\rVer 1.0\n\r")
                self.uart.write(self.codes["Newline"])
        
    def poll(self):
        if not self.active:
            self.monitor_enable()
            return
        while True:
            data = self.uart.read(1)
            if not data == None:
                
                if data == self.codes['Escape']:  
                    next1 = self.uart.read(1)
                    next2 = self.uart.read(1)
                    continue
                
                if data == self.codes['Enter']:
                    if self.command == "exit":
                        self.uart.write("Goodbye. The system will now reset.")
                        microcontroller.reset()
                    else:
                        self.commands.execute(self.command)
                    self.uart.write(self.codes["Newline"])
                    self.command = ""
                elif data == self.codes['Backspace']:
                    if not self.command == "":
                        self.uart.write(self.codes['Erase'])
                        self.command = self.command[:-1]
                else:
                    self.uart.write(data)
                    self.command += data.decode("utf-8")
        