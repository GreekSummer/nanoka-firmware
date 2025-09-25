import board
import digitalio
import time
import pwmio

    
class SelfTest():
    def __init__(self, settings):
        self.relay = digitalio.DigitalInOut(board.GP20)
        self.relay.direction = digitalio.Direction.OUTPUT
        
        self.b1 = digitalio.DigitalInOut(board.GP5)
        self.b2 = digitalio.DigitalInOut(board.GP6)
        self.b3 = digitalio.DigitalInOut(board.GP8)
        
        self.settings = settings
        self.relay_switch_interval = settings['relay_switch_interval']
        self.relay_hold_time = settings["relay_hold_time"]
        self.gpio_hold_time = settings["gpio_hold_time"]
        self.gpio_test_interval = settings["gpio_test_interval"]
        
    def deinit(self):
        for gpio in [self.relay, self.b1, self.b2, self.b3]:
            gpio.deinit()
        
    def test_relay(self):
        for x in range(self.relay_switch_interval):
            self.relay.value = not self.relay.value
            time.sleep(self.relay_hold_time)
    
    def test_gpio(self):
        for b in [self.b1, self.b2, self.b3]:
            b.direction = digitalio.Direction.INPUT
            b.pull = digitalio.Pull.UP
            
            for x in range(self.gpio_test_interval):
                if b.value == False:
                    self.beep(35000, 1000, 1)
                    time.sleep(1)
                    self.beep(35000, 1000, 1)
                    time.sleep(1)
                    self.beep(35000, 1000, 1)
                    raise Exception("GPIO line high on startup!")
                time.sleep(self.gpio_hold_time)
                
    def beep(self, dt, freq, duration):
        buzzer = pwmio.PWMOut(board.GP13, duty_cycle=dt, frequency=freq)
        time.sleep(duration)
        buzzer.deinit()
                
    def run(self):
        self.test_gpio()
        self.test_relay()
        
        self.deinit()
        return True
        
                

if __name__ == "__main__":
    import config
    settings = config.Settings()
    settings.load()
    
    print("rs i: " + str(settings.get()['self_test']['relay_switch_interval']))
    print("rh t: " + str(settings.get()['self_test']["relay_hold_time"]))
    print("gh t: " + str(settings.get()['self_test']["gpio_hold_time"]))
    print("gt i: " + str(settings.get()['self_test']["gpio_test_interval"]))
    
    t = SelfTest(settings.get()['self_test'])
    t.run()
    
            
            
        
        