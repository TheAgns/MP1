import requests
import pandas as pd
import smtplib
import ssl
from bs4 import BeautifulSoup
from email.message import EmailMessage
import re

email_sender = 'din email'
email_password = 'gmail app code'
subject = 'Invitation to our event'
message_body_template = """Dear {title} {name},
    
We are pleased to invite you to our event. Please find the attached copy of our company’s yearly report.

Best regards,
Your Company"""

attachment = "yearly_report.pdf"

invitees = pd.read_csv("invitees.csv")

def findCountryByIp(ip):
    url = "http://wsgeoip.lavasoft.com/ipservice.asmx"
    
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <GetIpLocation xmlns="http://lavasoft.com/">
        <sIp>{ip}</sIp>
        </GetIpLocation>
    </soap12:Body>
    </soap12:Envelope>"""

    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    response = requests.request("POST", url, headers=headers, data=payload)
    content = response.content
    xml = BeautifulSoup(content, "xml")

    result = xml.find("GetIpLocationResult").contents
    resultString = result.pop(0).text
    tag = "Country"
    regEx = "<" + tag + ">(.*?)</" + tag + ">"
    country = re.findall(regEx, resultString).pop()
    return country

genderize_service = "https://api.genderize.io?name={name}"

for index, row in invitees.iterrows():

    country = findCountryByIp(row["ip"])

    name_response = requests.get(genderize_service.format(name=row["name"]))
    name_data = name_response.json()
    gender = name_data.get("gender", "")

    if gender == "male" and country in ["US", "UK", "CA", "AU", "NZ", "DK"]:
        title = "Mr."
    elif gender == "female" and country in ["US", "UK", "CA", "AU", "NZ", "DK"]:
        title = "Ms."
    else:
        title = "error on define: "

    message_body = message_body_template.format(title=title, name=row["name"])

    message = EmailMessage()
    message["From"] = email_sender
    message["To"] = row["email"]
    message["Subject"] = subject
    message.set_content(message_body)

    with open(attachment, "rb") as f:
        message.add_attachment(f.read(), maintype="application", subtype="pdf", filename=attachment)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(message)

    print(f"Sent email to {row['email']}")
