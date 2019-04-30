from tkinter import Tk, Label, Button, Canvas, PhotoImage, StringVar, Entry
from threading import Thread
import serial
import re


class Dashboard(Thread):
    def __init__(self, root):
        #Call to Thread constructor
        Thread.__init__(self)

        #State Sonde
        self._state = {
            "luminosity": StringVar(),
            "temperature": StringVar(),
            "humidity": StringVar()
        }

        #Thread Bool
        self._isAlive = True

        #VisualVariable
        self._fontTitle = ("Helvetica", 32)
        self._fontNormal = ("Helvetica", 16)
        self._backgroundColor = "#d3ffce"


        #Initialize Window
        self._root = root
        self._root.title("Help My Flower")
        self._root.geometry("400x600")
        self._root.resizable(width=False, height=False)
        self._root.configure(background=self._backgroundColor)
        #self._root.iconbitmap('ressources/hmf_icon.ico')

        #VisualGobal
        self._title = Label(self._root, text="Help My Flower", font=self._fontTitle, background=self._backgroundColor).place(x=50,y=10)
        self._slogan = Label(self._root, text="Parce qu'elles le valent bien !", font=self._fontNormal, background=self._backgroundColor).place(x=60, y=70)

        self._quitButton = Button(self._root, text="Quitter", font=self._fontNormal, command=lambda: self.quit() ).place(x=150, y=500)

        #visualSonde
        self._labelHumidity = Label(self._root, text="Humidité: ", font=self._fontNormal, background=self._backgroundColor).place(x=80, y=200)
        self._sondeHumidity = Entry(self._root, state="disabled", font=self._fontNormal, width=6, textvariable=self._state["humidity"]).place(x=220, y=200)

        self._labelLuminosity = Label(self._root, text="Luminosité: ", font=self._fontNormal, background=self._backgroundColor).place(x=80, y=300)
        self._sondeLuminosity = Entry(self._root, state="disabled", font=self._fontNormal, width=6, textvariable=self._state["luminosity"]).place(x=220, y=300)

        self._labelTemperature = Label(self._root, text="Température: ", font=self._fontNormal, background=self._backgroundColor).place(x=80, y=400)
        self._sondeTemperature = Entry(self._root, state="disabled", font=self._fontNormal, width=6, textvariable=self._state["temperature"]).place(x=220, y=400)
    
    def run(self):
        ser = serial.Serial('COM6', timeout=1)
        while 1:
            donnees = ser.readline()
            data = donnees.decode("utf-8")
            test = re.findall("\d+\.\d+", data)
            print(test)
            if len(test) == 3:
                self._state["humidity"].set(test[0])
                self._state["temperature"].set(test[1])
                self._state["luminosity"].set(test[2])

    def quit(self):
        self._isAlive = False
        self._root.destroy()
            
            




root = Tk()
myDashboard = Dashboard(root)
myDashboard.start()
root.mainloop()
if myDashboard._isDead == True:
    myDashboard.terminate()
