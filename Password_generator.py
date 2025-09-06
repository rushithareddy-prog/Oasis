import secrets
import string
import sys

# Generate a secure random password containing letters, digits, and symbols
def generate_password(length: int = 12) -> str:
    MIN_LENGTH = 8
    if length < MIN_LENGTH:
        raise ValueError(f"Password length must be at least {MIN_LENGTH} characters.")

    charset = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = ''.join(secrets.choice(charset) for _ in range(length))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

# Prompt user for desired password length with validation and fallback to default
def request_length(default: int = 12) -> int:
    prompt = f"Enter desired password length (default={default}): "
    user_input = input(prompt).strip()
    if not user_input:
        return default
    try:
        length = int(user_input)
        if length < 1:
            raise ValueError("Password length must be positive.")
        return length
    except ValueError:
        print(f"⚠ Invalid input. Falling back to default length: {default}", file=sys.stderr)
        return default

# Main program logic
def main() -> None:
    length = request_length()
    try:
        password = generate_password(length)
    except Exception as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"✅ Generated password: {password}")

# Ensure main runs only when script is executed directly
if __name__ == "__main__":
    main()
