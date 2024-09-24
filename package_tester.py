from PIL import Image
import pytesseract
from thefuzz import fuzz
import pandas as pd
import time
import smtplib
import ssl
from email.message import EmailMessage

email_sender = 'studentrectory@gmail.com'
email_password = 'rkbajalwxnueonsd'
email_receiver = 'madeline.karp@rectoryschool.org'

subject = 'Your package has arrived'
body = """
Your package has arrived and is waiting in the package room.
"""


em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	smtp.login(email_sender, email_password)
	smtp.sendmail(email_sender, email_receiver, em.as_string())
	
s = time.time()
def extract_text_from_image(image_path):
	image = Image.open(image_path)
	text = pytesseract.image_to_string(image)
	return text
f = pd.read_csv('facultyplus.csv')
cols = f.columns.tolist()
high = 0
index = 0
name = (extract_text_from_image('package_1.jpg'))
print(name)
names = f[cols[0]]
split = time.time()
for i in range(len(names)):
	x = fuzz.ratio(name, names[i])
	if x > high:
		index = i
		high = x
print(x)
print(index)
print(x, ",", index, "," , names[index])
e = time.time()
print(split - s)
print(e - split)
print(e - s)

