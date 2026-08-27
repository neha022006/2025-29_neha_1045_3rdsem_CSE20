import re

password = input("Enter a password: ")

strength = 0

# Check password length
if len(password) >= 8:
    strength += 1

# Check for uppercase letter
if re.search(r"[A-Z]", password):
    strength += 1

# Check for lowercase letter
if re.search(r"[a-z]", password):
    strength += 1

# Check for numbers
if re.search(r"[0-9]", password):
    strength += 1

# Check for special characters
if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
    strength += 1

# Display password strength
if strength <= 2:
    print("Password Strength: Weak")
elif strength <= 4:
    print("Password Strength: Medium")
else:
    print("Password Strength: Strong")