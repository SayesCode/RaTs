from colorama import init, Fore, Style
from modules.recon import perform_recon
from modules.targeting import perform_targeting
from dotenv import load_dotenv
import os

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

def validate_env_keys():
    """
    Checks if the required API keys are present in the .env file and valid.
    Allows the user to manually add keys if they are missing.
    """
    required_keys = {
        "NUMVERIFY_API_KEY": "https://numverify.com - Get a free API key for phone number validation.",
        "HUNTER_API_KEY": "https://hunter.io - Get a free API key for email verification."
    }

    load_dotenv()  # Load environment variables from .env
    missing_keys = []

    for key, help_text in required_keys.items():
        value = os.getenv(key)
        if not value or value.strip() == "":
            print(Fore.YELLOW + f"\nThe key {key} is missing or invalid.")
            print(Fore.CYAN + f"To obtain it, visit: {help_text}")
            missing_keys.append(key)

    if missing_keys:
        print(Fore.LIGHTMAGENTA_EX + "\nWould you like to add the missing keys now?")
        add_now = input(Fore.LIGHTGREEN_EX + "Type 'y' to add or any other key to exit: ").lower()
        if add_now == 'y':
            with open('.env', 'a') as env_file:
                for key in missing_keys:
                    new_value = input(Fore.LIGHTBLUE_EX + f"Enter the key for {key}: ").strip()
                    env_file.write(f"\n{key}={new_value}")
            print(Fore.LIGHTGREEN_EX + "\nKeys have been added to the .env file. Restart the program to apply changes.")
            exit()
        else:
            print(Fore.LIGHTRED_EX + "Exiting. Please add the keys manually to the .env file and restart the program.")
            exit()

if __name__ == "__main__":
    # Validate keys before displaying the menu
    validate_env_keys()

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
