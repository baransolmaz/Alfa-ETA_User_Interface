from tkinter import *
import math

class App:
    def __init__(self):
        self.window = Tk()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(str(self.screen_width)+"x" +
                             str(self.screen_height))  # Screen Size

        self.window.minsize(500, 500)
        self.window.title("ALFA-ETA")  # Pencere ismi
        self.window.iconname("ALFA-ETA")
        self.window.config(background="white")
        #app icon
        photo = PhotoImage(file="Images/logo.png")
        self.window.iconphoto("false", photo)
        self.speedometer = Speedometer(self)
        self.battery = Battery(self) 
        #self.driver=Driver(self)       

''' class Driver:
    def __init__(self, obj):
        self.driverCanvas = Canvas(
            obj.window, height=200, width=400, background="white", highlightthickness=0)
        self.driver = PhotoImage(file='driver.png')
        self.driverCanvas.create_image(
            100, 100, image=self.driver, anchor=CENTER)
        self.driverCanvas.pack()
        self.driverCanvas.place(relx=1, rely=0.5, anchor=CENTER)
        self.driverTxt = self.driverCanvas.create_text(
            100, 40, fill="black", text="DRIVER", font=('Helvetica 20 bold')) '''
            
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
        self.normalbattery = PhotoImage(file='Images/normalbattery.png')
        self.chargingbattery = PhotoImage(file='Images/chargbatery.png')
        #Battery Charge
        self.batteryCharge = self.batteryCanvas.create_rectangle(
            69, 122, 5, 122, fill="#A10000")
        self.batteryImage = self.batteryCanvas.create_image(
            0, 2, image=self.normalbattery, anchor=NW)
        self.batteryCanvas.place(relx=0.0, rely=1.0, anchor=SW)
        self.batteryTxt = self.batteryCanvas.create_text(
            37.5, 110, fill="black", text="0", font=('Helvetica 16 bold'))
        self.charge = 0
        self.allBatteries = Toplevel(obj.window)
        self.allBatteries.destroy()

def speedUP(obj):
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
def speedDOWN(obj):
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
def batteryUP(obj):
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
            0, 2, image=obj.battery.chargingbattery, anchor=NW)
        obj.battery.batteryTxt = obj.battery.batteryCanvas.create_text(
            37.5, 110, fill="black", text=str(obj.battery.charge), font=('Helvetica 16 bold'))

    obj.window.update()
def batteryDOWN(obj):
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
            0, 2, image=obj.battery.normalbattery, anchor=NW)
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


app = App()
app.window.bind("<Up>", lambda event, obj=app: speedUP(obj))
app.window.bind("<Down>", lambda event, obj=app: speedDOWN(obj))
app.window.bind("<Left>", lambda event, obj=app: batteryUP(obj))
app.window.bind("<Right>", lambda event, obj=app: batteryDOWN(obj))
app.battery.batteryCanvas.bind(
    "<Button-1>", lambda event, obj=app.battery: showAllBatteries(obj))
app.window.mainloop()
