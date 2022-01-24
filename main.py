import time
from tkinter import *
import math
from turtle import up
class App:
    def __init__(self):
        self.window = Tk()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(str(self.screen_width)+"x"+str(self.screen_height))  # Screen Size
        self.window.minsize(800,600)
        self.window.title("ALFA-ETA")  # Pencere ismi
        self.window.iconname("ALFA-ETA")
        self.window.config(background="white")
        #app icon
        photo = PhotoImage(file="Images/logo.png")
        self.window.iconphoto("false", photo)
        self.speedometer = Speedometer(self)
        self.battery = Battery(self)
        self.signals=Signals(self) 

class Signals:
    def __init__(self, obj):
        #Signals Canvas
        self.allSignals=[0,0,0]#Engine,Left,Right
        self.rightSignal = [PhotoImage(file='Images/right_off.png'), PhotoImage(file='Images/right_on.png')]
        self.leftSignal = [PhotoImage(file='Images/left_off.png'), PhotoImage(file='Images/left_on.png')]
        self.engineSignal = [PhotoImage(file='Images/engine_ok.png'), PhotoImage(file='Images/engine_bad.png')]
        self.thermometer = [PhotoImage(file='Images/thermometer_ok.png'),PhotoImage(file='Images/thermometer_bad.png')]
        self.signalFrame = Frame(
            obj.window, height=135, width=800, background="white", highlightthickness=5)
        self.signalFrame.pack(side=BOTTOM)
        self.engineLabel = Label(self.signalFrame, image=self.engineSignal[0])
        self.engineLabel.pack(side=LEFT)
        self.leftLabel = Label(self.signalFrame, image=self.leftSignal[0])
        self.leftLabel.pack(side=LEFT)
        self.rightLabel = Label(self.signalFrame, image=self.rightSignal[0])
        self.rightLabel.pack(side=LEFT)
        self.thermoLabel = Label(
            self.signalFrame, image=self.thermometer[0], text="0", compound=TOP, fg="black", font=('Helvetica 16 bold'))
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
    def __init__(self, obj):
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
        self.batteryCanvas.place(relx=0.0, rely=1.0, anchor=SW)
        self.batteryTxt = self.batteryCanvas.create_text(
            37.5, 110, fill="black", text="0", font=('Helvetica 16 bold'))
        self.charge = 0
        self.allBatteries = Toplevel(obj.window)
        self.allBatteries.destroy()

def speedUP(obj,speed=0):
    if obj.speedometer.angle < 270:
        #angle =90 + 1.8*speed
        obj.speedometer.angle += 1.8
        x = 100 - 100*math.sin(math.radians(obj.speedometer.angle))
        y = 100 + 100*math.cos(math.radians(obj.speedometer.angle))
        obj.speedometer.speedCanvas.delete(obj.speedometer.speedTxt)
        obj.speedometer.speedCanvas.delete(obj.speedometer.speedArrow)
        obj.speedometer.speedTxt = obj.speedometer.speedCanvas.create_text(100, 65, fill="black", text=str(
            int((obj.speedometer.angle-90)/1.8)), font=('Helvetica 20 bold'))
        obj.speedometer.speedArrow = obj.speedometer.speedCanvas.create_line(
            100, 100, 0 + x, y, arrow=LAST, width=5, fill="blue")

    obj.window.update()

def speedDOWN(obj, speed=0):
    if obj.speedometer.angle > 90:
        #angle =90 + 1.8*speed
        obj.speedometer.angle -= 1.8
        x = 100 - 100*math.sin(math.radians(obj.speedometer.angle))
        y = 100 + 100*math.cos(math.radians(obj.speedometer.angle))
        global speedArrow, speedTxt
        obj.speedometer.speedCanvas.delete(obj.speedometer.speedTxt)
        obj.speedometer.speedCanvas.delete(obj.speedometer.speedArrow)
        obj.speedometer.speedTxt = obj.speedometer.speedCanvas.create_text(100, 65, fill="black", text=str(
            int((obj.speedometer.angle-90)/1.8)), font=('Helvetica 20 bold'))
        obj.speedometer.speedArrow = obj.speedometer.speedCanvas.create_line(
            100, 100, 0 + x, y, arrow=LAST, width=5, fill="blue")

    obj.window.update()
def colorPicker(charge):
    if charge < 20:
        return "#A10000"
    else:
        if charge < 40:
            return "#C25F00"
        else:
            if charge < 60:
                return "#E2BE00"
            else:
                if charge < 80:
                    return "#AAB900"
                else:
                    return "#71B400"
