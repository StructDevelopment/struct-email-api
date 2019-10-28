import configparser
from flask import abort, Flask, request
import smtplib
import sys

# Read the config file.
config = configparser.ConfigParser()
config.read("struct-email.ini")
config.sections()
smtpsettings = config["SMTP"]

app = Flask(__name__)

@app.route("/email", methods=["POST"])
def email():
  try:
    # Read fields.
    content = request.get_json(silent=True)
    message = content.get("message")

    # Connect.
    s = smtplib.SMTP("smtp.gmail.com", 587)
    # Authentication.
    s.starttls()
    s.login(smtpsettings["FromEmailAddress"], smtpsettings["Password"])

    # Build the message.
    emailMessage = "Subject: {}\n\n{}".format("Contact Message", message)

    # Send the email.
    s.sendmail(smtpsettings["FromEmailAddress"], smtpsettings["ToEmailAddress"], emailMessage)

    # Disconnect.
    s.quit()

    return "True"
  except:
    abort(500)

app.run(debug=True, port=8080)