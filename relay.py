import board
import digitalio

class RelayControl():
    def __init__(self):
        self.relay = digitalio.DigitalInOut(board.GP20)
        self.relay.direction = digitalio.Direction.OUTPUT
        self.relay.value = False
    
    def switch(self, state):
        self.relay.value = state
    
    def getState(self):
        return self.relay.value
        
    
    
        