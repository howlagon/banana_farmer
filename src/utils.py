from time import sleep

def block(time: float = 0.5) -> None:
    sleep(time)

def strftime(time: float) -> str:
    days = int(time // 86400)
    hours = int(time // 3600)
    minutes = int((time % 3600) // 60)
    seconds = int(time % 60)
    string = ""
    if days > 0:
        string += f"{days}d "
    string += f"{hours:02}:{minutes:02}:{seconds:02}"
    return string