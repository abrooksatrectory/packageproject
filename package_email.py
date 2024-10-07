from PIL import Image
import pytesseract
from thefuzz import fuzz
import pandas as pd
import time
import smtplib
import ssl
from email.message import EmailMessage
from picamera2 import Picamera2, Preview
import time
import pyautogui
import PySimpleGUI as sg
import numpy
import cv2

def extract_text_from_image(image_path):
	image = Image.open(image_path)
	text = pytesseract.image_to_string(image)
	return text

def get_email():
	s = time.time()
		
		
	f = pd.read_csv('facultyplus.csv')
	cols = f.columns.tolist()
	high = 0
	index = 0
	name = (extract_text_from_image('test_photo.jpg'))
	#print(name)
	names = f[cols[0]]
	split = time.time()
	for i in range(len(names)):
		x = fuzz.partial_ratio(name, names[i])
		if x > high:
			index = i
			high = x
	#print(x)
	#print(index)
	#print(x, ",", index, "," , names[index])
	e = time.time()
	#print(split - s)
	#print(e - split)
	#print(e - s)
	return names[index]

#Mrs. Karp's code
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()

layout = [
	[sg.Image(filename="", key="-IMAGE-")],
	[sg.Button("Capture"), sg.Output(size=(30,10)), sg.Button("Exit")]
]

window = sg.Window("Camera App", layout)

stop_gui = 0
while stop_gui == 0:
	event, values = window.read(timeout=100)

	if event == "Exit" or event == sg.WIN_CLOSED:
		stop_gui = 1
	if event == "Capture":
		picam2.capture_file("test_photo.jpg")
		name = get_email()
		print(name)
	image = picam2.capture_array()

	_, encoded_image = cv2.imencode(".png", image)
	window["-IMAGE-"].update(data=encoded_image.tobytes())

window.close()
picam2.stop()
# End of Mrs. Karp's code


"""
boby = "Dear "+str(names[i])+" Your packaged arrived"
email_sender = 'studentrectory@gmail.com'
email_password = 'rkbajalwxnueonsd'
email_receiver = high

subject = 'package arrived :D'
body = boby

em=EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['subject'] = subject
em.set_content(body)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	ask = input("send email to "+em['To']+" ?  [Y/n]")
	if ask == 'Y':
		smtp.login(email_sender, email_password)
		smtp.sendmail(email_sender, email_receiver, em.as_string())

"""
