import RPi.GPIO as GPIO
from os import path as os_path 
from sys import path as sys_path
sys_path.append(os_path.abspath(os_path.join(os_path.dirname(__file__), '..')))

from humidity_sender import PumpController
from config import DEBUG_PRINT, FMT_RED, FMT_GREEN, FMT_NONE, MOIST_THRESHOLD

TEST_RANGE_LOWER = 0
TEST_RANGE_UPPER = 250 

def test_pump_answer(pump_pin=None, return_signal_pin=None):
    # Initialize input values 
    pump_pin = pump_pin if not pump_pin is None else 21
    return_signal_pin = return_signal_pin if not return_signal_pin is None else 20
    # Prepare gpio 
    GPIO.setmode(GPIO.BCM)
    # Define processing variables
    result_success = True 
    signalPin = lambda: GPIO.input(pump.return_signal_pin)
    # Prompt user for physical setup
    print("Ziehen sie die Pumpenpins vom Board pls.")
    input("Drücken sie dann die ENTER Taste")
    pump = PumpController(pump_pin, return_signal_pin)

    if DEBUG_PRINT: 
        print(f"Prüfe Pumpe für moist_level im Bereich von {TEST_RANGE_LOWER} bis {TEST_RANGE_UPPER}")

    for moist_level in range(TEST_RANGE_LOWER, TEST_RANGE_UPPER):
        pump.control(moist_level)
        
        if DEBUG_PRINT: 
            print(f"Pumpe {'aktiviert' if signalPin() else 'deaktiviert'} bei moist_level={moist_level}")
        
        # Test case for unexpected input when moist_level is already high enough
        if moist_level > MOIST_THRESHOLD and signalPin():
            # Print error only once, unless DEBUG_PRINT is set
            if result_success or DEBUG_PRINT:
                print(f"{FMT_RED}FEHLER{FMT_NONE}: Unerwarteter Signaleingang an Pumpensteuerung für moist_level={moist_level}. Erwarte: 0")
                result_success = False 
        
        # Test case for missing input when most_level is too low 
        if moist_level <= MOIST_THRESHOLD and not signalPin():
            # Print error only once, unless DEBUG_PRINT is set
            if result_success or DEBUG_PRINT:
                print(f"{FMT_RED}FEHLER{FMT_NONE}: Fehlender Signaleingang an Pumpensteuerung für moist_level={moist_level}. Erwarte: 1")
                result_success = False 
            
    # Prevent multiple usage when script is executet after tests 
    GPIO.cleanup()
    return result_success       
