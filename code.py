import audio
import relay
import console
import commands
import buzzer
import time
import json
import busio
import board
import config
import self_test
import sys
import traceback

settings = config.Settings()
settings.load()
my_settings = settings.get()['main']

if not my_settings["skip_startup_self_test"]:
    tester = self_test.SelfTest(settings.get()["self_test"])
    tester.run()
    tester.deinit()

uart = busio.UART(tx=board.GP12, rx=board.GP1, baudrate=57600, timeout=0.1)

try:
    relay_controller = relay.RelayControl()
    beeper = buzzer.Buzzer()
    cmds = commands.Commands(beeper, relay_controller, uart, settings)
    cli = console.Console(cmds, uart)
    player = audio.AudioPlayer(settings.get()["player"], relay_controller)

    while True:
        player.poll()
        cli.poll()       
except Exception as e:
    if my_settings["write_to_uart_on_error"]:
        uart.write("\r\n")
        uart.write("".join(traceback.format_exception(type(e), e, e.__traceback__)).encode())
        
    if my_settings["beep_on_error"]:
        beeper.buzz()
    
    if my_settings["raise_exceptions"]:
        raise e
    
    if my_settings['exit_on_error']:
        sys.exit()
