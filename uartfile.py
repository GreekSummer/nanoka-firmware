import storage
import time
import busio
import board
import adafruit_hashlib as hashlib

class UartReceiver():
    def __init__(self, uart):
        self.uart = uart
        
    def read_uart(self, buffer_size, utf=False):
        for t in range(10):
            data = self.uart.read(buffer_size)
            if not data == None:
                if utf:
                    try:
                        return data.decode("utf-8")
                    except:
                        raise Exception("Invalid unicode. Bad baudrate?")
                else:
                    return data
            time.sleep(0.1)
                
        raise Exception("Response not received")
    
    def write_uart(self, msg):
        for x in range(10):
            self.uart.write(msg)
            response = self.read_uart(3, utf=True)
            
            if response == "ACK":
                return True
            
        raise Exception("Command not acknowledged")
            
    def receive(self, filename):
        file = open(filename, "wb")
        
        self.write_uart("READY")
        
        while True:
            self.write_uart("NEXT")
            data = self.read_uart(4)
            while True:
                succesful_attempts = 0
                for x in range(3):
                    self.write_uart("HASH")
                    received_hash = self.read_uart(32)
                    h = hashlib.sha256()
                    h.update(data)
                    calculated_hash = h.digest()
                    
                    if received_hash == calculated_hash:
                        succesful_attempts += 1
                    
                if succesful_attempts == 3:
                    file.write(data)
                    break
                else:
                    print("crc mismatch!!!")
            
            self.write_uart("LEFT")
            response = self.read_uart(3, utf=True)
            
            if response == "NO":
                file.close()
                return True
            elif response == "YES":
                pass   








    