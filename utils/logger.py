import datetime
import os

class Logger:
    def __init__(self):
        self.logs = []

    def log(self, msg, level="INFO"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{now}] [{level}] {msg}"
        self.logs.append(line)
        print(line)  # 控制台输出

    def info(self, msg):
        self.log(msg, "INFO")

    def warning(self, msg):
        self.log(msg, "WARNING")

    def error(self, msg):
        self.log(msg, "ERROR")

    def export(self, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.logs))
            return True
        except Exception:
            return False 