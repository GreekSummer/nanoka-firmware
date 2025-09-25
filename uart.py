import board
import busio
import time

while True:
            
class Console():
    def __init__(self):
        self.uart = busio.UART(tx=board.GP12, rx=board.GP1, baudrate=57600, timeout=0.1)
        
    def poll(self):
    data = uart.read(1)
    if not data == None:
        if data == b'\r':
            uart.write(b'\n\r\x1b[32mNanoka\x1b[34m >> \x1b[0m')
        elif data == b'\x7f':
            uart.write(b'\b \b')
        else:
            uart.write(data)
        
        