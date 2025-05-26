from colorama import Fore, Style, init

def init_color():
    init(autoreset=True)

def print_colored(text, color, no_color=False):
    if no_color:
        print(text)
    else:
        colors = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "cyan": Fore.CYAN
        }
        print(colors.get(color, Fore.WHITE) + Style.BRIGHT + text)