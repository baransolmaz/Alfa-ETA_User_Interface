import time
from tkinter import *
import math
import folium
from selenium import webdriver
from PIL import Image, ImageTk
import os
import serial
import threading as thr
_PORT_ = '/dev/ttyUSB0'
#manager = mp.Manager()
#_END_FLAG_ = manager.Value("i", 0)
#_END_FLAG_=mp.Value("i",0)
_END_FLAG_=0
class App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("705x650")  # Screen Size
        self.window.resizable(0, 0)
        self.window.title("ALFA-ETA")  # Pencere ismi
        self.window.iconname("ALFA-ETA")
        self.window.config(background="white")
        photo = PhotoImage(file="Images/logo.png")  # app icon
        self.window.iconphoto("false", photo)
        self.speedometer = Speedometer(self)
        self.mainBattery = Battery(self, "Main", 0, 525)
        x = 80;y = 130
        self.allBatteries=[[0 for j in range(5)] for i in range(4)]
        for i in range(4):
            for j in range(5):
                if ((i*5)+j)<18:
                    self.allBatteries[i][j] = Battery(self, (i*5+j), (x*j)+1, (y*i)+1)
        #self.allBatteries = [[Battery(self, (i*5+j), (x*j)+1, (y*i)+1) for j in range(5)] for i in range(4)]
        self.signals = Signals(self)
        self.location = Location(self)
        #self.mapThread = thr.Thread(target=self.location.)
        self.logo = Logo(self)
        self.steer = Steering(self)
        self.serial= self.connectUSB();
        self.readData = thr.Thread(target=self.readAndParseDATA)
        self.readData.start()
        
    def connectUSB(self):
        ser = serial.Serial(
            # Serial Port to read the data from
            port=_PORT_,
            #Rate at which the information is shared to the communication channel
            baudrate=9600,
            #Applying Parity Checking (none in this case)
            parity=serial.PARITY_NONE,
            # Pattern of Bits to be read
            stopbits=serial.STOPBITS_ONE,
            # Total number of bits to be read
            bytesize=serial.EIGHTBITS,
            # Number of serial commands to accept before timing out
            timeout=1
        )
        return ser
    def readAndParseDATA(self):
        while(getFlag()==0):
            x = self.serial.readline()
            datas=str(x).split(":")
            paket = datas[0][2:4]
            if paket == '1':  # Battery 0 - 12
                paket1(self,datas[1])
            if paket == '2':  # Battery 12 - 18  + Left -Right Signal +Motor +Leakage Signal+Amper+Volt+pil Temp. 
                paket2(self, datas[1])
            if paket == '3':
                paket3(self, datas[1])
class Logo:
    def __init__(self, obj):
        self.logoCanvas = Canvas(
            obj.window, height=100, width=150, background="blue", highlightthickness=0)
        self.photo = PhotoImage(file="Images/logo.png")
        self.logoCanvas.create_image(75, 50, image=self.photo, anchor=CENTER)
        self.logoCanvas.place(x=375, y=400)
