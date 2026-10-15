# CST8808 Take-Home Quiz: Sign-Up Form Validation

XYZ Company registration form. The program asks for a first name, an email address, a Canadian telephone number, and a Canadian postal code. It accepts the registration only when every value matches the format for that field.

The checks reject unexpected characters. A value that contains SQL-injection or command-injection text fails because it does not match the field format. The program does not search for words such as SELECT or DROP.

## Files

These three files must stay in the same folder.

| File | Purpose |
|---|---|
| README.md | These instructions |
| server.py | The website. Use this file for marking. |
| signup.py | The validation rules. The website uses this file. It can also be run on its own. |

No other packages are required. Both programs use the Python 3 standard library.

Python may create a folder named `__pycache__` after a run. That folder is not part of the submission.

## Run the website on Windows

Use Command Prompt. The steps below do not use Windows PowerShell.

1. Install Python 3 if it is not already installed. Download it from https://www.python.org/downloads/windows/ and run the installer. On the first installer screen, turn on **Add python.exe to PATH**, then click Install Now.
2. Open File Explorer and open the folder that contains `README.md`, `server.py`, and `signup.py`.
3. Click the address bar at the top of that folder window. The folder path becomes highlighted.
4. Type `cmd` and press Enter. A Command Prompt window opens in this folder. Its title should show the folder path.
5. In that Command Prompt window, type this command and press Enter:

    python server.py

6. Leave the Command Prompt window open. When the server is ready, it prints this line:

    XYZ Company sign-up: http://127.0.0.1:8765

7. Open Microsoft Edge or another web browser.
8. Click the address bar, type the address below, and press Enter:

    http://127.0.0.1:8765

9. The XYZ Company sign-up page opens. Fill in the four fields and click **Create account**.
10. To stop the website, click the Command Prompt window and press Ctrl+C. If Windows asks you to terminate the batch job, type `Y` and press Enter.

The page loads only while the Command Prompt window is still running that command. Closing the window stops the website.

The site listens only on this computer, at address 127.0.0.1, port 8765. It is not reachable from other computers.

### If the command is not recognized

If Command Prompt says that `python` is not recognized, close the window and repeat steps 2 to 4 so a new Command Prompt opens in this folder. Then type this command and press Enter:

    py server.py

Use the same address in the browser: http://127.0.0.1:8765

### If port 8765 is already in use

Type this command instead:

    python server.py 8080

Then open this address in the browser:

    http://127.0.0.1:8080

If you had to use `py` above, the command is `py server.py 8080`.

## Optional: run the same checks without the website

From the same Command Prompt window, in this folder, type:

    python signup.py

The program asks for the four fields one at a time. Type each value and press Enter. It uses the same rules as the website. If `python` is not recognized, type `py signup.py` instead.

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
