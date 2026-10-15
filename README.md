# CST8808 Take-Home Quiz: Sign-Up Form Validation

XYZ Company registration form. The program asks for a first name, an email address, a Canadian telephone number, and a Canadian postal code. It accepts the registration only when every value matches the format for that field.

The checks reject unexpected characters. A value that contains SQL-injection or command-injection text fails because it does not match the field format. The program does not search for words such as SELECT or DROP.

## Files

Keep these files in the same folder.

| File | Purpose |
|---|---|
| start.bat | Windows only. Double-click this file to open the website. |
| README.md | These instructions |
| server.py | The website |
| signup.py | The validation rules. The website uses this file. |

No other packages are required. The programs use the Python 3 standard library.

Python may create a folder named `__pycache__` after a run. That folder is not part of the submission.

The folder can sit anywhere on the computer. `start.bat`, `server.py`, and `signup.py` must stay together in that folder.

The website runs only on the computer where it was started. Other computers cannot open it. The page address is:

http://127.0.0.1:8765

## Run the website on Windows

1. If Python 3 is not installed, download it from https://www.python.org/downloads/windows/ . On the first screen of the installer, check **Add python.exe to PATH**, then finish the install.
2. Open the quiz folder.
3. Double-click **start.bat**.
4. The sign-up page opens in the browser. Fill in the four fields and click **Create account**.

Leave the black window open while you use the page. Close that window when you are finished. Closing it stops the website.

If the browser does not open by itself, open Microsoft Edge and go to http://127.0.0.1:8765

If start.bat says Python was not found, install Python as described in step 1, then double-click start.bat again.

## Run the website on macOS

`start.bat` does not start the website on a Mac. Use Terminal instead.

1. If Python 3 is not installed, download it from https://www.python.org/downloads/macos/ and finish the install.
2. Open the Terminal app.
3. Type `cd` and then a space. Do not press Return yet.
4. Drag the quiz folder onto the Terminal window. The folder path appears after `cd`.
5. Press Return.
6. Type this command and press Return:

    python3 server.py

7. Leave the Terminal window open. When it prints `XYZ Company sign-up: http://127.0.0.1:8765`, open Safari and go to that address.
8. Fill in the four fields and click **Create account**.
9. To stop the website, click the Terminal window and press Control-C.

If Terminal says that python3 was not found, install Python as described in step 1, then repeat from step 2.

## Accepted format

The program checks the text exactly as entered. It does not remove spaces. A leading space, a trailing space, or a missing character makes the field invalid.

| Field | Required format | Accepted example |
|---|---|---|
| First Name | One uppercase letter, then one or more lowercase letters. No spaces, digits, hyphens, or accents. | John |
| Email Address | A normal address: letters, digits, and the characters . _ % + - in the name, then @, then a domain whose ending is at least two letters. | john@example.com |
| Telephone Number | Exactly (###) ###-####. The area code cannot start with 0 or 1. The brackets, space, and hyphen are required. | (416) 555-1234 |
| Postal Code | Uppercase letter, digit, uppercase letter, one space, digit, uppercase letter, digit. | M5V 3A8 |

## Result

- All four fields match: the program displays **Sign-Up Completed!**
- Any field does not match: the program displays **Registration failed.** and one message for each failed field. The registration does not complete. On the website, the entered values stay on the form so they can be corrected.

## Values that should be accepted

| First Name | Email Address | Telephone Number | Postal Code |
|---|---|---|---|
| John | john@example.com | (416) 555-1234 | M5V 3A8 |
| Mary | mary.ann+quiz@mail.example.co.uk | (613) 555-0100 | K1A 0B1 |

## Values that should be rejected

Each row below changes one field. The other three fields can be the accepted John example. The registration must not complete.

| Field entered | Why it is rejected |
|---|---|
| john | The first name must begin with an uppercase letter. |
| John1 | The first name must contain letters only. |
| John'; DROP TABLE users;-- | Quotes, spaces, and punctuation are not allowed in the first name. |
| john.example.com | The email has no @. |
| john@example.com; rm -rf / | The email contains characters that are not part of an email address. |
| 416-555-1234 | The telephone number is not in the form (416) 555-1234. |
| (016) 555-1234 | The area code starts with 0. |
| (416) 555-1234 && whoami | Extra characters follow the telephone number. |
| M5V3A8 | The postal code is missing the required space. |
| m5v 3a8 | Postal code letters must be uppercase. |
| M5V 3A8' OR '1'='1 | Extra characters follow the postal code. |

## How the checks work

Each field is accepted only when the entire value matches that field's pattern. Characters outside the pattern are rejected. This includes quotes, semicolons, pipes, and other symbols used in SQL injection and command injection.

The entered text is not sent to a database or to a command shell. On the website, any text placed back on the page is escaped, so it is shown as text and is not treated as page code.
