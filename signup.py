#!/usr/bin/env python3
"""XYZ Company sign-up checks.

Each field is accepted only when the entire value matches that field's
pattern. Characters outside the pattern, including SQL and command
metacharacters, are rejected. Input is not stripped and is not passed
to a database or a shell.

The website in server.py and the terminal form below use these checks.
"""

import re
import sys

# ASCII ranges only. \d is not used, so Unicode digits cannot slip through.
FIRST_NAME_RE = re.compile(r"^[A-Z][a-z]+$")
EMAIL_RE = re.compile(
    r"^[A-Za-z0-9]+(?:[._%+-][A-Za-z0-9]+)*"
    r"@[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
    r"(?:\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)*"
    r"\.[A-Za-z]{2,}$"
)
# Area code is [2-9][0-9]{2}. The rest is exactly "(###) ###-####".
PHONE_RE = re.compile(r"^\([2-9][0-9]{2}\) [0-9]{3}-[0-9]{4}$")
POSTAL_RE = re.compile(r"^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$")


def validate_first_name(value):
    if FIRST_NAME_RE.fullmatch(value):
        return None
    return (
        "First Name must contain letters only and begin with one capital "
        "letter (example: John)."
    )


def validate_email(value):
    if EMAIL_RE.fullmatch(value):
        return None
    return "Email Address must be a standard address (example: john@example.com)."


def validate_phone(value):
    if PHONE_RE.fullmatch(value):
        return None
    return (
        "Telephone Number must be a Canadian number in the form (416) 555-1234. "
        "The area code cannot start with 0 or 1."
    )


def validate_postal(value):
    if POSTAL_RE.fullmatch(value):
        return None
    return "Postal Code must match the Canadian format A1A 1A1 (example: M5V 3A8)."


def validate_fields(first_name, email, phone, postal):
    """Return (field name, message) pairs for every value that does not match."""
    named = (
        ("first_name", validate_first_name(first_name)),
        ("email", validate_email(email)),
        ("phone", validate_phone(phone)),
        ("postal", validate_postal(postal)),
    )
    return [(name, message) for name, message in named if message]


def collect_inputs():
    """Read the four raw lines. Spaces are kept and checked by the patterns."""
    labels = (
        "First Name",
        "Email Address",
        "Telephone Number",
        "Postal Code",
    )
    values = []
    for label in labels:
        try:
            values.append(input(f"{label}: "))
        except EOFError:
            print("Registration failed.")
            print("- Input ended before every field was entered.")
            return None
    return values


def main():
    values = collect_inputs()
    if values is None:
        return 1

    errors = validate_fields(*values)
    if errors:
        print("Registration failed.")
        for _name, message in errors:
            print(f"- {message}")
        return 1

    print("Sign-Up Completed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
