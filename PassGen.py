import random
import string
import re
import time
import click
from colorama import init, Fore
import subprocess

# Initialize Colorama for colored output
init(autoreset=True)

# Constants for character sets
UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SPECIAL_CHARS = string.punctuation

# Password history to prevent reuse
password_history = set()

def colored_print(text, color=Fore.RESET):
    click.echo(color + text)

def animate_input_prompt(prompt_text):
    while True:
        user_input = click.prompt(prompt_text, err=True).strip()
        if user_input:
            return user_input

def generate_password(
    length=12,
    use_uppercase=True,
    use_lowercase=True,
    use_digits=True,
    use_special_chars=True,
    avoid_similar_chars=True,
):
    # Define character sets based on user preferences
    chars = ""
    if use_uppercase:
        chars += UPPERCASE
    if use_lowercase:
        chars += LOWERCASE
    if use_digits:
        chars += DIGITS
    if use_special_chars:
        chars += SPECIAL_CHARS

    # Check if at least one character set is selected
    if not chars:
        return colored_print("Please select at least one character set.", Fore.RED)

    while True:
        # Generate the password
        password = ''.join(random.choice(chars) for _ in range(length))

        # Check if password meets strength criteria
        if is_strong_password(password, avoid_similar_chars):
            if password not in password_history:
                password_history.add(password)
                return password

def is_strong_password(password, avoid_similar_chars=True):
    # Check password strength based on criteria such as length, character sets, etc.
    if len(password) < 8:
        return False

    if avoid_similar_chars and re.search(r'([il1Lo0])', password):
        return False

    return any(char in UPPERCASE for char in password) \
        and any(char in LOWERCASE for char in password) \
        and any(char in DIGITS for char in password) \
        and any(char in SPECIAL_CHARS for char in password)

def save_password_to_file(password, filename="passwords.txt"):
    with open(filename, "a") as file:
        file.write(password + "\n")

def loading_spinner(seconds=3):
    spinner = "/-\\|"
    for _ in range(seconds * 10):
        time.sleep(0.1)
        click.echo(f"\rGenerating Password... {spinner[_ % 4]}", nl=False, color=Fore.CYAN, err=True)

def animate_save_message():
    message = "Saving password to passwords.txt"
    for _ in range(2):
        for i in range(1, len(message) + 1):
            time.sleep(0.05)  # Adjust the duration for the desired speed
            click.echo(f"\r{message[:i]}", nl=False, err=True, color=Fore.YELLOW)
        click.echo(" " * len(message), nl=False, err=True)  # Clear the line
        time.sleep(0.3)  # Add a delay for the loading spinner effect
        click.echo(f"\rSaving password to passwords.txt...   ", nl=False, err=True, color=Fore.YELLOW)
        time.sleep(0.3)  # Add a delay for the loading spinner effect
    click.echo(f"\rPassword saved to passwords.txt               ", nl=False, err=True, color=Fore.YELLOW)  # Clear the line

def animate_generating_password_text():
    text = "Generating a New Password"
    for _ in range(1):  # Repeat the animation a few times
        for i in range(len(text)):
            animated_text = f"{Fore.CYAN}{text[:i]}{Fore.RESET}.{text[i + 1:]}"  # Add color and dot animation effect
            click.echo(f"\r{animated_text}", nl=False, err=True)
            time.sleep(0.1)  # Adjust the duration for the desired speed
        time.sleep(0.3)  # Add a pause before the next animation cycle
        
        
def fade_in_text(text, duration=0.05):
    for i in range(1, len(text) + 1):
        time.sleep(duration)
        click.echo(f"\r{text[:i]}", nl=False, err=True, color=Fore.CYAN)
    click.echo(" " * len(text), nl=False, err=True)  # Clear the line

def generate_and_save_password():
    animate_generating_password_text()  # Animate "Generating a New Password" text

    length = int(animate_input_prompt("\nEnter the desired password length: "))
    use_uppercase = animate_input_prompt("Include uppercase letters (Y/N)? ").strip().lower() == 'y'
    use_lowercase = animate_input_prompt("Include lowercase letters (Y/N)? ").strip().lower() == 'y'
    use_digits = animate_input_prompt("Include digits (Y/N)? ").strip().lower() == 'y'
    use_special_chars = animate_input_prompt("Include special characters (Y/N)? ").strip().lower() == 'y'
    avoid_similar_chars = animate_input_prompt("Avoid similar characters (Y/N)? ").strip().lower() == 'y'

    fade_in_text("Generating Password...")

    loading_spinner()
    password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special_chars, avoid_similar_chars)
    colored_print(f"Generated Password: {password}", Fore.GREEN)

    save_option = animate_input_prompt("Do you want to save this password to a file (Y/N)? ").strip().lower() == 'y'
    if save_option:
        animate_save_message()  # Add the animation for saving the password
        save_password_to_file(password)

def main():
    subprocess.run(["clear"])  # Clear the terminal screen

    colored_print(f"""
     ____                ____            
    |  _ \ __ _ ___ ___ / ___| ___ _ __  
    | |_) / _` / __/ __| |  _ / _ \ '_ \ 
    |  __/ (_| \__ \__ \ |_| |  __/ | | |
    |_|   \__,_|___/___/\____|\___|_| |_|
                                      
Welcome to the Advanced Password Generator!
""", Fore.YELLOW)

    while True:
        generate_and_save_password()
        another_password = animate_input_prompt("\n\nDo you want to create another password (Y/N)? ").strip().lower() == 'y'
        if not another_password:
            break

if __name__ == "__main__":
    main()
