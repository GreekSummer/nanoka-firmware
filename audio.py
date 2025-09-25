import board
import digitalio
import audiomp3
import audiopwmio
from audiocore import WaveFile
import time
import relay
import os

class AudioPlayer():
    def __init__(self, settings, relay_object):
        assert(isinstance(relay_object, relay.RelayControl), "Wrong object type passed")
        
        self.sounds_directory = "sounds/"
        self.relay = relay_object
        self.debounce_delay = settings["debounce_delay"]
        self.double_click_delay = settings["double_click_delay"]
        
        #Maps physical board pins to sound files
        self.sound_map = {
            board.GP5: "1.wav",
            board.GP6: "2.wav",
            board.GP8: "3.wav"
            }
        
        #Maps physical board pins to DigitalIO objects so we can interact with them
        self.button_map = {}
        for gpio in self.sound_map:
            
            io_obj = digitalio.DigitalInOut(gpio)
            io_obj.direction = digitalio.Direction.INPUT
            io_obj.pull = digitalio.Pull.UP
 
            self.button_map[gpio] = io_obj
            
        self.audio = audiopwmio.PWMAudioOut(board.GP27)
        self.mp3 = None
    
    def play_wav(self, filename):
        f = open(filename, "rb")
        wave = WaveFile(f)

        self.relay.switch(True)
        self.audio.play(wave)
        
    def poll(self):
        for gpio in self.sound_map:
            double_click = False
            io_obj = self.button_map[gpio]
            
            if not io_obj.value and not self.audio.playing:
                time.sleep(self.debounce_delay)
                start = time.monotonic()
                while (time.monotonic() - start) < self.double_click_delay:
                    if not io_obj.value: #We say not because it goes low when pressed
                        double_click = True
                
                if double_click:
                    filename = self.sounds_directory + "d_" + self.sound_map[gpio]
                else:
                    filename = self.sounds_directory + self.sound_map[gpio]
                    
                try:
                    self.play_wav(filename)
                except Exception as e:
                    print("e: " + str(e))
        
        if not self.audio.playing:
            self.relay.switch(False)
            
