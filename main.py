import configparser
from flask import Flask, request
import smtplib
import sys

# Read the config file.
config = configparser.ConfigParser()
config.read("config.ini")
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
    s.login(smtpsettings["FromEmailAddress"], smtpSettings["Password"])

    # Build the message.
    emailMessage = "Subject: {}\n\n{}".format("Contact Message", message)

    # Send the email.
    s.sendmail(smtpsettings["FromEmailAddress"], smtpsettings["ToEmailAddress"], emailMessage)

    # Disconnect.
    s.quit()

    # Good response.
    return "True"
  except:
    return "False"

app.run(debug=True, port=8080)