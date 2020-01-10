import smtplib
import imaplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

def readEmail():
	mailserver = imaplib.IMAP4_SSL("imap.gmail.com", 993)
	username = raw_input("gmail username: ")
	password = raw_input("password: ")
	mailserver.login(username, password)

	status, count = mailserver.select("Inbox")
	status, data = mailserver.fetch(count[0],'(UID BODY[TEXT])')

	print(data[0][1])

	mailserver.close()
	mailserver.logout()

def sendEmail():
	username = raw_input("gmail username: ")
	password = raw_input("password: ")
	fromAddr = raw_input("from: ")
	toAddr = raw_input("to: ")
	subject = raw_input("Subject: ")
	text = raw_input("Text: ")
	attachment = raw_input("Attachment: ")

	msg = MIMEMultipart()
	msg["From"] = fromAddr
	msg["To"] = toAddr
	msg["Subject"] = subject
	msg.attach(MIMEText(text))

	if attachment is not None:
		files = [attachment]
		for path in files:
			part = MIMEBase("application", "octet-stream")
			with open(path, "rb") as f:
				part.set_payload(f.read())
				Encoders.encode_base64(part)
				part.add_header("Content-Disposition", "attachment; filename = {}".format(path))
				msg.attach(part)

	server = smtplib.SMTP("smtp.gmail.com:587")
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username,password)
	server.sendmail(fromAddr, toAddr, msg.as_string())
	server.quit()

print("Gmail")
while (1):
	choice = raw_input("1. Send\n2. Inbox\n3. Exit\n")
	if choice == "1":
		print("Send")
		sendEmail()
		print("Email Sent")
	elif choice == "2":
		print("Inbox")
		readEmail()
	elif choice == "3":
		print("Exit")
		break
	else:
		print("Invalid input. Please choose again.")