class Signals:
    def __init__(self, obj):
        # Current,Voltage,Engine,Left,Right,Tempereture
        self.allSignals = [0, 0, 0, 0, 0, 0]
        self.electroSignals = self.ElectroSignals(obj)
        self.engineSignal = self.EngineSignal(obj)
        self.directionSignals = self.DirectionSignals(obj)
        self.thermoSignal = self.ThermoSignal(obj)
        self.leakageSignal = self.LeakageSignal(obj)
    class EngineSignal(object):
        def __init__(self, obj):
            self.engineImage = [PhotoImage(
                file='Images/engine_ok.png'), PhotoImage(file='Images/engine_bad.png')]
            self.engineCanvas = Canvas(
                obj.window, height=50, width=49, background="blue", highlightthickness=1)
            self.engineCanvas.create_image(
                25, 25, image=self.engineImage[0], anchor=CENTER)
            self.engineCanvas.place(x=200, y=575, anchor=S)
    class ElectroSignals(object):
        def __init__(self, obj):
            self.electroSignal = [PhotoImage(file='Images/A.png'), PhotoImage(file='Images/V.png')]
            self.current = self.Current(obj, self.electroSignal[0])
            self.voltage = self.Voltage(obj, self.electroSignal[1])
        class Current(object):
            def __init__(self, obj, image):
                self.currentCanvas = Canvas(
                    obj.window, height=75, width=49, background="red", highlightthickness=1)
                self.currentCanvas.create_image(25, 25, image=image, anchor=CENTER)
                self.currentCanvas.place(x=100, rely=1, anchor=S)
                self.currentTxt = self.currentCanvas.create_text(
                    25, 65, fill="black", text="0", font=('Helvetica 16 bold'))
        class Voltage(object):
            def __init__(self, obj, image):
                self.voltageCanvas = Canvas(
                    obj.window, height=75, width=49, background="yellow", highlightthickness=1)
                self.voltageCanvas.create_image(25, 25, image=image, anchor=CENTER)
                self.voltageCanvas.place(x=150, rely=1, anchor=S)
                self.voltageTxt = self.voltageCanvas.create_text(
                    25, 65, fill="black", text="0", font=('Helvetica 16 bold'))
    class DirectionSignals(object):
        def __init__(self, obj):
            self.leftsignal = self.LeftSignal(obj)
            self.rightsignal = self.RightSignal(obj)
        class LeftSignal(object):
            def __init__(self, obj):
                self.leftSignalImage = [PhotoImage(
                    file='Images/left_off.png'), PhotoImage(file='Images/left_on.png')]
                self.leftCanvas = Canvas(
                    obj.window, height=50, width=49, background="red", highlightthickness=1)
                self.leftCanvas.create_image(
                    25, 25, image=self.leftSignalImage[0], anchor=CENTER)
                self.leftCanvas.place(x=100, y=575, anchor=S)
        class RightSignal(object):
            def __init__(self, obj):
                self.rightSignalImage = [PhotoImage(
                    file='Images/right_off.png'), PhotoImage(file='Images/right_on.png')]
                self.rightCanvas = Canvas(
                    obj.window, height=50, width=49, background="yellow", highlightthickness=1)
                self.rightCanvas.create_image(
                    25, 25, image=self.rightSignalImage[0], anchor=CENTER)
                self.rightCanvas.place(x=150, y=575, anchor=S)
    class ThermoSignal(object):
        def __init__(self, obj):
            self.thermometer = [PhotoImage(
                file='Images/thermometer_ok.png'), PhotoImage(file='Images/thermometer_bad.png')]
            self.thermoCanvas = Canvas(
                obj.window, height=75, width=49, background="blue", highlightthickness=1)
            self.thermoCanvas.create_image(25, 26, image=self.thermometer[0], anchor=CENTER)
            self.thermoCanvas.place(x=200, rely=1, anchor=S)
            self.thermoTxt = self.thermoCanvas.create_text(
                25, 65, fill="black", text="0", font=('Helvetica 16 bold'))
    class LeakageSignal(object):
        def __init__(self, obj):
            self.leakageImage = [PhotoImage(
                file='Images/red_dot_empty.png'), PhotoImage(file='Images/red_dot_full.png')]
            self.leakageCanvas = Canvas(
                obj.window, height=75, width=49, background="black", highlightthickness=1)
            self.img = self.leakageCanvas.create_image(25, 25, image=self.leakageImage[0], anchor=CENTER)
            self.leakageCanvas.place(x=250, rely=1, anchor=S)
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
        self.speedCanvas.place(x=375, rely=1, anchor=S)
        #SPEED Arrow
        self.speedArrow = self.speedCanvas.create_line(
            100, 100, 0, 100, arrow=LAST, width=5, fill="blue")
        self.angle = 90
        self.speedTxt = self.speedCanvas.create_text(
            100, 65, fill="black", text="0", font=('Helvetica 20 bold'))
class Battery:
    def __init__(self, obj, name, _x_=100, _y_=100):
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
        self.batteryName = self.batteryCanvas.create_text(
            37.5, 35, fill="black", text=name, font=('Helvetica 14 roman'))
        self.batteryTxt = self.batteryCanvas.create_text(
            37.5, 110, fill="black", text="0", font=('Helvetica 16 bold'))
        self.charge = 0
