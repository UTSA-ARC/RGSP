import RPi.GPIO as gpio
import threading
import queue
from time import sleep

from config import *
from commands import *

gpio.setmode(gpio.BOARD)

for pin in PINS: # Iterate through relay pins and make each an output
    gpio.setup(pin.value, gpio.OUT)

try:
    cmd_actions: dict[str, Any] = COMMANDS
    cmd_queue: queue.Queue = queue.Queue()
    stdout_lock: threading.Lock = threading.Lock()

    input_thread = threading.Thread(target=console, args=(cmd_queue, stdout_lock))
    print('Press enter for Input Mode\n')
    input_thread.start()

    while 1: # Main Loop
        cmd = cmd_queue.get()
        if cmd == 'quit':
            break
            
        action = cmd_actions.get(cmd, invalid_input)
        action(stdout_lock)
        
        if cmd == 'start gox' and AutoIgniterOpen:
            sleep( IgniteDelay )
            cmd = 'ignite'
            action = cmd_actions.get(cmd, invalid_input)
            action(stdout_lock)
        
        if cmd == 'ignite' and AutoGOXClose:
            sleep( GOXCloseDelay )
            cmd = 'stop gox'
            action = cmd_actions.get(cmd, invalid_input)
            action(stdout_lock)
        
        if cmd == 'stop gox' and AutoIgniterClose:
            cmd = 'stop ignition'
            action = cmd_actions.get(cmd, invalid_input)
            action(stdout_lock)
        
        print('\nPress Enter for Input Mode\n')

except KeyboardInterrupt:
    print('\nCleaning up...\n')
    gpio.cleanup()
