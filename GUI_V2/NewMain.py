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
        x = 80 ; y = 130
        self.allBatteries = [[Battery(self, (x*j)+5, (y*i)+5) for j in range(8)] for i in range(4)]
        self.signals=Signals(self)
class Signals:
    def __init__(self, obj):
        #Signals Canvas
        self.allSignals=[0,0,0,0,0,0]#Current,Voltage,Engine,Left,Right,Tempereture        
        self.electroSignals = self.ElectroSignals(obj)
        self.engineSignal = self.EngineSignal(obj)
        self.directionSignals=self.DirectionSignals(obj)
        self.thermoSignal=self.ThermoSignal(obj)
        
    class EngineSignal(object):
        def __init__(self, obj):
            self.engineImage = [PhotoImage(
                file='Images/engine_ok.png'), PhotoImage(file='Images/engine_bad.png')]
            self.engineCanvas = Canvas(
                obj.window, height=60, width=40, background="black", highlightthickness=1)
            self.engineCanvas.create_image(
                20, 20, image=self.engineImage[0], anchor=CENTER)
            self.engineCanvas.place(x=200, rely=1, anchor=S)
    class ElectroSignals(object):
        def __init__(self, obj):
            self.electroSignal = [PhotoImage(file='Images/A.png'), PhotoImage(file='Images/V.png')]
            self.current = self.Current(obj, self.electroSignal[0])
            self.voltage = self.Voltage(obj, self.electroSignal[1])
        class Current(object):
            def __init__(self, obj, image):
                self.currentCanvas = Canvas(
                    obj.window, height=60, width=40, background="red", highlightthickness=1)
                self.currentCanvas.create_image(
                    20, 20, image=image, anchor=CENTER)
                self.currentCanvas.place(x=100, rely=1, anchor=S)
                self.currentTxt = self.currentCanvas.create_text(
                    20, 50, fill="black", text="0", font=('Helvetica 15 bold'))
        class Voltage(object):
            def __init__(self,obj,image):
                self.voltageCanvas = Canvas(
                        obj.window, height=60, width=40, background="yellow", highlightthickness=1)
                self.voltageCanvas.create_image(
                    20, 20, image=image, anchor=CENTER)
                self.voltageCanvas.place(x=150, rely=1, anchor=S)  
                self.voltageTxt = self.voltageCanvas.create_text(
                    20, 50, fill="black", text="0", font=('Helvetica 15 bold'))
    class DirectionSignals(object):
        def __init__(self, obj):
            self.leftsignal = self.LeftSignal(obj)
            self.rightsignal = self.RightSignal(obj)
        class LeftSignal(object):
            def __init__(self, obj):
                self.leftSignalImage = [PhotoImage(file='Images/left_off.png'), PhotoImage(file='Images/left_on.png')]
                self.leftCanvas = Canvas(
                    obj.window, height=60, width=40, background="red", highlightthickness=1)
                self.leftCanvas.create_image(
                    20, 20, image=self.leftSignalImage[0], anchor=CENTER)
                self.leftCanvas.place(x=250, rely=1, anchor=S)
        class RightSignal(object):
            def __init__(self, obj):
                self.rightSignalImage = [PhotoImage(
                    file='Images/right_off.png'), PhotoImage(file='Images/right_on.png')]
                self.rightCanvas = Canvas(
                    obj.window, height=60, width=40, background="yellow", highlightthickness=1)
                self.rightCanvas.create_image(
                    20, 20, image=self.rightSignalImage[0], anchor=CENTER)
                self.rightCanvas.place(x=300, rely=1, anchor=S)
    class ThermoSignal(object):
        def __init__(self, obj):
            self.thermometer = [PhotoImage(
                file='Images/thermometer_ok.png'), PhotoImage(file='Images/thermometer_bad.png')]
            self.thermoCanvas = Canvas(
                obj.window, height=60, width=40, background="white", highlightthickness=1)
            self.thermoCanvas.create_image(
                20, 20, image=self.thermometer[0], anchor=CENTER)
            self.thermoCanvas.place(x=350, rely=1, anchor=S)
            self.thermoTxt = self.thermoCanvas.create_text(
                20, 50, fill="black", text="0", font=('Helvetica 15 bold'))
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
        updateBattery(obj.allBatteries[0][5], i)
        obj.window.update()
    for i in range(80, 40, -1):
        updateBattery(obj.allBatteries[0][5], i)
        obj.window.update()
    for i in range(40, 100):
        updateBattery(obj.allBatteries[0][5], i)
        obj.window.update()
    for i in range(100, 0, -1):
        updateBattery(obj.allBatteries[0][5], i)
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
    time.sleep(0.5)
    changeSignals(obj, [10,15,0, 0, 0,20])
    time.sleep(0.5)
    changeSignals(obj, [36,54,1, 0, 1,100])
    time.sleep(0.5)
    changeSignals(obj, [0,0,0, 1,0,9])
    time.sleep(0.5)
    changeSignals(obj, [99,99,1, 1, 1,45])
    time.sleep(0.5)
    changeSignals(obj, [0,0,0,0,0,0])

def changeSignals(obj,signals):
    changeElectroSignal(obj.signals.electroSignals, signals[0:2])
    changeEngineSignal(obj.signals.engineSignal,signals[2])
    changeDirectionSignal(obj.signals.directionSignals, signals[3:5])
    changeThermoSignal(obj.signals.thermoSignal, signals[5])
    obj.window.update()

def changeElectroSignal(obj, signals):
    obj.current.currentCanvas.delete(obj.current.currentTxt)
    obj.voltage.voltageCanvas.delete(obj.voltage.voltageTxt)
    obj.current.currentTxt = obj.current.currentCanvas.create_text(
        20, 50, fill="black", text=str(signals[0]), font=('Helvetica 15 bold'))
    obj.voltage.voltageTxt = obj.voltage.voltageCanvas.create_text(
        20, 50, fill="black", text=str(signals[1]), font=('Helvetica 15 bold'))
def changeEngineSignal(obj, signal):
    obj.engineCanvas.create_image(
            20, 20, image=obj.engineImage[signal], anchor=CENTER)
def changeDirectionSignal(obj, signals):
    obj.leftsignal.leftCanvas.create_image(
        20, 20, image=obj.leftsignal.leftSignalImage[signals[0]], anchor=CENTER)
    obj.rightsignal.rightCanvas.create_image(
        20, 20, image=obj.rightsignal.rightSignalImage[signals[1]], anchor=CENTER)
def changeThermoSignal(obj,signal):
    img = obj.thermometer[0]
    if signal > 40:
        img = obj.thermometer[1]
    obj.thermoCanvas.create_image(
        20, 20, image=img, anchor=CENTER)
    obj.thermoCanvas.delete(obj.thermoTxt)
    obj.thermoTxt = obj.thermoCanvas.create_text(
        20, 50, fill="black", text=str(signal), font=('Helvetica 15 bold'))
        
app = App()
app.window.bind("<Up>", lambda event, obj=app: changeSpeed(obj))
app.window.bind("<Left>", lambda event, obj=app: changeBattery(obj))
app.window.bind("<BackSpace>", lambda event, obj=app: change(obj))

app.window.mainloop()
