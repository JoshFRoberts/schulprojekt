#!/bin/python3 
from sys import argv

from tests.PumpTest import test_pump_answer 
from tests.MoistureSensorTest import test_sensor_data
from humidity_sender import MoistureMonitoringSystem 
from config import DEBUG_PRINT, FMT_RED, FMT_GREEN, FMT_NONE


def helptext():
    print("\nUsage:")
    print("humidity_handler.py [FLAGS] [OPTIONS]\n")
    print("Available flags:")
    print("  -t          Run tests before execution")
    print("  -d          Run only tests")
    print("  -l          Activate control led")
    print("  -h, --help  Print this help text")
    print("Available options:")
    print("  --mqtt_topic      %TOPIC%       MQTT topic to send to")
    print("  --mqtt_host       %HOST%        Host running MQTT broker")
    print("  --mqtt_port       %PORT%        Port of MQTT service on broker")
    print("  --pump_pin        %GPIO_PIN%    GPIO pin for pump control")
    print("  --pump_return_pin %GPIO_PIN%    GPIO pin for pump observation")
    print("  --spi_bus         %SPI_BUS%     SPI bus number")
    print("  --spi_device      %SPI_DEVICE%  SPI device number")
    print("  --spi_channel     %SPI_CHANNEL% SPI channel number")
    print()

if __name__ == "__main__":
    print("HumidityHandler - WetEarthSociety 2024")
    # Prepare option variables
    apply_tests = False 
    only_tests = False 
    has_led = False
    pump_pin = None 
    pump_return_signal_pin = None 
    spi_bus = None 
    spi_device = None 
    spi_channel = None 
    mqtt_topic = None 
    mqtt_host = None 
    mqtt_port = None 

    # Handle input arguments
    for i, arg in enumerate(argv): 
        # Avoiding match case to keep compatibility with python < 3.10
        if(arg == "-h" or arg == "--help"):
            helptext()
            exit(0)
        if(arg == "-t"):
            apply_tests = True 
        if(arg == "-d"):
            apply_tests = True 
            only_tests = True  
        if(arg == "-l"):
            has_led = True
        if(arg == "--pump_pin"):
            try:
                pump_pin = int(argv[i+1])
            except ValueError: 
                print(f"'{argv[i+1]}' ist kein gültiger Wert für den Steuerungspin der Pumpe.")
                exit(1)
        if(arg == "--pump_return_pin"):
            try: 
                pump_return_signal_pin = int(argv[i+1])
            except ValueError:
                print("f'{argv[i+1]}' ist kein gültiger Wert für den Prüfpin der Pumpe.")
                exit(1)
        if(arg == "--spi_bus"):
            try:
                spi_bus = int(argv[i+1])
            except ValueError: 
                print(f"'{argv[i+1]}' ist kein gültiger Wert für den SPI Bus.")
                exit(1)
        if(arg == "--spi_device"):
            try:
                spi_device = int(argv[i+1])
            except ValueError: 
                print(f"'{argv[i+1]}' ist kein gültiger Wert für den Steuerungspin der Pumpe.")
                exit(1)
        if(arg == "--spi_channel"):
            try:
                spi_channel = int(argv[i+1])
            except ValueError:
                print(f"'{argv[i+1]}' ist kein gültiger Wert für den SPI-Kanal")
                exit(1)
        if(arg == "--mqtt_host"):
            mqtt_host = argv[i+1]
        if(arg == "--mqtt_topic"):
            mqtt_topic = argv[i+1]
        if(arg == "--mqtt_port"):
            try:
                spi_channel = int(argv[i+1])
            except ValueError:
                print(f"'{argv[i+1]}' ist kein gültiger Wert für den MQTT Port")
                exit(1)


        

    # Run tests
    if(apply_tests):
        print("Initialisiere Tests für Hydrationseinheit")

        print("\n===== Feuchigkeitssensor =====") 
        print("Status Feuchtigkeitssensor: ", end="")
        if(test_sensor_data(spi_bus, spi_device, spi_channel)):
            print(f"[  {FMT_GREEN}OK{FMT_NONE}  ]")
        else:
            print(f"[{FMT_RED}FEHLER{FMT_NONE}]")
        
        print("\n====== Pumpensteuerung =======")
        status_pumpe = test_pump_answer(pump_pin, pump_return_signal_pin)
        print("Status Pumpensteuerung: ", end="")
        if(status_pumpe): 
            print(f"[  {FMT_GREEN}OK{FMT_NONE}  ]")
        else:
            print(f"[{FMT_RED}FEHLER{FMT_NONE}]")
        
        print("\n")

    # Execute application
    if(only_tests == False):
        print("Starte Feuchtigkeitsmessung")
        MoistureMonitoringSystem(
            has_led=has_led, 
            mqtt_host=mqtt_host, 
            mqtt_port=mqtt_port, 
            mqtt_topic=mqtt_topic, 
            spi_bus=spi_bus, 
            spi_device=spi_device,
            pump_pin=pump_pin,
            pump_observe_pin=pump_return_signal_pin            
        ).run()
