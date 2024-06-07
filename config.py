#
# General 
#
# Output settings
DEBUG_PRINT = True
# ANSI-escape sequences for basic color formatting of stdout 
FMT_RED     = "\033[0;31m"
FMT_GREEN   = "\033[0;32m"
FMT_NONE    = "\033[0m"

#
# Application configuration
#
MOIST_THRESHOLD     = 100       # Moist level for activation of pump 
# SPI Config 
DEFAULT_SPI_BUS     = 0 
DEFAULT_SPI_DEVICE  = 0 
DEFAULT_SPI_FREQ    = 100000
# Pump pins 
DEFAULT_PIN_PUMP    = 21
DEFAULT_PIN_PUMP_OBSERVE    = 20
# MQTT settings 
DEFAULT_BROKER      = "localhost"
DEFAULT_PORT        = 1883
DEFAULT_TOPIC       = "humantiddy"
# LED Output config 
DEFAULT_PIN_RED     = 6
DEFAULT_PIN_GREEN   = 19
DEFAULT_PIN_BLUE    = 13 
THRESHOLD_RED       = 50
THRESHOLD_YELLOW    = 100
THRESHOLD_GREEN     = 150
