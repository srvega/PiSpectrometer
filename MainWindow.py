#lines are terminated with EOL
#blocks are terminated by end of indentation
#you ain't gotta declare. Just start typing it and it exists.
#multi-line comments are designated by triple quotes. This is a garbage language.
#!/usr/bin/env python3
import os
import sys
from time import sleep
import datetime
#import PIL
nPythonVersion = sys.version_info.major
sFileTimeStamp = ""
bCameraActive = False

try:
	#start as v3 and gracefully degrade
	import tkinter as tkinter
	from tkinter import StringVar
	import tkinter.ttk as ttk
	from tkinter import font
	from tkinter import PhotoImage
	sFileTimeStamp = '{:%Y%m%d-%H%M%S-%f}'.format(datetime.datetime.now())[:-4]
except:
	import Tkinter as tkinter
	from tkinter import StringVar
	import Tkinter.ttk as ttk
	from tkFont import Font
	from tkinter import PhotoImage
	#import datetime
	sFileTimeStamp = "{:%Y%m%d-%H%M%S-%f}".format(datetime.datetime.now())[:-4]
#end try/catch

try:
	import picamera
	#rotation=0,90,180,270
	#sensor_mode=2,vflip=,shutter_speed=,sharpness=,saturation=,
	oCamera = picamera.PiCamera(iso=800,led=False,meter_mode="backlit",resolution=(2592,1944))
	bCameraActive = True
except:
	bCameraActive = False
#end try/catch

sCurrentFolder = os.path.dirname(__file__)
sImgIcnArrowUpLoc = os.path.join(sCurrentFolder, "images/arrowUp.png")
sImgIcnArrowDownLoc = os.path.join(sCurrentFolder, "images/arrowDown.png")
sImgIcnPowerLoc = os.path.join(sCurrentFolder, "images/power.png")
sImgIcnLEDRedOn = os.path.join(sCurrentFolder, "images/LEDRedOn.png")
sImgIcnLEDRedOff = os.path.join(sCurrentFolder, "images/LEDRedOff.png")
sImgIcnLEDYellowOn = os.path.join(sCurrentFolder, "images/LEDYellowOn.png")
sImgIcnLEDYellowOff = os.path.join(sCurrentFolder, "images/LEDYellowOff.png")
sImgIcnLEDGreenOn = os.path.join(sCurrentFolder, "images/LEDGreenOn.png")
sImgIcnLEDGreenOff = os.path.join(sCurrentFolder, "images/LEDGreenOff.png")
sImgIcnCamera = os.path.join(sCurrentFolder, "images/camera.png")

bLEDRed = False
bLEDGreen = False
bLEDYellow = False

#build window object ASAP
oAppWindow = tkinter.Tk()

colorBGMain = "white"
colorFGMain = "black"
colorBGExit = "#d9534f"
colorFGExit = "white"
colorBGExitClick = "#c9302c"
colorBGShutdown = "black"
colorFGShutdown = "white"
colorBGPrimary = "#337ab7"
colorBGPrimaryClick = "#286090"
colorBGYellow = "#f0ad4e"
colorBGGreen = "#5cb85c"

imgIcnPower = PhotoImage(file=sImgIcnPowerLoc)
imgIcnArrowUp = PhotoImage(file=sImgIcnArrowUpLoc)
imgIcnArrowDown = PhotoImage(file=sImgIcnArrowDownLoc)
imgIcnLEDRedOn = PhotoImage(file=sImgIcnLEDRedOn)
imgIcnLEDRedOff = PhotoImage(file=sImgIcnLEDRedOff)
imgIcnLEDYellowOn = PhotoImage(file=sImgIcnLEDYellowOn)
imgIcnLEDYellowOff = PhotoImage(file=sImgIcnLEDYellowOff)
imgIcnLEDGreenOn = PhotoImage(file=sImgIcnLEDGreenOn)
imgIcnLEDGreenOff = PhotoImage(file=sImgIcnLEDGreenOff)
imgIcnCamera = PhotoImage(file=sImgIcnCamera)

nScannerDistance = 0
nScannerDistanceMin = 0
nScannerDistanceMax = 10
sDistanceDesc = StringVar()
sDistanceDesc.set("0mm")
sDistanceUnits = "mm"

