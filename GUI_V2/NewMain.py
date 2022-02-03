import time
from tkinter import *
import math
class App:
    def __init__(self):
        self.window = Tk()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry("850x650")  # Screen Size
        self.window.resizable(0, 0)
        self.window.title("ALFA-ETA") # Pencere ismi
        self.window.iconname("ALFA-ETA")
        self.window.config(background="white")
        #app icon
        photo = PhotoImage(file="Images/logo.png")
        self.window.iconphoto("false", photo)
        self.speedometer = Speedometer(self)
        self.mainBattery = Battery(self,0,525)
        x = 130 ; y = 80
        self.allBatteries = [Battery(self, (y*j)+5, (x*i)+5)  for j in range(8) for i in range(4)]
        
        '''self.signals=Signals(self)  '''
class Signals:
    def __init__(self, obj):
        #Signals Canvas
        self.allSignals=[0,0,0,0,0,0]#Current,Voltage,Engine,Left,Right,Tempereture
        self.rightSignal = [PhotoImage(file='Images/right_off.png'), PhotoImage(file='Images/right_on.png')]
        self.leftSignal = [PhotoImage(file='Images/left_off.png'), PhotoImage(file='Images/left_on.png')]
        self.engineSignal = [PhotoImage(file='Images/engine_ok.png'), PhotoImage(file='Images/engine_bad.png')]
        self.thermometer = [PhotoImage(file='Images/thermometer_ok.png'),PhotoImage(file='Images/thermometer_bad.png')]
        self.electroSignal = [PhotoImage(file='Images/A.png'), PhotoImage(file='Images/V.png')]
        self.signalFrame = Frame(
            obj.window, height=135, width=800, background="white", highlightthickness=5)
        self.signalFrame.pack(side=BOTTOM)
        self.currentLabel = Label(
            self.signalFrame, image=self.electroSignal[0], bg="white", text="0", compound=TOP, fg="black", font=('Helvetica 16 bold'))
        self.currentLabel.pack(side=LEFT)
        self.voltageLabel = Label(
            self.signalFrame, image=self.electroSignal[1], bg="white", text="0", compound=TOP, fg="black", font=('Helvetica 16 bold'))
        self.voltageLabel.pack(side=LEFT)
        self.engineLabel = Label(
            self.signalFrame, image=self.engineSignal[0], bg="white")
        self.engineLabel.pack(side=LEFT)
        self.leftLabel = Label(
            self.signalFrame, image=self.leftSignal[0], bg="white")
        self.leftLabel.pack(side=LEFT)
        self.rightLabel = Label(
            self.signalFrame, image=self.rightSignal[0], bg="white")
        self.rightLabel.pack(side=LEFT)
        self.thermoLabel = Label(
            self.signalFrame, image=self.thermometer[0],bg="white", text="0", compound=TOP, fg="black", font=('Helvetica 16 bold'))
        self.thermoLabel.pack(side=LEFT)
class Speedometer:
    def __init__(self, obj):
        #SPEED Canvas
        self.speedCanvas = Canvas(
            obj.window, height=100, width=200, background="white", highlightthickness=0)
        self.speedometer = PhotoImage(file='Images/speedometer.png')
        self.speedCanvas.create_image(
            103, 52, image=self.speedometer, anchor=CENTER)
        coord = 2, 200, 200, 2
        self.speedCanvas.create_arc(coord, start=0, extent=180, width=2)
        self.speedCanvas.pack()
        self.speedCanvas.place(relx=1, rely=1, anchor=SE)
        #SPEED Arrow
        self.speedArrow = self.speedCanvas.create_line(
            100, 100, 0, 100, arrow=LAST, width=5, fill="blue")
        self.angle = 90
        self.speedTxt = self.speedCanvas.create_text(
            100, 65, fill="black", text="0", font=('Helvetica 20 bold'))
class Battery:
    def __init__(self, obj,_x_=100,_y_=100):
        #Battery Canvas
        self.batteryCanvas = Canvas(obj.window, height=125, width=74,
                                    background="white", highlightthickness=1)
        self.batteryImages = [PhotoImage(
            file='Images/normalbattery.png'), PhotoImage(file='Images/chargbatery.png')]
        #Battery Charge
        self.batteryCharge = self.batteryCanvas.create_rectangle(
            69, 122, 5, 122, fill="#A10000")
        self.batteryImage = self.batteryCanvas.create_image(
            0, 2, image=self.batteryImages[0], anchor=NW)
        self.batteryCanvas.place(x=_x_, y=_y_)
        self.batteryTxt = self.batteryCanvas.create_text(
            37.5, 110, fill="black", text="0", font=('Helvetica 16 bold'))
        self.charge = 0

def changeSpeed(obj):
    for i in range(0,80):
        updateSpeed(obj,i)
    for i in range(80,40,-1):
        updateSpeed(obj, i)
    for i in range(40,100):
        updateSpeed(obj, i)
    for i in range(100,0, -1):
        updateSpeed(obj, i)
def changeBattery(obj):
    for i in range(0, 80):
        updateBattery(obj.mainBattery, i)
        obj.window.update()
    for i in range(80, 40, -1):
        updateBattery(obj.mainBattery, i)
        obj.window.update()
    for i in range(40, 100):
        updateBattery(obj.mainBattery, i)
        obj.window.update()
    for i in range(100, 0, -1):
        updateBattery(obj.mainBattery, i)
        obj.window.update()