class Location:
    def __init__(self, obj):
        self.location = [40.9016, 29.2258]  # x,y
        self.locationCanvas = Canvas(obj.window, height=25, width=300,
                                     background="white", highlightthickness=1)
        self.locationCanvas.place(x=400, y=300)
        self._X_ = self.locationCanvas.create_text(
            20, 15, fill="black", text="X: ", font=('Helvetica 16 bold'))
        self._Y_ = self.locationCanvas.create_text(
            160, 15, fill="black", text="Y: ", font=('Helvetica 16 bold'))
        self._X_Loc = self.locationCanvas.create_text(
            40, 15, fill="black", text=str(self.location[0]), font=('Helvetica 14 roman'), anchor=W)
        self._Y_Loc = self.locationCanvas.create_text(
            180, 15, fill="black", text=str(self.location[1]), font=('Helvetica 14 roman'), anchor=W)
        self.button = Button(obj.window, text='Show On Map !',bd='1', command=lambda: self.updateLoc(obj))
        self.button.place(x=480, y=325)
        self.imageCanvas = Canvas(obj.window, height=300, width=300,background="red", highlightthickness=1)
        self.imageCanvas.place(x=400, y=0)
    def updateLoc(self, obj):
        mapLoc = folium.Map(location=self.location,
                            tiles="OpenStreetMap", zoom_start=15, zoom_control=False)
        folium.Marker(location=self.location).add_to(mapLoc)
        directory = os.path.dirname(os.path.abspath(__file__))
        mapLoc.save(directory+"/Map/map.html")
        self.savePNG()
        self.imag = PhotoImage(file=(directory+'/Map/ss.png'))
        self.image = self.imageCanvas.create_image(0, 0, image=self.imag, anchor=NW)
        self.imageCanvas.pack()
        self.imageCanvas.place(x=400, y=0)
        obj.window.update()
    def savePNG(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        opt.add_argument("--offline")
        driver = webdriver.Chrome(options=opt)
        driver.set_window_size(320, 320)  # choose a resolution
        directory = os.path.dirname(os.path.abspath(__file__))
        driver.get("file://"+directory+"/Map/map.html")
        time.sleep(1)
        # You may need to add time.sleep(seconds) here
        driver.save_screenshot(directory+'/Map/ss.png')
        #driver.close()
    def changeLoc(self, obj, locs):
        self.location = locs
        self.locationCanvas.delete(self._X_Loc)
        self.locationCanvas.delete(self._Y_Loc)
        self._X_Loc = self.locationCanvas.create_text(
            40, 15, fill="black", text=str(locs[0]), font=('Helvetica 14 roman'), anchor=W)
        self._Y_Loc = self.locationCanvas.create_text(
            180, 15, fill="black", text=str(locs[1]), font=('Helvetica 14 roman'), anchor=W)
        obj.window.update()
class Steering:
    def __init__(self, obj):
        self.steerStrait = Image.open("Images/direksiyon.png")
        self.steerImage = ImageTk.PhotoImage(self.steerStrait)
        self.steerCanvas = Canvas(
            obj.window, height=196, width=200, background="white", highlightthickness=0)
        self.steer = self.steerCanvas.create_image(
            100, 102, image=self.steerImage, anchor=CENTER)
        self.steerCanvas.place(relx=1, rely=1, anchor=SE)
        self.steerAngle = 0
def changeSteer(obj):  # + sol (- sag)
    for i in range(0, 270):
        updateSteer(obj, i)
    time.sleep(1)
    for i in range(270, -540, -1):
        updateSteer(obj, i)
def updateSteer(obj, angle=0):
    obj.steer.steerCanvas.delete(obj.steer.steer)
    obj.steer.steerImage = ImageTk.PhotoImage(
        obj.steer.steerStrait.rotate(angle))
    obj.steer.steer = obj.steer.steerCanvas.create_image(
        100, 102, image=obj.steer.steerImage, anchor=CENTER)
    obj.window.update()
def changeSpeed(obj):
    for i in range(0, 80):
        updateSpeed(obj, i)
    for i in range(80, 40, -1):
        updateSpeed(obj, i)
    for i in range(40, 100):
        updateSpeed(obj, i)
    for i in range(100, 0, -1):
        updateSpeed(obj, i)
def changeBattery(obj):
    for i in range(0, 80):
        updateBattery(obj.allBatteries[0][4], i)
        obj.window.update()
    for i in range(80, 40, -1):
        updateBattery(obj.allBatteries[0][4], i)
        obj.window.update()
    for i in range(40, 100):
        updateBattery(obj.allBatteries[0][4], i)
        obj.window.update()
    for i in range(100, 0, -1):
        updateBattery(obj.allBatteries[0][4], i)
        obj.window.update()
def changeLoc(obj):
    updateLoc(obj, [40.807712, 29.355991])
def updateLoc(obj,loc):
    obj.location.changeLoc(obj, loc)
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
def changeSig(obj):
    time.sleep(0.5)
    changeSignals(obj, [3, 46, 0, 1, 1, 55, 0])
    time.sleep(0.5)
    changeSignals(obj, [10, 15, 0, 0, 0, 20, 1])
    time.sleep(0.5)
    changeSignals(obj, [36, 54, 1, 0, 1, 100, 1])
    time.sleep(0.5)
    changeSignals(obj, [0, 0, 0, 1, 0, 9, 0])
    time.sleep(0.5)
    changeSignals(obj, [99, 99, 1, 1, 1, 45, 0])
    time.sleep(0.5)
    changeSignals(obj, [0, 0, 0, 0, 0, 0, 1])
def changeSignals(obj, signals):
    changeElectroSignal(obj.signals.electroSignals, signals[0:2])
    changeEngineSignal(obj.signals.engineSignal, signals[2])
    changeDirectionSignal(obj.signals.directionSignals, signals[3:5])
    changeThermoSignal(obj.signals.thermoSignal, signals[5])
    changeLeakageSignal(obj.signals.leakageSignal, signals[6])
    obj.window.update()
def changeElectroSignal(obj, signals):
    obj.current.currentCanvas.delete(obj.current.currentTxt)
    obj.voltage.voltageCanvas.delete(obj.voltage.voltageTxt)
    obj.current.currentTxt = obj.current.currentCanvas.create_text(
        25, 65, fill="black", text=str(signals[0]), font=('Helvetica 16 bold'))
    obj.voltage.voltageTxt = obj.voltage.voltageCanvas.create_text(
        25, 65, fill="black", text=str(signals[1]), font=('Helvetica 16 bold'))
def changeEngineSignal(obj, signal):
    obj.engineCanvas.create_image(
        25, 25, image=obj.engineImage[signal], anchor=CENTER)
def changeDirectionSignal(obj, signals):
    obj.leftsignal.leftCanvas.create_image(
        25, 25, image=obj.leftsignal.leftSignalImage[signals[0]], anchor=CENTER)
    obj.rightsignal.rightCanvas.create_image(
        25, 25, image=obj.rightsignal.rightSignalImage[signals[1]], anchor=CENTER)
def changeThermoSignal(obj, signal):
    img = obj.thermometer[0]
    if signal > 40:
        img = obj.thermometer[1]
    obj.thermoCanvas.create_image(
        25, 26, image=img, anchor=CENTER)
    obj.thermoCanvas.delete(obj.thermoTxt)
    obj.thermoTxt = obj.thermoCanvas.create_text(
        25, 65, fill="black", text=str(signal), font=('Helvetica 16 bold'))
def changeLeakageSignal(obj, signal):
    obj.leakageCanvas.delete(obj.img)
    obj.img = obj.leakageCanvas.create_image(25, 25, image=obj.leakageImage[signal], anchor=CENTER)
def exit_func(obj):
    setFlag(1)
    obj.readData.join()
    obj.window.destroy()
    
def getFlag():
    global _END_FLAG_
    return _END_FLAG_    
def setFlag(i):
    global _END_FLAG_
    #_END_FLAG_= mp.Value("i", 1)
    _END_FLAG_=1
def paket1(obj, datas):
    arr= datas.split("\\")[0].split(",")
    for i in range(0, 2):
        for j in range(0,5):
            updateBattery(obj.allBatteries[i][j], int(arr[(5*i)+j]))
    for i in range(0, 2):
        updateBattery(obj.allBatteries[2][i], int(arr[10+i]))
        
def paket2(obj, datas):
    arr= datas.split("\\")[0].split(",")
    for i in range(3):
        updateBattery(obj.allBatteries[2][2+i], int(arr[i]))
    for i in range(3):
        updateBattery(obj.allBatteries[3][i], int(arr[i+3]))
    sag=int(arr[6])
    sol = int(arr[7])
    kacak = int(arr[8])
    mot = int(arr[9])
    amp = int(arr[10])
    volt = int(arr[11])
    sicaklik = float(arr[12])
    changeSignals(obj, [amp,volt,mot, sol, sag, sicaklik,kacak])
    updateSpeed(obj, int(arr[13]))
    
def paket3(obj, datas):
    arr= datas.split("\\")[0].split(",")
    updateSteer(obj, float(arr[0]))
    updateLoc(obj, [float(arr[1]), float(arr[2])])

if __name__ == '__main__':
    app = App()
    app.window.bind("<Up>", lambda event, obj=app: changeSpeed(obj))
    app.window.bind("<Left>", lambda event, obj=app: changeBattery(obj))
    app.window.bind("<BackSpace>", lambda event, obj=app: changeSig(obj))
    app.window.bind("<Down>", lambda event, obj=app: changeLoc(obj))
    app.window.bind("<Right>", lambda event, obj=app: changeSteer(obj))
    app.window.protocol('WM_DELETE_WINDOW', lambda obj= app: exit_func(obj))
    app.window.mainloop()
