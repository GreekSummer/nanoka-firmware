import time
import uartfile
import os
import json
import traceback

class Commands():
    def __init__(self, beeper, relay, uart, settings):
        self.uart = uart
        self.beeper = beeper
        self.relay_control = relay
        self.uart_receiver = uartfile.UartReceiver(uart)
        self.settings = settings
        
        f = open("help.txt", "r")
        self.help = "".join(f.readlines()).replace("\n", "\r\n")
        f.close()
        
        self.map = {
            "poem": self.poem,
            "relay": self.relay,
            "beep": self.beep,
            "upload_file": self.upload_file,
            "cat": self.cat,
            "ls": self.ls,
            "rm": self.rm,
            "mkdir": self.mkdir,
            "print_settings": self.print_settings,
            "set_setting": self.set_setting,
            "echo": self.echo,
            "eval": self.run_code,
            "help": self.print_help
            }
    
    def execute(self, cmd):
        self.uart.write("\n\r")
        try:
            cmd_name = cmd.split(" ")[0]
            args = cmd.split(" ")[1:]
            command = self.map[cmd_name]
            command(args)
        except KeyError:
            self.uart.write(f"command {cmd_name} not known. Type help for help.")
        except Exception as e:
            if self.settings.get()['commands']['print_exception_on_console']:
                self.uart.write("\r\n\x1b[0;31m".encode())
                self.uart.write("".join(traceback.format_exception(type(e), e, e.__traceback__)).encode())
            else:
                self.uart.write(f"\r\n\x1b[0;31m An error occured: {e}".encode())
            
            if self.settings.get()['commands']['raise_exception_on_command_error']:
                raise e
    
    def relay(self, args):
        if not args:
            self.uart.write("Usage: relay on/off")
            return
        state = args[0]
        
        if state == "on":
            self.relay_control.switch(True)
        elif state == "off":
            self.relay_control.switch(False)
        else:
            self.uart.write("\n\rState must be either on or off\n\r")
    
    def beep(self, args):    
        try:
            freq = int(args[0])
            dt = int(args[1])
            duration = int(args[2])
        except:
            self.uart.write("Invalid arguments")
            return
        
        if freq < 0 or freq > 6000:
            self.uart.write("Invalid frequency: " + str(freq))
            return
        
        if not duration > 0:
            self.uart.write("Invalid duration")
            return
            
        if not dt > 0 or dt > 65535:
            self.uart.write("Invalid duty cycle")
            return
            
        self.beeper.buzz(duration, dt, freq)
        
    def upload_file(self, args):
        filename = args[0]
        try:
            self.uart_receiver.receive(filename)
        except Exception as e:
            self.uart.write("\n\rFailed: client didn't negotiate. Are you running the NANOKA client or a bare terminal?")
            
    def ls(self, args):
        if not args:
            self.uart.write("Usage: ls [directory]")
            return
        
        path = args[0] if args else "/"
        files = os.listdir(path)
        for f in files:
            self.uart.write(f + "\r\n")

    def cat(self, args):
        if not args:
            self.uart.write("Usage: cat <filename>")
            return
        
        filename = args[0]
        with open(filename, "r") as f:
            for line in f:
                self.uart.write(line.rstrip("\n") + "\r\n")
                
    def rm(self, args):
        if not args:
            self.uart.write("Usage: rm <filename> or rm -r <directory>")
            return
        
        if "-r" in args:
            path = args[1]
            os.rmdir(path)
        else:
            path = args[0]
            os.remove(path)
        
    def mkdir(self, args):
        if not args:
            self.uart.write("Usage: mkdir <directory>")
        
        os.mkdir(args[0])
            
    def set_setting(self, args):
        *keys, value = args
        data = self.settings.get()
        try:
            target = data
            for k in keys[:-1]:
                target = target[k]
            
            final_key = keys[-1]
            data_type = type(target[final_key])
            if data_type == bool:
                if value.lower() == "true":
                    value = True
                else:
                    value = False
            else:
                value = data_type(value)
            
            target[final_key] = value
            self.settings.save()
        except ValueError:
            self.uart.write("Invalid data type entered.")
            
    def print_settings(self, args):
        configs = self.settings.get()

        def descend(data, prefix=""):
            lines = []
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        lines.append(f"{prefix}{key}:")
                        lines.extend(descend(value, prefix + "  "))
                    else:
                        lines.append(f"{prefix}{key}: {value}")
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    lines.append(f"{prefix}[{i}]")
                    lines.extend(descend(item, prefix + "  "))
            else:
                lines.append(f"{prefix}{data}")
            return lines

        pretty_list = "\r\n".join(descend(configs))
        self.uart.write("\r\n" + pretty_list + "\r\n")
        
    def echo(self, args):
        self.uart.write("echo")
    
    def print_help(self, args):
        self.uart.write(self.help.encode())
        
    def run_code(self, args):
        eval(args[0])
        
    def poem(self, args):
        raven = """
        Then this ebony bird beguiling my sad fancy into smiling,
        \n\rBy the grave and stern decorum of the countenance it wore,
        \n\r“Though thy crest be shorn and shaven, thou,” I said, “art sure no craven,
        \n\rGhastly grim and ancient Raven wandering from the Nightly shore—
        \n\rTell me what thy lordly name is on the Night’s Plutonian shore!”
        \n\r    Quoth the Raven 'Nevermore.' \n\r """
        self.uart.write(raven)