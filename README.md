# nanoka-firmware
Firmware for Project Nanoka, written in Python. The essential functionality behind this board is to play WAV sounds when GPIO lines are grounded (through a button, for example) in order to function like a traditional audio board. 

In the future, I plan to make a C++ version of this. 

# Features
1. Seven total GPIO lines exposed through screw terminals (two are reserved for UART)
2. An audio input to use with a microphone or other sources
3. A piezo speaker for notifications (like errors)
4. A custom Linux-like shell environment exposed through the UART pins (I plan to make this optional in the future to free up more lines)
5. A custom file transfer protocol exposed through the console
6. Configurable behaviour (either through the file or through the console)
7. Plays sounds automatically when GPIO lines are grounded. Double-click functionality is supported to have two sounds per line.

# Code Architecture
This code is made to be very modular. Every module has its own scope of functionality which it provides as a class. There is then a main file (code.py) which ties all the modules together by creating the respective objects. If an object must interface with another object, a reference to it is passed through a parameter during creation. 

By convention, objects are instanced in the main file.

1. **audio.py** (audio player and button press detection)
2. **buzzer.py** (manages the piezo speaker)
3. **relay.py** (manages the relay)
4. **settings.py** (provides mechanisms for settings management)
5. **self_test.py** (performs some simple self tests)
6. **console.py** (creates a terminal-like environment on UART)
7. **commands.py** (provides commands to console.py)
8. **uartfile.py** (custom file transfer protocol)

# Settings
There are a series of settings that exist within nanoka_settings.json. These are managed by settings.py and can be set through the uart console or of course, through the file manually. 

The file includes categories of settings for each module. In order, these are:

1. **self_test.py**
     1. relay_hold_time `[int]` — The amount of time (in seconds) that the relay is held in a position.
     2. relay_switch_interval `[int]` — The amount of times the relay is switched during the test. The default of 6 switches relay on three times, and off another three times. 
     3. gpio_test_interval `[int]` — the amount of times each individual GPIO line will be checked. 
     4. gpio_hold_time `[float]` — the amount of time (in seconds) the tester will wait after making a check on the line. The default is 0.01 so it makes rapid checks.
2. **commands.py**
     1. raise_exception_on_command_error `[boolean]` — whether an occured exception during command execution is raised to the **console.py** module. If it isn't, it is skipped.
     2. print_exception_on_console `[boolean]` — whether the backtrace of an excception is printed on the UART console when it occurs.
3. **player.py**
     1. debounce_delay `[float]` — This is the period of time (in seconds) before double-click detection starts to prevent debounce.
     2. double_click_delay `[float]` — This is the detection period of a double click. It starts right after the debounce delay. If a GPIO line isn't grounded during that time, it's considered a single-click.

4. **main.py**:
     1. exit_on_error `[boolean]` — If an exception is caught in the main try-except block, exit to stop all further execution
     2. raise_exceptions `[boolean]` — if the main try-except block catches an exception, raise it. This is mostly useful for debugging.
     3. write_to_uart_on_error `[boolean]` — Print backtraces of caught exceptions on uart, regardless of whether the console is enabled.
     4. beep_on_error `[boolean]` — use the built-in piezo to make a beep when an exception is caught.
     5. skip_startup_self_test `[boolean]` — skip the test within self_test.py on start.

# UART console commands
The console always listens for "enable" to be written to UART. When it is, the console becomes enabled, all event loops are effectively blocked so they are accessible and commandable from this environment, and it beings to prompt the user for commands. 

The console environment behaves as Linux-like shell. When a command is entered, every space-seperated word that comes after it is considered an argument. 

The following commands are available:
1. **help** — provides information about commands
2. **eval** (code) — accepts bare Python code as the first argument and executes it.
3. **echo** — simply writes "echo" back.
4. **set_setting** (*keys, value) — sets value to specified setting. The key argument specifies a category. The asterisk denotes that its possible to specify a series of setting categories (seperated by spaces) instead of just one. The last argument in the command is always considered to be the value.
5. **print_settings** — prints the current settings
6. **mkdir** (path) — makes a directory in the file system.
7. **ls** (path) — lists files in the specified directory
8. **rm** *<-r>* (path) — removes file or directory
9. **cat** (path_to_file) — prints the contents of a file
10. **upload_file** (filename) — uploads a file. This essentially starts the file transfer protocol, which listens on UART for commands. A special client is needed for this, of course. 
11. **beep** (frequency, duty_cycle, duration) — uses the piezo to make a beep
12. **relay** (on/off) — switches relay to the specified state
