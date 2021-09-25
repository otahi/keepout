from pathlib import Path
import os
import json

APP_DIR = os.getenv('APPDATA')
CONFIG_PATH = Path(APP_DIR, 'keepout')
CONFIG_FILE = Path(CONFIG_PATH, 'keepout.json')

DEFAULT_CONFIG = {
    "password" : "password",
    "soft" : {
        "start" : "22:50",
        "end"   : "03:10",
        "message" : "It's almost 23:00.",
    },
    "hard" : {
        "start" : "23:00",
        "end"   : "03:00",
        "message" : "It's already 23:00.",
    },
}

def get_config() -> dict:
    if Path(CONFIG_FILE).is_file():
        with open(CONFIG_FILE,"r",encoding = 'utf-8') as f:
            try:
                conf = DEFAULT_CONFIG | json.load(f)
                return conf
            except:
                pass
    else:
        os.makedirs(CONFIG_PATH, exist_ok=True)
        Path(CONFIG_FILE).touch()
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

        # First execution, just create the config file and exit
        exit()

    return DEFAULT_CONFIG
