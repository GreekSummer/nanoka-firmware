import board
import pwmio
import time 
    
class Buzzer():
    def __init__(self):
        pass
    
    def buzz(self, duration=1, dt=32500, freq=1000):
        buzzer = pwmio.PWMOut(board.GP13, duty_cycle=dt, frequency=freq)
        start = time.monotonic()
        while time.monotonic() - start < duration:
            pass
        buzzer.deinit()
        
        

        
    
        
        
        