from colorama import init, Fore, Style
from modules.recon import perform_recon
from modules.targeting import perform_targeting

init(autoreset=True)

def rgb_to_ansi(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def print_gradient_text(text):
    lines = text.split('\n')
    total_lines = len(lines)
    
    for i, line in enumerate(lines):
        r = int(255 - (255 * i / (total_lines - 1)))
        g = int(255 * i / (total_lines - 1))
        b = 0
        ansi_code = rgb_to_ansi(r, g, b)
        print(f'{ansi_code}{line}{Style.RESET_ALL}')

ascii_art = """
 ██▀███   ▄▄▄     ▄▄▄█████▓  ██████ 
▓██ ▒ ██▒▒████▄   ▓  ██▒ ▓▒▒██    ▒ 
▓██ ░▄█ ▒▒██  ▀█▄ ▒ ▓██░ ▒░░ ▓██▄   
▒██▀▀█▄  ░██▄▄▄▄██░ ▓██▓ ░   ▒   ██▒
░██▓ ▒██▒ ▓█   ▓██▒ ▒██▒ ░ ▒██████▒▒
░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒ ░░   ▒ ▒▓▒ ▒ ░
  ░▒ ░ ▒░  ▒   ▒▒ ░   ░    ░ ░▒  ░ ░
  ░░   ░   ░   ▒    ░      ░  ░  ░  
   ░           ░  ░              ░  

   By: github.com/SayesCode/RaTs
"""

def display_banner():
    print_gradient_text(ascii_art)
    print(Fore.RED + "\nChoose an option:")
    print(Fore.LIGHTGREEN_EX + "1. Recon")
    print(Fore.LIGHTGREEN_EX + "2. Targeting")
    print(Fore.LIGHTGREEN_EX + "3. Exit")


if __name__ == "__main__":
    while True:
        try:
            display_banner()
            choice = input(Fore.RED + "\nEnter your choice number: ")

            if choice == "1":
                perform_recon()
            elif choice == "2":
                perform_targeting()
            elif choice == "3":
                print(Fore.LIGHTRED_EX + "Exiting...")
                break
            else:
                print(Fore.LIGHTRED_EX + "Invalid choice, try again.")
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\nProgram interrupted. Exiting...")
            break