def updateSpeed(obj, speed=0):
    if (obj.speedometer.angle < 270) or (obj.speedometer.angle > 90):
        obj.speedometer.angle = 90 + 1.8*speed
        #obj.speedometer.angle += 1.8
        x = 100 - 100*math.sin(math.radians(obj.speedometer.angle))
        y = 100 + 100*math.cos(math.radians(obj.speedometer.angle))
        obj.speedometer.speedCanvas.delete(obj.speedometer.speedTxt)
        obj.speedometer.speedCanvas.delete(obj.speedometer.speedArrow)
        obj.speedometer.speedTxt = obj.speedometer.speedCanvas.create_text(100, 65, fill="black", text=str(
            int((obj.speedometer.angle-90)/1.8)), font=('Helvetica 20 bold'))
        obj.speedometer.speedArrow = obj.speedometer.speedCanvas.create_line(
            100, 100, 0 + x, y, arrow=LAST, width=5, fill="blue")

    obj.window.update()
def updateBattery(obj, charge=0):
    if (obj.charge > 0) or (obj.charge < 100):
        obj.batteryCanvas.delete(obj.batteryCharge)
        obj.batteryCanvas.delete(obj.batteryTxt)
        obj.batteryCanvas.delete(obj.batteryImage)
        
        x = 122 - int(charge*1.04)
        color = colorPicker(charge)
        obj.batteryCharge = obj.batteryCanvas.create_rectangle(
            69, 122, 5, x, fill=color)
        if charge >= obj.charge:
            obj.batteryImage = obj.batteryCanvas.create_image(
                0, 2, image=obj.batteryImages[1], anchor=NW)
        else:
            obj.batteryImage = obj.batteryCanvas.create_image(
                0, 2, image=obj.batteryImages[0], anchor=NW)
        obj.charge = charge
        obj.batteryTxt = obj.batteryCanvas.create_text(
            37.5, 110, fill="black", text=str(obj.charge), font=('Helvetica 16 bold'))

def colorPicker(charge):
    if charge < 20:
        return "#A10000"
    elif charge < 40:
        return "#C25F00"
    elif charge < 60:
        return "#E2BE00"
    elif charge < 80:
        return "#AAB900"
    else:
        return "#71B400"
    
def change(obj):
    time.sleep(0.5)
    changeSignals(obj,[3,46,0,1,1,55])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [10,15,0, 0, 0,20])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [36,54,1, 0, 1,100])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [0,0,0, 1,0,9])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [99,99,1, 1, 1,45])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [0,0,0,0,0,0])
    obj.window.update()

def change_leftSignal(obj):
    time.sleep(0.5)
    changeSignals(obj, [0,0,0,1,0,0])
    obj.window.update()
    time.sleep(0.5)
    obj.window.update()
    changeSignals(obj, [0,0,0,0,0,0])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [0,0,0,1,0,0])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [0,0,0,0,0,0])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [0,0,0,1,0,0])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [0, 0, 0, 0, 0, 0])
    obj.window.update()

def changeSignals(obj,signals):
    electroSignal(obj.signals,signals[0:2])
    engineSignal(obj.signals,signals[2])
    leftSignal(obj.signals, signals[3])
    rightSignal(obj.signals, signals[4])
    thermoSignal(obj.signals, signals[5])

def electroSignal(obj, signal):
    obj.currentLabel.destroy()
    obj.voltageLabel.destroy()
    obj.currentLabel = Label(
        obj.signalFrame, image=obj.electroSignal[0], bg="white", text=str(signal[0])+" I", compound=TOP, fg="black", font=('Helvetica 16 bold'))
    obj.currentLabel.pack(side=LEFT)
    obj.voltageLabel = Label(
        obj.signalFrame, image=obj.electroSignal[1], bg="white", text=str(signal[1])+" V", compound=TOP, fg="black", font=('Helvetica 16 bold'))
    obj.voltageLabel.pack(side=LEFT)
    
def engineSignal(obj,signal):
    obj.engineLabel.destroy()
    if signal == 0:
        obj.engineLabel = Label(
            obj.signalFrame, image=obj.engineSignal[0], bg="white")
    else:
        obj.engineLabel = Label(
            obj.signalFrame, image=obj.engineSignal[1], bg="white")
    obj.engineLabel.pack(side=LEFT)

def leftSignal(obj, signal):
    obj.leftLabel.destroy()
    if signal == 0:
        obj.leftLabel = Label(
            obj.signalFrame, image=obj.leftSignal[0], bg="white")
    else:
        obj.leftLabel = Label(
            obj.signalFrame, image=obj.leftSignal[1], bg="white")
    obj.leftLabel.pack(side=LEFT)
    
def rightSignal(obj, signal):
    obj.rightLabel.destroy()
    if signal == 0:
        obj.rightLabel = Label(
            obj.signalFrame, image=obj.rightSignal[0], bg="white")
    else:
        obj.rightLabel = Label(
            obj.signalFrame, image=obj.rightSignal[1], bg="white")
    obj.rightLabel.pack(side=LEFT)

def thermoSignal(obj,signal):
    obj.thermoLabel.destroy()
    img = obj.thermometer[0]
    if signal > 40:
        img = obj.thermometer[1]
    obj.thermoLabel = Label(
        obj.signalFrame, image=img, text=str(signal), bg="white", compound=TOP, fg="black", font=('Helvetica 16 bold'))
    obj.thermoLabel.pack(side=LEFT)
        
app = App()
app.window.bind("<Up>", lambda event, obj=app: changeSpeed(obj))
app.window.bind("<Left>", lambda event, obj=app: changeBattery(obj))

#app.window.bind("<BackSpace>", lambda event, obj=app: change(obj)) #

app.window.mainloop()
