#!/usr/bin/env python3
"""XYZ Company sign-up website.

Serves a registration form on localhost and checks each field with the
validators in signup.py. Submitted text is escaped before it is placed
back on the page. Nothing is sent to a database or a shell.
"""

import html
import socketserver
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

from signup import validate_fields

HOST = "127.0.0.1"
DEFAULT_PORT = 8765
MAX_BODY = 8192
FIELDS = (
    ("first_name", "First Name", "John", "given-name", "One capital letter, then lowercase letters."),
    ("email", "Email Address", "john@example.com", "email", "A standard email address."),
    ("phone", "Telephone Number", "(416) 555-1234", "tel", "Include the brackets, space, and hyphen."),
    ("postal", "Postal Code", "M5V 3A8", "postal-code", "Letter, number, letter, space, number, letter, number."),
)
ALLOWED_FIELDS = {name for name, *_rest in FIELDS}

CSS = """
:root {
  --ink: #1c1915;
  --muted: #5e584e;
  --line: #e3dbd0;
  --paper: #f6f3ee;
  --card: #fffdfb;
  --accent: #1f4d3a;
  --accent-dark: #16382a;
  --danger: #8d2c2c;
  --danger-bg: #f8eceb;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  background: radial-gradient(ellipse at top, #fff 0%, var(--paper) 58%);
  font-family: "Iowan Old Style", Palatino, "Palatino Linotype", Georgia, serif;
}
main {
  width: min(28rem, calc(100% - 2rem));
  margin: 3.5rem auto 4rem;
}
.brand {
  margin: 0 0 0.4rem;
  font-family: system-ui, sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
}
h1 {
  margin: 0 0 0.45rem;
  font-size: 2.05rem;
  font-weight: 560;
  line-height: 1.15;
}
.lede {
  margin: 0 0 1.35rem;
  color: var(--muted);
  line-height: 1.5;
}
.panel, form {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1.2rem 1.2rem 1.3rem;
}
.banner {
  margin: 0 0 1rem;
  padding: 0.75rem 0.9rem;
  border-radius: 8px;
  background: var(--danger-bg);
  color: var(--danger);
  font-family: system-ui, sans-serif;
  font-size: 0.92rem;
}
.banner strong { display: block; margin-bottom: 0.35rem; }
.banner ul { margin: 0; padding-left: 1.15rem; }
.field { margin-bottom: 0.95rem; }
label {
  display: block;
  margin-bottom: 0.35rem;
  font-family: system-ui, sans-serif;
  font-size: 0.92rem;
  font-weight: 650;
}
input {
  width: 100%;
  padding: 0.68rem 0.75rem;
  border: 1px solid #d4cdc2;
  border-radius: 8px;
  background: #fff;
  color: var(--ink);
  font: 1rem/1.4 system-ui, sans-serif;
}
input:focus {
  outline: 2px solid var(--accent);
  outline-offset: 1px;
  border-color: var(--accent);
}
input[aria-invalid="true"] { border-color: var(--danger); }
.hint, .field-error {
  margin: 0.35rem 0 0;
  font-family: system-ui, sans-serif;
  font-size: 0.8rem;
  line-height: 1.4;
}
.hint { color: var(--muted); }
.field-error { color: var(--danger); }
button, .back {
  font-family: system-ui, sans-serif;
}
button {
  width: 100%;
  margin-top: 0.35rem;
  padding: 0.82rem 1rem;
  border: 0;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
  font-size: 1rem;
  font-weight: 650;
  cursor: pointer;
}
button:hover { background: var(--accent-dark); }
button:focus-visible, .back:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.back {
  display: inline-block;
  margin-top: 1rem;
  color: var(--accent);
  font-weight: 650;
}
.panel p { margin: 0.35rem 0 0; line-height: 1.5; }
"""


def esc(value):
    return html.escape(value, quote=True)