def batteryUP(obj,charge=0):
    if obj.battery.charge < 100:
        obj.battery.charge += 1
        x = 122 - int(obj.battery.charge*1.04)
        color = colorPicker(obj.battery.charge)
        obj.battery.batteryCanvas.delete(obj.battery.batteryCharge)
        obj.battery.batteryCanvas.delete(obj.battery.batteryTxt)
        obj.battery.batteryCanvas.delete(obj.battery.batteryImage)
        obj.battery.batteryCharge = obj.battery.batteryCanvas.create_rectangle(
            69, 122, 5, x, fill=color)
        obj.battery.batteryImage = obj.battery.batteryCanvas.create_image(
            0, 2, image=obj.battery.batteryImages[1], anchor=NW)
        obj.battery.batteryTxt = obj.battery.batteryCanvas.create_text(
            37.5, 110, fill="black", text=str(obj.battery.charge), font=('Helvetica 16 bold'))

    obj.window.update()
def batteryDOWN(obj,charge=0):
    if obj.battery.charge > 0:
        obj.battery.charge -= 1
        x = 122 - int(obj.battery.charge*1.04)
        color = colorPicker(obj.battery.charge)
        obj.battery.batteryCanvas.delete(obj.battery.batteryCharge)
        obj.battery.batteryCanvas.delete(obj.battery.batteryTxt)
        obj.battery.batteryCanvas.delete(obj.battery.batteryImage)
        obj.battery.batteryCharge = obj.battery.batteryCanvas.create_rectangle(
            69, 122, 5, x, fill=color)

        obj.battery.batteryImage = obj.battery.batteryCanvas.create_image(
            0, 2, image=obj.battery.batteryImages[0], anchor=NW)
        obj.battery.batteryTxt = obj.battery.batteryCanvas.create_text(
            37.5, 110, fill="black", text=str(obj.battery.charge), font=('Helvetica 16 bold'))

    obj.window.update()
    
def showAllBatteries(obj):
    if obj.allBatteries.winfo_exists():
        obj.allBatteries.lift()
    else:
        obj.allBatteries = Toplevel()
        obj.allBatteries.geometry("600x500")
        obj.allBatteryCanvas = Canvas(obj.allBatteries, height=500, width=600,
                               background="white", highlightthickness=1)
        
        obj.allBatteries.mainloop()

def change(obj):
    time.sleep(0.5)
    changeSignals(obj,[0,1,1,55])
    obj.window.update()
    time.sleep(0.5)
    obj.window.update()
    changeSignals(obj, [0, 0, 0,20])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [1, 0, 0,100])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [0, 1,0,9])
    obj.window.update()
    time.sleep(0.5)
    changeSignals(obj, [1, 1, 1,45])
    obj.window.update()
    
def changeSignals(obj,signals):
    obj.signals.engineLabel.destroy()
    obj.signals.leftLabel.destroy()
    obj.signals.rightLabel.destroy()
    obj.signals.thermoLabel.destroy()
    engineSignal(obj.signals,signals[0])
    leftSignal(obj.signals, signals[1])
    rightSignal(obj.signals, signals[2])
    thermoSignal(obj.signals, signals[3])

def engineSignal(obj,signal):
    if signal == 0:
        obj.engineLabel = Label(obj.signalFrame, image=obj.engineSignal[0])
    else:
        obj.engineLabel = Label(obj.signalFrame, image=obj.engineSignal[1])
    obj.engineLabel.pack(side=LEFT)

def leftSignal(obj, signal):
    if signal == 0:
        obj.leftLabel = Label(obj.signalFrame, image=obj.leftSignal[0])
    else:
        obj.leftLabel = Label(obj.signalFrame, image=obj.leftSignal[1])
    obj.leftLabel.pack(side=LEFT)
    
def rightSignal(obj, signal):
    if signal == 0:
        obj.rightLabel = Label(obj.signalFrame, image=obj.rightSignal[0])
    else:
        obj.rightLabel = Label(obj.signalFrame, image=obj.rightSignal[1])
    obj.rightLabel.pack(side=LEFT)

def thermoSignal(obj,signal):
    img = obj.thermometer[0]
    if signal > 40:
        img = obj.thermometer[1]
    obj.thermoLabel = Label(
        obj.signalFrame, image=img, text=str(signal), compound=TOP, fg="black", font=('Helvetica 16 bold'))
    obj.thermoLabel.pack(side=LEFT)
    
app = App()
app.window.bind("<Up>", lambda event, obj=app: speedUP(obj))
app.window.bind("<Down>", lambda event, obj=app: speedDOWN(obj))
app.window.bind("<Left>", lambda event, obj=app: batteryUP(obj))
app.window.bind("<Right>", lambda event, obj=app: batteryDOWN(obj))
app.battery.batteryCanvas.bind(
    "<Button-1>", lambda event, obj=app.battery: showAllBatteries(obj))
app.window.bind("<BackSpace>", lambda event, obj=app: change(obj))

app.window.mainloop()
