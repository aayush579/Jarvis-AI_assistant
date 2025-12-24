import platform, subprocess

def run(arg: str, cfg: dict) -> str:
    cmd = (arg or "notepad").lower()
    if platform.system() == "Windows":
        if cmd == "notepad":
            subprocess.Popen(["notepad"])
            return "Opened Notepad."
        if cmd == "calc":
            subprocess.Popen(["calc"])
            return "Opened Calculator."
    return "System control: specify 'notepad' or 'calc' on Windows."