def page(title, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<main>
<p class="brand">XYZ Company</p>
{body}
</main>
</body>
</html>
"""


def render_form(values, errors):
    by_field = {}
    for name, message in errors:
        if name:
            by_field[name] = message
    banner = ""
    if errors:
        items = "".join(f"<li>{esc(message)}</li>" for _name, message in errors)
        banner = (
            '<div class="banner" role="alert">'
            "<strong>Registration failed.</strong>"
            f"<ul>{items}</ul></div>"
        )
    fields_html = []
    for name, label, example, autocomplete, hint in FIELDS:
        message = by_field.get(name)
        described = f"{name}-hint"
        error_html = ""
        invalid = ""
        if message:
            described += f" {name}-error"
            invalid = ' aria-invalid="true"'
            error_html = f'<p id="{name}-error" class="field-error">{esc(message)}</p>'
        fields_html.append(
            f'<div class="field">'
            f'<label for="{name}">{esc(label)}</label>'
            f'<input id="{name}" name="{name}" type="text" '
            f'autocomplete="{esc(autocomplete)}" spellcheck="false" '
            f'placeholder="{esc(example)}" value="{esc(values.get(name, ""))}" '
            f'aria-describedby="{described}"{invalid}>'
            f'<p id="{name}-hint" class="hint">{esc(hint)} Example: {esc(example)}</p>'
            f"{error_html}</div>"
        )
    body = (
        "<h1>Create an account</h1>"
        '<p class="lede">Enter the four fields below. The server accepts a value only when the whole entry matches that field.</p>'
        f'<form method="post" action="/" novalidate>{banner}{"".join(fields_html)}'
        '<button type="submit">Create account</button></form>'
    )
    return page("Sign up · XYZ Company", body)


def render_success(first_name):
    body = (
        '<section class="panel">'
        "<h1>Sign-Up Completed!</h1>"
        f"<p>Welcome, {esc(first_name)}. The account details passed validation.</p>"
        '<a class="back" href="/">Register another account</a>'
        "</section>"
    )
    return page("Sign-Up Completed! · XYZ Company", body)


def render_notice(heading, message):
    body = (
        '<section class="panel">'
        f"<h1>{esc(heading)}</h1>"
        f"<p>{esc(message)}</p>"
        '<a class="back" href="/">Back to sign-up</a>'
        "</section>"
    )
    return page(f"{heading} · XYZ Company", body)


def read_submission(raw):
    """Return (values, errors). values is None when the body itself is refused."""
    try:
        parsed = parse_qs(
            raw,
            keep_blank_values=True,
            strict_parsing=False,
            # A couple of unexpected names are still parsed so the response can
            # say they are not part of the form. A larger set is refused here.
            max_num_fields=8,
        )
    except ValueError:
        return None, [(None, "The form contained too many fields.")]
    unknown = set(parsed) - ALLOWED_FIELDS
    if unknown:
        return None, [(None, "The form contained a field that is not part of sign-up.")]
    values = {}
    for name in ALLOWED_FIELDS:
        items = parsed.get(name, [""])
        if len(items) != 1:
            return None, [(None, "Each field must be submitted once.")]
        values[name] = items[0]
    return values, validate_fields(
        values["first_name"],
        values["email"],
        values["phone"],
        values["postal"],
    )


class SignUpServer(ThreadingHTTPServer):
    def server_bind(self):
        # The normal HTTP server looks up the hostname for 127.0.0.1.
        # That reverse lookup can stall, so the local name is set directly.
        socketserver.TCPServer.server_bind(self)
        _host, port = self.server_address[:2]
        self.server_name = "localhost"
        self.server_port = port


class SignUpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if path != "/":
            self._send(404, render_notice("Page not found", "That page is not part of the sign-up form."))
            return
        self._send(200, render_form({}, []))

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path != "/":
            self._send(404, render_notice("Page not found", "That page is not part of the sign-up form."))
            return
        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("application/x-www-form-urlencoded"):
            self._send(
                415,
                render_form({}, [(None, "Submit the sign-up form from this page.")]),
            )
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(400, render_notice("Registration failed.", "The form submission could not be read."))
            return
        if length < 0 or length > MAX_BODY:
            self.close_connection = True
            self._send(
                413,
                render_notice("Registration failed.", "The form submission is too large."),
            )
            return
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        values, errors = read_submission(raw)
        if errors:
            self._send(400, render_form(values or {}, errors))
            return
        self._send(200, render_success(values["first_name"]))

    def _send(self, status, body):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
        )
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    httpd = SignUpServer((HOST, port), SignUpHandler)
    print(f"XYZ Company sign-up: http://{HOST}:{port}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
