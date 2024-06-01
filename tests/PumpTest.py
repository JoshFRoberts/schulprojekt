import RPi.GPIO as GPIO

from humidity_sender import PumpController

def test_pump_answer(pump_pin=21, return_signal_pin=20):

    print("Ziehen sie die Pumpenpins vom Board pls.")
    input("Drücken sie dann die ENTER Taste")

    pump = PumpController(pump_pin, return_signal_pin)
    signalPin = lambda: GPIO.input(pump.return_signal_pin)

    for moist_level in range(0, 250):
        pump.control(moist_level)
        if GPIO.input(pump.return_signal_pin):
            print(f"Pumpe Läuft bei moist = {moist_level}")
        elif moist_level >= 100 and not signalPin():
            return False
    return True