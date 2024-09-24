import subprocess
import re

def get_wifi_profiles():
    """Fetch all Wi-Fi profiles stored on the computer."""
    try:
        # Run the command to get the list of Wi-Fi profiles
        data = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8").splitlines()
        
        # Extract the profile names from the output
        profiles = [line.split(":")[1][1:-1] for line in data if "All User Profile" in line]
        return profiles
    except subprocess.CalledProcessError as e:
        print("Error fetching Wi-Fi profiles:", e)
        return []

def get_wifi_password(profile):
    """Fetch the password for a given Wi-Fi profile."""
    try:
        # Run the command to get the details of the Wi-Fi profile
        results = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode("utf-8").splitlines()
        
        # Search for the line containing the key content (password)
        for line in results:
            if "Key Content" in line:
                return line.split(":")[1][1:-1]  # Return the password
        return None  # No password found
    except subprocess.CalledProcessError as e:
        print(f"Error fetching password for {profile}: {e}")
        return None

def display_wifi_passwords():
    """Display all Wi-Fi profiles and their passwords."""
    profiles = get_wifi_profiles()
    
    # Check if profiles were found
    if not profiles:
        print("No Wi-Fi profiles found.")
        return
    
    print("{:<30} | {:<}".format("Profile Name", "Password"))
    print("-" * 50)

    # Iterate through profiles and get passwords
    for profile in profiles:
        password = get_wifi_password(profile)
        if password:
            print("{:<30} | {:<}".format(profile, password))
        else:
            print("{:<30} | {:<}".format(profile, "No password found"))

if __name__ == "__main__":
    display_wifi_passwords()