oAppWindow.style = ttk.Style()
oAppWindow.configure(bg = colorBGMain)
#re-enable this for PROD/deploy
oAppWindow.geometry("700x480+0+0")
#this hides the window titlebar, along with close/min/max buttons
oAppWindow.overrideredirect(True)
#oAppWindow.geometry(str(oAppWindow.winfo_screenwidth()-20) + "x" + str(oAppWindow.winfo_screenheight()-20))
oAppWindow.lift()

def Take_Photo():
	global oCamera
	sTempImagePath = os.path.join(sCurrentFolder, "./captures/" + "{:%Y%m%d-%H%M%S-%f}".format(datetime.datetime.now())[:-4] + ".png")
	oCamera.capture(sTempImagePath)
	cnvImageDisplay.create_image(300, 300, image=sTempImagePath)
#end Take_Photo

#any ui interaction functions must be declared before whatever invokes them
def Window_Close():   
    oAppWindow.destroy()
#end Window_Close

def OS_Shutdown():
    os.system("sudo shutdown -h now")
#end OS_Shutdown

#variables in functions are assumed to be local declarations unless explicitly declared as being references to global ones.
#if buttons increment or decrement beyond the min or max, cycle through accepted values
def Lower_ScanDistance():
	global nScannerDistance
	global sDistanceDesc
	global sDistanceUnits
	global nScannerDistanceMax
	global nScannerDistanceMin
	if nScannerDistance - 1 < nScannerDistanceMin :
		nScannerDistance = nScannerDistanceMax
	else:
		nScannerDistance -= 1
	sDistanceDesc.set(str(nScannerDistance) + sDistanceUnits)
#end Decrement_ScanDistance

def Raise_ScanDistance():
	global nScannerDistance
	global sDistanceDesc
	global sDistanceUnits
	global nScannerDistanceMax
	global nScannerDistanceMin
	if nScannerDistance + 1 > nScannerDistanceMax :
		nScannerDistance = nScannerDistanceMin
	else:
		nScannerDistance += 1
	sDistanceDesc.set(str(nScannerDistance) + sDistanceUnits)
#end Increment_ScanDistance

def ActivateLED(nCode):	
	global imgIcnLEDRedOn
	global imgIcnLEDRedOff
	global imgIcnLEDGreenOn
	global imgIcnLEDGreenOff
	global imgIcnLEDYellowOn
	global imgIcnLEDYellowOff
	global colorBGExit
	global colorBGMain
	global colorFGExit
	global bLEDRed
	global bLEDGreen
	global bLEDYellow
	#red
	if (nCode == 1):
		if (bLEDRed):
			btnLEDRed.configure(image=imgIcnLEDRedOff, background=colorBGMain, fg=colorBGExit)
		else:
			btnLEDRed.configure(image=imgIcnLEDRedOn, background=colorBGExit, fg=colorFGExit)
		bLEDRed = not bLEDRed
		bLEDGreen = False
		bLEDYellow = False
		btnLEDYellow.configure(image=imgIcnLEDYellowOff, background=colorBGMain, fg=colorBGYellow)
		btnLEDGreen.configure(image=imgIcnLEDGreenOff, background=colorBGMain, fg=colorBGGreen)		
	#green
	if (nCode == 2):
		if (bLEDGreen):
			btnLEDGreen.configure(image=imgIcnLEDGreenOff, background=colorBGMain, fg=colorBGGreen)
		else:
			btnLEDGreen.configure(image=imgIcnLEDGreenOn, background=colorBGGreen, fg=colorBGMain)
		bLEDGreen = not bLEDGreen
		bLEDRed = False
		bLEDYellow = False
		btnLEDRed.configure(image=imgIcnLEDRedOff, background=colorBGMain, fg=colorBGExit)
		btnLEDYellow.configure(image=imgIcnLEDYellowOff, background=colorBGMain, fg=colorBGYellow)		
	#yellow
	if (nCode == 3):
		if (bLEDYellow):
			btnLEDYellow.configure(image=imgIcnLEDYellowOff, background=colorBGMain, fg=colorBGYellow)		
		else:
			btnLEDYellow.configure(image=imgIcnLEDRedOn, background=colorBGYellow, fg=colorBGMain)
		bLEDYellow = not bLEDYellow
		bLEDRed = False
		bLEDGreen = False
		btnLEDRed.configure(image=imgIcnLEDRedOff, background=colorBGMain, fg=colorBGExit)
		btnLEDGreen.configure(image=imgIcnLEDGreenOff, background=colorBGMain, fg=colorBGGreen)
