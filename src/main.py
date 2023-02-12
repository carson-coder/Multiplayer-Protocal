
#
# AOSMP (A Open-Souce Multiplayer Protocal)
# Version 
# 
# 



import sys, json
import logging
import colorama

open_text = colorama.Style.BRIGHT + colorama.Fore.CYAN + f"""    _   ___  ___ __  __ ___ 
   /_\ / _ \/ __|  \/  | _ \\
  / _ \ (_) \__ \ |\/| |  _/
 /_/ \_\___/|___/_|  |_|_| {colorama.Fore.GREEN}  (A Open-Source Multiplayer Protocal)
 """ + colorama.Style.RESET_ALL

print(open_text)

# Logging INIT

FORMAT = "[{levelname:^7}] {name}.{threadName}.{module}.{funcName}.{lineno}: {message}"
FORMAT = "{asctime} [{threadName}] |{levelname}| in {filename}/{module}/{funcName} Line {lineno}: {message}"
FORMATS = {
    logging.DEBUG: colorama.Fore.BLUE + colorama.Style.BRIGHT + FORMAT + colorama.Style.RESET_ALL,
    logging.INFO:  colorama.Fore.GREEN + colorama.Style.BRIGHT + FORMAT + colorama.Style.RESET_ALL,
    logging.WARNING: colorama.Fore.YELLOW + colorama.Style.BRIGHT + FORMAT + colorama.Style.RESET_ALL,
    logging.ERROR: colorama.Fore.RED + colorama.Style.BRIGHT + FORMAT + colorama.Style.RESET_ALL,
    logging.CRITICAL: colorama.Back.RED + colorama.Fore.WHITE + colorama.Style.BRIGHT + FORMAT + colorama.Style.RESET_ALL,
}

class Format(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        #a = record.levelname+(" "*(9-len(record.levelname)))
        #log_fmt = log_fmt.replace("{levelname}", a)
        if record.funcName == "<module>":
            # record.funcName = "global"
            log_fmt = log_fmt.replace("/{funcName}", "")
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)
    
handler = logging.StreamHandler()
handler.setFormatter(Format())


# Desc:
# Launch A server or client
# 
# Args :
#  -s Server
#  -c Client
#  -l Output Level
#  -h Help
#  -p Port
#  -cf Config File
#

PORT = 1853

# Handle Arguments
server = "-s" in sys.argv
client = "-c" in sys.argv
debug_set = "-l" in sys.argv
help = "-h" in sys.argv
port_set = "-p" in sys.argv
config_set = "-cf" in sys.argv

if help or len(sys.argv) < 2:
    print(colorama.Fore.LIGHTMAGENTA_EX + colorama.Style.BRIGHT + f"""    Arguments:
          \u001b[4m Flag \u001b[0m {colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX}               |\u001b[4m Desc \u001b[0m {colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX}
        |-> -c                  | Run as client
        |-> -s                  | Run as server
        |-> -l (LEVEL)          | Debug level. Default is 1 (INFO)
        |-> -h                  | Show this message
        |-> -p (PORT)           | Port to run on or listen on. Default is port 1853
        |-> -cf (/path/to/file) | Config file to load.

    Debug Levels:
         \u001b[4m Id | Name \u001b[0m {colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX}    |\u001b[4m Desc \u001b[0m {colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX}
        |->0 | Debug.    | Everything
        |->1 | Info.     | Alot of stuff but not everything
        |->2 | Warning.  | Non important errors.
        |->3 | Error.    | Errors that program can still run but might skip somethings.
        |->4 | Critical. | Errors that cause the program to exit. DO NOT SET AS DEBUG LEVEL UNLESS PRODUCTION or do but its not recomended.
    """ + colorama.Style.RESET_ALL)
    exit(0)

if debug_set:
    debug_level = sys.argv[sys.argv.index("-l") + 1]
    if debug_level in ["0","1","2","3","4"]:
        logging.basicConfig(
            level = (int(debug_level) + 1) * 10,
            handlers=[handler]
        )
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        print(f"Debug Level {debug_level} ({levels[int(debug_level)]})")
    else:
        logging.basicConfig(
            level = logging.INFO,
            handlers=[handler]
        )
        logging.error(f"Invalid Debug Level {debug_level}. Defaulting to 1 (INFO)")
else: 
    logging.basicConfig(
        level = logging.INFO,
        handlers=[handler]
    )
if server and client: 
    logging.critical("Cannot run as client and as server. Remove -s or -c flag to fix")
    exit(1)

if not (server or client):
    logging.critical("Please provide -c or -s flag. Use -h flag for help")
    exit(1)

# 
# Now we are ether launching a server or conencting as a client
#  

