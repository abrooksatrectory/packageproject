#importing all necessary
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
import PySimpleGUI as sg
import numpy
import cv2

#function to extract text from image
def extract_text_from_image(image_path):
	image = Image.open(image_path)
	text = pytesseract.image_to_string(image)
	return text

#function to send email
def send_email(name, email):
	boby = "Dear "+name+" Your packaged arrived"
	email_sender = 'studentrectory@gmail.com'
	email_password = 'rkbajalwxnueonsd'
	email_receiver = email
	subject = 'package arrived :D'
	body = boby
	em=EmailMessage()
	em['From'] = email_sender
	em['To'] = email_receiver
	em['subject'] = subject
	em.set_content(body)
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login(email_sender, email_password)
			smtp.sendmail(email_sender, email_receiver, em.as_string())

#compares the extracted text through the list of names and picks the most similar name and email
def get_email(input_name):
	s = time.time()	
	f = pd.read_csv('facultyplus.csv')
	cols = f.columns.tolist()
	high = 0
	index = 0
	if input_name != 0:
		name = input_name
	else:
		name = (extract_text_from_image('test_photo.jpg'))
	names = f[cols[0]]
	emails = f[cols[1]]
	split = time.time() 
	for i in range(len(names)):
		x = fuzz.partial_ratio(name, names[i])
		if x > high:
			index = i
			high = x
	e = time.time()
	return names[index], emails[index]


#initializes camera
picam2 = Picamera2()
#fixes color contrast issue with the camera
picam2.configure(picam2.create_preview_configuration({'format': 'RGB888'}))
#starts the camera
picam2.start()

#defines a layout column
col = [
	[sg.Output(size=(30,10))],
	[sg.Button("Send email")]
]

#creates the layout for the user interface
layout = [
	[sg.Button("Capture")],
	[sg.Image(filename="", key="-IMAGE-"), sg.Column(col)],
	[sg.Input(default_text=" ", key='-Input-'), sg.Button("Submit"), sg.Button("Exit")]
]

#pop-up UI
window = sg.Window("Camera App", layout)

#loop that holds all button functions and runs the UI
stop_gui = 0
while stop_gui == 0:	
	#creates the live picture preview
	image = picam2.capture_array()
	#continues to run the UI
	event, values = window.read(timeout=100)
	#exits the UI if the Exit button is used
	if event == "Exit" or event == sg.WIN_CLOSED:
		stop_gui = 1
	#takes an image when the Capture button is used
	if event == "Capture":
		picam2.capture_file("test_photo.jpg")
		name, email = get_email(0)
		#prints the results so the user can confirm
		print(name)
		print(email)
		#allows the user to enter the name manually
	if event=='Submit':
		name, email = get_email(values['-Input-'])
		print(name)
		print(email)
		#sends the email to the listed email address if the Send email button is used
	if event=='Send email':
		send_email(name, email)	

	#displaying preview
	_, encoded_image = cv2.imencode(".png", image)
	window["-IMAGE-"].update(data=encoded_image.tobytes())

#exits the window and stops the camera (when Exit button is pressed)
window.close()
picam2.stop()
