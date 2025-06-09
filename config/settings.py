import json
import os

CONFIG_PATH = os.path.expanduser("~/.md2word_config.json")

DEFAULTS = {
    "last_input_dir": "",
    "last_output_dir": "",
    "theme": "light",
    "last_format": "Word (.docx)"
}

def load_settings():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in DEFAULTS.items():
                if k not in data:
                    data[k] = v
            return data
        except Exception:
            return DEFAULTS.copy()
    else:
        return DEFAULTS.copy()

def save_settings(settings: dict):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
