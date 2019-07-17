import numpy as np
import cv2
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import pandas as pd

window = tk.Tk()
window.geometry("+500+400")
panelA = None
panelB = None


final = True
cap = cv2.VideoCapture(0)

def nothing(x):
    pass
def makeBars():
    datahsv = pd.read_csv("current.csv")
    cv2.namedWindow('image')
    cv2.createTrackbar('Hue Min', 'image', datahsv.hMin[0], 255, nothing)
    cv2.createTrackbar('Hue Max', 'image', datahsv.hMax[0], 255, nothing)
    cv2.createTrackbar('Sat Min', 'image', datahsv.sMin[0], 255, nothing)
    cv2.createTrackbar('Sat Max', 'image', datahsv.sMax[0], 255, nothing)
    cv2.createTrackbar('Val Min', 'image', datahsv.vMin[0], 255, nothing)
    cv2.createTrackbar('Val Max', 'image', datahsv.vMax[0], 255, nothing)
def use():
    hMin = cv2.getTrackbarPos('Hue Min', 'image')
    hMax = cv2.getTrackbarPos('Hue Max', 'image')
    sMin = cv2.getTrackbarPos('Sat Min', 'image')
    sMax = cv2.getTrackbarPos('Sat Max', 'image')
    vMin = cv2.getTrackbarPos('Val Min', 'image')
    vMax = cv2.getTrackbarPos('Val Max', 'image')
    dict = {"hMin": [hMin],
            "hMax": [hMax],
            "sMin": [sMin],
            "sMax": [sMax],
            "vMin": [vMin],
            "vMax": [vMax]
            }
    data = pd.DataFrame(dict)
    data.to_csv("current.csv")
def save():

    hMin = cv2.getTrackbarPos('Hue Min', 'image')
    hMax = cv2.getTrackbarPos('Hue Max', 'image')
    sMin = cv2.getTrackbarPos('Sat Min', 'image')
    sMax = cv2.getTrackbarPos('Sat Max', 'image')
    vMin = cv2.getTrackbarPos('Val Min', 'image')
    vMax = cv2.getTrackbarPos('Val Max', 'image')

    dict = {"hMin": [hMin],
            "hMax":[hMax],
            "sMin": [sMin],
            "sMax":[sMax],
            "vMin":[vMin],
            "vMax":[vMax]
            }
    data = pd.DataFrame(dict)
    print(data)
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    data.to_csv(export_file_path, index=None, header=True)
    #data.to_csv("data.csv")
def default():
    datahsv = pd.read_csv("default.csv")
    cv2.setTrackbarPos('Hue Min', 'image', datahsv.hMin[0])
    cv2.setTrackbarPos('Hue Max', 'image', datahsv.hMax[0])
    cv2.setTrackbarPos('Sat Min', 'image', datahsv.sMin[0])
    cv2.setTrackbarPos('Sat Max', 'image', datahsv.sMax[0])
    cv2.setTrackbarPos('Val Min', 'image', datahsv.vMin[0])
    cv2.setTrackbarPos('Val Max', 'image', datahsv.vMax[0])
def load():
    open_file = filedialog.askopenfilename()
    datahsv = pd.read_csv(open_file)
    cv2.setTrackbarPos('Hue Min', 'image', datahsv.hMin[0])
    cv2.setTrackbarPos('Hue Max', 'image', datahsv.hMax[0])
    cv2.setTrackbarPos('Sat Min', 'image', datahsv.sMin[0])
    cv2.setTrackbarPos('Sat Max', 'image', datahsv.sMax[0])
    cv2.setTrackbarPos('Val Min', 'image', datahsv.vMin[0])
    cv2.setTrackbarPos('Val Max', 'image', datahsv.vMax[0])
def exit():
    global final
    final = False
    cv2.destroyAllWindows()
def show_frame():
    global final
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame,(320,240))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.resize(hsv,(320,240))
    hMin = cv2.getTrackbarPos('Hue Min', 'image')
    hMax = cv2.getTrackbarPos('Hue Max', 'image')
    sMin = cv2.getTrackbarPos('Sat Min', 'image')
    sMax = cv2.getTrackbarPos('Sat Max', 'image')
    vMin = cv2.getTrackbarPos('Val Min', 'image')
    vMax = cv2.getTrackbarPos('Val Max', 'image')
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    gray = cv2.inRange(hsv, lower, upper)

    cv2.imshow("original",frame)
    cv2.moveWindow("original",200,100)
    cv2.imshow("masked", gray)
    cv2.moveWindow("masked", 540, 100)
    cv2.moveWindow("image", 880, 100)
    if final == True:
        window.after(10, show_frame)
    else:
        cv2.destroyAllWindows()
        window.destroy()

btn_default=tk.Button(window, text="Default", width=50, command=default)
btn_default.pack(anchor=tk.CENTER, expand=True)

btn_save=tk.Button(window, text="Save", width=50, command=save)
btn_save.pack(anchor=tk.CENTER, expand=True)

btn_load=tk.Button(window, text="Load", width=50, command=load)
btn_load.pack(anchor=tk.CENTER, expand=True)

btn_use=tk.Button(window, text="Use this set", width=50, command=use)
btn_use.pack(anchor=tk.CENTER, expand=True)

btn_exit=tk.Button(window, text="Exit", width=50, command=exit)
btn_exit.pack(anchor=tk.CENTER, expand=True)
makeBars()
show_frame()

window.mainloop()  #Starts GUI