#end ActivateLED

#negative coordinates are valid - they will display slightly hidden
#add main window buttons (close app, shutdown device, etc)
btnCloseWindow = tkinter.Button(oAppWindow, image=imgIcnPower, width=35, height=35, command=Window_Close, activeforeground=colorFGExit, activebackground=colorBGExitClick, bg=colorBGExit, fg=colorFGExit, bd=1, relief="solid")
btnCloseWindow.place(x=662, y=-1)

btnArrowUp = tkinter.Button(oAppWindow, image=imgIcnArrowUp, width=28, height=28, command=Raise_ScanDistance, activebackground=colorBGPrimaryClick, bg=colorBGPrimary, bd=1, relief="solid")
btnArrowUp.place(x=10, y=75)
btnArrowDown = tkinter.Button(oAppWindow, image=imgIcnArrowDown, width=28, height=28, command=Lower_ScanDistance, activebackground=colorBGPrimaryClick, bg=colorBGPrimary, bd=1, relief="solid")
btnArrowDown.place(x=10, y=105)

btnCamera = tkinter.Button(oAppWindow, image=imgIcnCamera, width=120, height=60, command=Take_Photo, activebackground=colorBGPrimaryClick, bg=colorBGPrimary, bd=1, relief="solid")
btnCamera.place(x=30, y=300)
#se.btnCamera.config(state=NORMAL)

btnLEDRed = tkinter.Button(oAppWindow, image=imgIcnLEDRedOff, width=35, height=35, command=lambda:ActivateLED(1), activebackground=colorFGExit, bg=colorBGMain, bd=1, relief="solid")
btnLEDRed.place(x=20, y=170)
btnLEDGreen = tkinter.Button(oAppWindow, image=imgIcnLEDGreenOff, width=35, height=35, command=lambda:ActivateLED(2), activebackground=colorFGExit, bg=colorBGMain, bd=1, relief="solid")
btnLEDGreen.place(x=70, y=170)
btnLEDYellow = tkinter.Button(oAppWindow, image=imgIcnLEDYellowOff, width=35, height=35, command=lambda:ActivateLED(3), activebackground=colorFGExit, bg=colorBGMain, bd=1, relief="solid")
btnLEDYellow.place(x=120, y=170)

sText = "Screen: " + str(oAppWindow.winfo_screenwidth()) + "x" + str(oAppWindow.winfo_screenheight()) + "px"
sText += " | Win: " + str(oAppWindow.winfo_width()) + "x" + str(oAppWindow.winfo_height()) + "px"
sText += " | Python v" + str(sys.version_info.major) + "." + str(sys.version_info.minor)

lblHeader = tkinter.Label(oAppWindow, text=sText, bg=colorBGMain, fg=colorFGMain)
lblHeader.pack()

#need to create a control to replace spinbox.  Want something that cycles, has colored buttons, no textbox cursor, etc.
#spnboxDepth = tkinter.Spinbox(oAppWindow, width=3, from_=nScannerDistanceMin, to=nScannerDistanceMax, font=font.Font(oAppWindow, family="Lucida Sans Unicode", size=24, weight="bold"), relief="solid")
#spnboxDepth.place(x=20, y=80)
lblBasic = tkinter.Label(oAppWindow, textvariable=sDistanceDesc, font=font.Font(oAppWindow, family="Lucida Console", size=28, weight="bold"), bg=colorBGMain, fg=colorFGMain)
lblBasic.place(x=47, y=83)

#btnShutdown = tkinter.Button(oAppWindow, text = "Shutdown", bg=colorBGShutdown, fg=colorFGShutdown, activeforeground=colorFGShutdown, activebackground=colorBGShutdown, command=OS_Shutdown, borderwidth=1, relief="solid").pack()
cnvImageDisplay = tkinter.Canvas(oAppWindow)
cnvImageDisplay.create_image(300, 300)
cnvImageDisplay.place(x=200, y=70)

oAppWindow.mainloop()
